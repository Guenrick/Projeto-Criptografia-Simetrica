import math
import os

def criar_chave_numerica(chave_textual):
    """
    Converte uma chave textual em uma chave numérica de permutação.
    Exemplo: 'cauaguen' -> [3, 1, 7, 2, 5, 8, 4, 6] (baseado na ordem alfabética e posição original para desempate)
    """
    # Cria uma lista de tuplas (caractere, indice_original)
    caracteres_chave_indexados = [(char, i) for i, char in enumerate(chave_textual)]
    
    # Ordena essas tuplas com base no caractere (ordem alfabética)
    # Se os caracteres forem iguais, o índice original é usado como desempate (ordem estável)
    sorted_key_chars = sorted(caracteres_chave_indexados, key=lambda x: x[0])
    
    # Cria a chave numérica atribuindo classificações com base na ordem ordenada
    # A classificação é a posição na lista ordenada + 1 (índice baseado em 1)
    chave_numerica = [0] * len(chave_textual)
    for i, (char, indice_original) in enumerate(sorted_key_chars):
        chave_numerica[indice_original] = i + 1 # Atribui a classificação (baseado em 1) à sua posição original
        
    return chave_numerica

def cifra_transposicao(texto_claro, chave_textual):
    # Remove espaços e caracteres não alfabéticos e converte para maiúsculas.
    texto_claro_normalizado = ''.join(filter(str.isalpha, texto_claro)).upper()

    # Converte a chave para uma chave numérica
    chave_numerica = criar_chave_numerica(chave_textual.lower()) 
    comprimento_chave = len(chave_numerica)
    

    print(f"\nChave textual: '{chave_textual}' \nChave numérica de permutação: {chave_numerica}")

    # Determina o número de linhas necessárias para a matriz
    num_linhas = math.ceil(len(texto_claro_normalizado) / comprimento_chave)

    # Cria a matriz
    matriz = [['' for _ in range(comprimento_chave)] for _ in range(num_linhas)]

    # Preencher a matriz linha por linha
    indice_texto = 0
    for r in range(num_linhas):
        for c in range(comprimento_chave):
            if indice_texto < len(texto_claro_normalizado):
                matriz[r][c] = texto_claro_normalizado[indice_texto]
                indice_texto += 1
            else:
                # Preenchimento para a última linha se não tiver completa.
                matriz[r][c] = 'X' 

    print("\nMatriz do texto claro:")
    for row in matriz:
        print(" ".join(row))

    # Le o texto cifrado reordenado as colunas com base na chave numérica
    texto_cifrado = []
    
    # Cria um mapeamento da classificação para o índice da coluna original
    classificacao_para_indice_coluna_original = [0] * comprimento_chave
    for indice_original, classificacao in enumerate(chave_numerica):
        classificacao_para_indice_coluna_original[classificacao - 1] = indice_original # classificação-1 porque Python é 0-indexado

    print(f"\nOrdem de leitura baseada na chave numérica: {classificacao_para_indice_coluna_original}")

    # Lê as colunas na ordem definida pela chave numérica
    for indice_classificacao in range(comprimento_chave): # Itera da classificação 1 ao comprimento_chave
        coluna_original_a_ler = classificacao_para_indice_coluna_original[indice_classificacao]
        for r in range(num_linhas):
            texto_cifrado.append(matriz[r][coluna_original_a_ler])
            
    return "".join(texto_cifrado)

if __name__ == "__main__":
    arquivo_claro = "CLARO.txt"
    arquivo_chave = "CHAVE.txt" 

    # Lê o texto claro do arquivo CLARO.txt
    if not os.path.exists(arquivo_claro):
        print(f"Erro: O arquivo '{arquivo_claro}' não foi encontrado.")
        exit()
    try:
        with open(arquivo_claro, 'r', encoding='utf-8') as f:
            conteudo_texto_claro = f.read()
    except Exception as e:
        print(f"Erro ao ler '{arquivo_claro}': {e}")
        exit()

    # Lê a chave
    if not os.path.exists(arquivo_chave):
        print(f"Erro: O arquivo de chave '{arquivo_chave}' não foi encontrado.")
        exit()
    try:
        with open(arquivo_chave, 'r', encoding='utf-8') as f:
            chave_textual_lida = f.read().strip() # .strip() serve pra remover quebras de linha/espaços extras
        if not chave_textual_lida:
            print("Erro: A chave lida do arquivo CHAVE.txt está vazia. ")
            exit()
    except Exception as e:
        print(f"Erro ao ler '{arquivo_chave}': {e}")
        exit()

    # Aplica a cifra de transposição 
    print("\nAplicando Cifra de Transposição")
    try:
        texto_cifrado_transposicao = cifra_transposicao(conteudo_texto_claro, chave_textual_lida)
    except ValueError as e:
        print(f"Erro ao cifrar: {e}")
        exit()

    # 4. Salvar o texto cifrado em um arquivo
    nome_arquivo_cifrado_transposicao = "claroETransposicao.txt"
    try:
        with open(nome_arquivo_cifrado_transposicao, 'w', encoding='utf-8') as f_out:
            f_out.write(texto_cifrado_transposicao)
        print(f"\nTexto cifrado salvo em '{nome_arquivo_cifrado_transposicao}'.")
    except Exception as e:
        print(f"Erro ao salvar o texto cifrado de transposição: {e}")

    # Demonstração de como diferentes permutações afetam o texto cifrado 
    print("\n\nDemonstração de diferentes Permutações:")

    # Exemplo 1: Uma chave em ordem alfabética (ou quase)
    chave_exemplo_1 = "abcdefgh"
    print(f"\nCifrando com chave exemplo 1: '{chave_exemplo_1}'")
    texto_cifrado_exemplo_1 = cifra_transposicao(conteudo_texto_claro, chave_exemplo_1)
    print(f"Texto cifrado (Exemplo 1): {texto_cifrado_exemplo_1[:100]}...")

    # Exemplo 2: Uma chave em ordem inversa
    chave_exemplo_2 = "hgfedcba"
    print(f"\nCifrando com chave exemplo 2: '{chave_exemplo_2}'")
    texto_cifrado_exemplo_2 = cifra_transposicao(conteudo_texto_claro, chave_exemplo_2)
    print(f"Texto cifrado (Exemplo 2): {texto_cifrado_exemplo_2[:100]}...")

    print("\nAssim, conclui que a ordem dos caracteres no texto cifrado muda muito com a alteração da chave," \
    " mesmo que o texto original seja o mesmo. Isso acontece porque as colunas são lidas em ordens diferentes, " \
    "embaralhando a sequência dos caracteres.")