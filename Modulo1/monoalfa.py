import os
import string
from collections import Counter


def cifra_monoalfabetica(texto, chave_substituicao):
    resultado = ""
    alfabeto_original_minusculo = string.ascii_lowercase # 'abcdefghijklmnopqrstuvwxyz'
    alfabeto_original_maiusculo = string.ascii_uppercase # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Cria o mapeamento de substituição de acordo com a chave 
    mapa_substituicao_minusculo = {}
    mapa_substituicao_maiusculo = {}

    for i in range(26):
        # Mapeia a letra original do alfabeto para a letra na posição 'i' da chave
        mapa_substituicao_minusculo[alfabeto_original_minusculo[i]] = chave_substituicao[i].lower()
        mapa_substituicao_maiusculo[alfabeto_original_maiusculo[i]] = chave_substituicao[i].upper()

    for char in texto:
        if char.isalpha(): # Se for uma letra
            if char.islower():
                # Verifica se a letra está no mapeamento 
                if char in mapa_substituicao_minusculo:
                    resultado += mapa_substituicao_minusculo[char]
                else:
                    # Caracteres como acentos (á, ç) que são letras mas não estão no a-z,
                    # são mantidos inalterados.
                    resultado += char
            elif char.isupper():
                # Verifica se a letra está no mapeamento 
                if char in mapa_substituicao_maiusculo:
                    resultado += mapa_substituicao_maiusculo[char]
                else:
                    # Idem para maiúsculas
                    resultado += char
        else:
            # Se não é uma letra mantém inalterado
            resultado += char
    return resultado


def contar_frequencia_letras(texto):

    # Converte o texto para minúsculas e filtra apenas as letras do alfabeto (a-z)
    letras_no_texto = [char for char in texto.lower() if 'a' <= char <= 'z']
    
    # Usa Counter para contar a frequência de cada letra
    frequencia = Counter(letras_no_texto)
    
    return frequencia

# Programa Principal para Cifra Monoalfabética

if __name__ == "__main__":

    nome_arquivo_entrada = "CLARO.txt"
    chave = "CHAVE.txt" 
    nome_arquivo_cifrado_mono = "claroEmono.txt" # Mantido para referência, mas não será usado para escrita


    # Lendo o arquivo CHAVE.txt
    try:
        # Adicionado para robustez no caminho do arquivo da chave
        script_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_chave = os.path.join(script_dir, chave)

        with open(caminho_chave, 'r', encoding='utf-8') as f_chave_leitura:
            chave_lida = f_chave_leitura.read().strip() # .strip() para remover quebras de linha/espaços em branco
        
        # Validação da chave lida 
        if len(chave_lida) != 26:
            print(f"A chave monoalfabética lida tem {len(chave_lida)} caracteres, mas 26 são esperados para um alfabeto completo.")
        
    except Exception as e:
        print(f"Erro ao ler o arquivo de chave '{chave}': {e}")
        exit()

    # Lendo o texto do arquivo CLARO.txt
    try:
        # Adicionado para robustez no caminho do arquivo de entrada
        caminho_arquivo_entrada = os.path.join(script_dir, nome_arquivo_entrada)

        with open(caminho_arquivo_entrada, 'r', encoding='utf-8') as arquivo:
            mensagemtxt = arquivo.read()
        print(f"\nConteúdo de '{nome_arquivo_entrada}' lido com sucesso:\n") # Adição de print
        print(mensagemtxt) # Adição de print
        print("\n" + "="*60 + "\n") # Adição de print para separador
    except Exception as e:
        print(f"Erro ao ler o arquivo '{nome_arquivo_entrada}': {e}")
        exit()

    # --- Processamento da Cifra Monoalfabética ---
    print("\nProcessando Cifra Monoalfabética ")
    print(f"Chave de substituição lida de '{chave}': '{chave_lida}'")
    
    # Aplicar a Cifra Monoalfabética
    mensagem_cifrada_mono = cifra_monoalfabetica(mensagemtxt, chave_lida)

    # Salvar a saída no arquivo claroEmono.txt (Agora imprime na tela)
    try:
        # with open(nome_arquivo_cifrado_mono, 'w', encoding='utf-8') as arquivo_saida_mono: # Comentado, não será salvo
            # arquivo_saida_mono.write(mensagem_cifrada_mono) # Comentado, não será salvo
        print(f"\nMensagem cifrada (Monoalfabética) que seria salva em '{nome_arquivo_cifrado_mono}':") # Adaptação de print
        print("="*60) # Adição de print para separador
        print(mensagem_cifrada_mono) # Adição de print
        print("="*60 + "\n") # Adição de print para separador
    except Exception as e:
        print(f"Erro ao tentar exibir a mensagem cifrada da Cifra Monoalfabética: {e}") # Adaptação de print

    # Contagem de Frequência das Letras Cifradas
    print("\nContagem de Frequência das Letras Cifradas ")
    # Chama a função para contar a frequência no texto que acabou de ser cifrado
    frequencias_cifradas = contar_frequencia_letras(mensagem_cifrada_mono)

    # Exibe as frequências ordenadas da letra mais comum para a menos comum
    total_letras_contadas = sum(frequencias_cifradas.values())
    if total_letras_contadas > 0:
        print("\n" + "="*60) # Adição de print para separador
        print("Frequência das Letras no Texto Cifrado:") # Adição de print
        print("="*60) # Adição de print para separador
        for letra, contagem in frequencias_cifradas.most_common():
            porcentagem = (contagem / total_letras_contadas) * 100
            print(f"'{letra.upper()}': {contagem} ocorrências ({porcentagem:.2f}%)")
        print("="*60 + "\n") # Adição de print para separador
    else:
        print("Nenhuma letra do alfabeto básico foi encontrada no texto cifrado para contagem.")