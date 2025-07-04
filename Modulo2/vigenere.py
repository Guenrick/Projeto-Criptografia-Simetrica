import os
import math # Para o cálculo do MDC (Máximo Divisor Comum)
from collections import Counter

def vigenere(texto_claro, chave):

    texto_cifrado = ""
    chave_idx = 0
    chave_len = len(chave)
    
    for char_texto in texto_claro:
        if char_texto.isalpha(): # Processa apenas letras
            base = 0
            if char_texto.islower():
                base = ord('a')
            else:
                base = ord('A')
            
            # Obtém o deslocamento da letra da chave (0-25)
            # Garante que a letra da chave usada seja minúscula para o cálculo
            deslocamento = ord(chave[chave_idx % chave_len].lower()) - ord('a')
            
            # Aplica o deslocamento como na Cifra de César
            cifrado_val = (ord(char_texto) - base + deslocamento) % 26
            texto_cifrado += chr(base + cifrado_val)
            
            chave_idx += 1 # Avança para a próxima letra da chave
        else:
            texto_cifrado += char_texto # Mantém caracteres não alfabéticos
            
    return texto_cifrado

def vigenere_decifrar(texto_cifrado, chave):
    texto_claro = ""
    chave_idx = 0
    chave_len = len(chave)
    
    for char_texto_cifrado in texto_cifrado:
        if char_texto_cifrado.isalpha(): # Processa apenas letras
            base = 0
            if char_texto_cifrado.islower():
                base = ord('a')
            else:
                base = ord('A')
            
            # Obtém o deslocamento da letra da chave (0-25)
            # Garante que a letra da chave usada seja minúscula para o cálculo
            deslocamento = ord(chave[chave_idx % chave_len].lower()) - ord('a')
            
            # Aplica o deslocamento inverso
            decifrado_val = (ord(char_texto_cifrado) - base - deslocamento) % 26
            texto_claro += chr(base + decifrado_val)
            
            chave_idx += 1 # Avança para a próxima letra da chave
        else:
            texto_claro += char_texto_cifrado # Mantém caracteres não alfabéticos
            
    return texto_claro

# Método Kasiski 

def calcular_mdc(a, b):
    """Calcula o Máximo Divisor Comum (MDC) de dois números."""
    return math.gcd(a, b)

def encontrar_repeticoes(texto, min_len=3):
    """
    Encontra sequências de caracteres repetidas no texto e suas distâncias.
    Args:
        texto (str): O texto para analisar.
        min_len (int): Tamanho mínimo da sequência a ser considerada.
    Returns:
        dict: Um dicionário onde as chaves são as sequências repetidas
              e os valores são listas das distâncias entre suas ocorrências.
    """
    repeticoes_distancias = {}
    # Filtra apenas letras e converte para minúsculas para a análise de Kasiski
    texto_limpo = ''.join(filter(str.isalpha, texto.lower())) 

    for i in range(len(texto_limpo) - min_len):
        seq = texto_limpo[i : i + min_len]
        # Procura por outras ocorrências da mesma sequência
        for j in range(i + min_len, len(texto_limpo) - min_len + 1):
            if texto_limpo[j : j + min_len] == seq:
                distancia = j - i
                if seq not in repeticoes_distancias:
                    repeticoes_distancias[seq] = []
                repeticoes_distancias[seq].append(distancia)
    return {seq: dists for seq, dists in repeticoes_distancias.items() if len(dists) > 0} # Retorna apenas se houver distâncias

def kasiski_exame(texto_cifrado, min_len_seq=3, max_chave_len=15):
    print("\n Realizando Exame de Kasiski para o Tamanho da Chave ")
    
    # Encontrar sequências repetidas e suas distâncias
    repeticoes_com_distancias = encontrar_repeticoes(texto_cifrado, min_len_seq)

    if not repeticoes_com_distancias:
        print("Não foram encontradas sequências repetidas longas o suficiente para o Exame de Kasiski.")
        print("Pode ser que o texto cifrado seja muito curto ou a chave seja muito longa/aleatória.")
        return []

    print("\nSequências Repetidas Encontradas e Suas Distâncias:")
    for seq, dists in repeticoes_com_distancias.items():
        print(f"  '{seq.upper()}': Distâncias = {dists}")

    # Calculando o MDC de todas as distâncias encontradas
    mdcs_candidatos = []
    for seq, dists in repeticoes_com_distancias.items():
        if len(dists) > 1: # Precisa de pelo menos duas distâncias para calcular MDC entre elas
            mdc_atual = dists[0]
            for i in range(1, len(dists)):
                mdc_atual = calcular_mdc(mdc_atual, dists[i])
            if mdc_atual > 1: # Um MDC de 1 não nos dá muita informação sobre o tamanho da chave
                mdcs_candidatos.append(mdc_atual)
        elif len(dists) == 1: # Se só tem uma ocorrência repetida, sua distância é um candidato
            mdcs_candidatos.append(dists[0])

    if not mdcs_candidatos:
        print("\nNão foi possível calcular MDCs significativos a partir das distâncias.")
        print("Pode ser que a chave seja muito aleatória ou as repetições não sejam causadas pela chave.")
        return []

    # Contando a frequência dos MDCs candidatos
    # Os MDCs mais frequentes são os comprimentos de chave mais prováveis.
    contagem_mdcs = Counter(mdcs_candidatos)
    
    print("\nMDCs Candidatos e Suas Frequências:")
    for mdc, count in contagem_mdcs.most_common():
        print(f"  Tamanho '{mdc}': Ocorrências = {count}")

    # Filtrar MDCs que estejam dentro do limite de comprimento da chave e ordenar por frequência
    tamanhos_provaveis = [
        mdc for mdc, count in contagem_mdcs.most_common()
        if mdc <= max_chave_len and mdc > 0 # Garante que o tamanho é válido
    ]
    
    if not tamanhos_provaveis:
        print(f"\nNenhum comprimento de chave provável (<= {max_chave_len}) foi encontrado.")
    else:
        print(f"\nComprimentos de Chave Prováveis (ordenados por frequência, até {max_chave_len}):")
        print(tamanhos_provaveis)

    return tamanhos_provaveis


# Programa Principal

if __name__ == "__main__":
    nome_arquivo_entrada = "CLARO.txt"
    nome_arquivo_chave = "CHAVE.txt" 
    nome_arquivo_cifrado = "claroEvigenere.txt" # Texto codificado (mantido para referência)
    nome_arquivo_decifrado = "claroDecifradoVigenere.txt" # Texto decodificado (mantido para referência)

    # Adicionado para robustez no caminho dos arquivos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo_entrada = os.path.join(script_dir, nome_arquivo_entrada)
    caminho_arquivo_chave = os.path.join(script_dir, nome_arquivo_chave)

    # Lê o texto do arquivo CLARO.txt
    try:
        with open(caminho_arquivo_entrada, 'r', encoding='utf-8') as arquivo:
            mensagem_clara = arquivo.read()
        print(f"\nConteúdo de '{nome_arquivo_entrada}' lido com sucesso:\n") # Adição de print
        print(mensagem_clara) # Adição de print
        print("\n" + "="*60 + "\n") # Adição de print para separador
    except Exception as e:
        print(f"Erro ao ler o arquivo '{nome_arquivo_entrada}': {e}")
        exit()

    # Lê a chave do arquivo CHAVE.txt
    try:
        with open(caminho_arquivo_chave, 'r', encoding='utf-8') as f_chave:
            chave_vigenere = f_chave.read().strip()
        
        if not chave_vigenere.isalpha() or len(chave_vigenere) == 0:
            print(f"Erro: A chave lida de '{nome_arquivo_chave}' é inválida.")
            print("A chave deve conter apenas letras e não pode ser vazia.")
            exit()
        print(f"Chave lida de '{nome_arquivo_chave}': '{chave_vigenere}'\n") # Adição de print

    except Exception as e:
        print(f"Erro ao ler o arquivo de chave '{nome_arquivo_chave}': {e}")
        exit()

    print("\n Realizando Cifragem Vigenère ")
    texto_cifrado_vigenere = vigenere(mensagem_clara, chave_vigenere)
    
    # Salvando texto cifrado (agora imprime na tela)
    try:
        # with open(nome_arquivo_cifrado, 'w', encoding='utf-8') as arquivo_saida: # Comentado
            # arquivo_saida.write(texto_cifrado_vigenere) # Comentado
        print(f"Texto cifrado (Vigenère) (que seria salvo em '{nome_arquivo_cifrado}'):") # Adaptação de print
        print("="*60) # Adição de print para separador
        print(texto_cifrado_vigenere) # Adição de print
        print("="*60 + "\n") # Adição de print para separador
    except Exception as e:
        print(f"Erro ao tentar exibir o texto cifrado (Vigenère): {e}") # Adaptação de print

    # Decifragem 
    print("\n Realizando Decifragem")
    texto_decifrado_vigenere = vigenere_decifrar(texto_cifrado_vigenere, chave_vigenere)

    # Salvando texto decifrado (agora imprime na tela)
    try:
        # with open(nome_arquivo_decifrado, 'w', encoding='utf-8') as arquivo_decifrado: # Comentado
            # arquivo_decifrado.write(texto_decifrado_vigenere) # Comentado
        print(f"Texto decifrado (Vigenère) (que seria salvo em '{nome_arquivo_decifrado}'):") # Adaptação de print
        print("="*60) # Adição de print para separador
        print(texto_decifrado_vigenere) # Adição de print
        print("="*60 + "\n") # Adição de print para separador
    except Exception as e:
        print(f"Erro ao tentar exibir o texto decifrado (Vigenère): {e}") # Adaptação de print

    #  Executando o Exame de Kasiski no texto cifrado 
    comprimentos = kasiski_exame(texto_cifrado_vigenere)

    print("\n Processos Vigenère Concluídos ")
    if comprimentos:
        print(f"Sugestões de tamanho da chave pelo Kasiski: {comprimentos}")
    else:
        print("Não foi possível estimar o tamanho da chave com o Kasiski para este texto.")