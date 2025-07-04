import os     # Para verificar se o arquivo existe

def cifra_cesar(texto, k):
    
    resultado = ""

    for char in texto:
        # Verifica se o caractere é uma letra alfabética 
        if char.isalpha():
            # Converte o char para numero
            codigo_ascii = ord(char)

            # Define o começo e o fim do alfabeto baseado em maiúscula/minúscula
            if 'a' <= char <= 'z':  # É uma letra minúscula (a-z)
                base = ord('a')
                # Calcula a nova posição para minúscula
                index_nova_letra = (codigo_ascii - base + k) % 26 + base
                resultado += chr(index_nova_letra)

            elif 'A' <= char <= 'Z':  # É uma letra maiúscula (A-Z)
                base = ord('A')
                # Calcula a nova posição para maiuscula
                index_nova_letra = (codigo_ascii - base + k) % 26 + base
                resultado += chr(index_nova_letra)
            else:
                resultado += char # Não altera caractere especial

        else:
            # Se não for uma letra (número, espaço, pontuação, etc.), adiciona sem modificação
            resultado += char
    return resultado

# --- Nova Função: Quebra por Força Bruta ---
def quebra_por_fc(texto_cifrado, nome_arquivo_saida="quebra_fc.txt"):
    
    print(f"\nIniciando quebra por força bruta da Cifra de César...")
    # A linha abaixo era para salvar em arquivo, agora só printa a intenção.
    print(f"Os resultados serão exibidos no console.") # Adaptação de print

    # Bloco try/except original, mas o conteúdo de escrita em arquivo será substituído por prints
    try:
        # with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida: # Comentado, não será salvo
        print("\n" + "="*60) # Adição de print para separador visual
        print("Resultados da Quebra por Força Bruta da Cifra de César:") # Adição de print
        print("="*60 + "\n") # Adição de print para separador visual
        print(f"Texto Original (Cifrado):\n{texto_cifrado}\n") # Adição de print

        for chave_tentativa in range(26): # Testa chaves de 0 a 25
            # Usando chave negativa ara descriptografar
            chave_descripto = -chave_tentativa
            
            # Chama a função cifra_cesar para descriptografar com a chave de tentativa
            texto_descriptografado = cifra_cesar(texto_cifrado, chave_descripto)

            # Escreve o resultado no arquivo (agora imprime no console)
            print("-" * 60) # Adição de print para separador
            print(f"Tentativa com Chave k de Cifragem = {chave_tentativa} "
                                f"(Deslocamento de Descriptografia = {chave_descripto}):") # Adição de print
            print(f"{texto_descriptografado}\n") # Adição de print
            # arquivo_saida.write("-" * 60 + "\n\n") # Separador para cada tentativa (Comentado)

        print(f"\nQuebra por força bruta concluída! Resultados exibidos no console.") # Adaptação de print

    except Exception as e:
        print(f"Erro ao exibir os resultados da quebra por força bruta: {e}") # Adaptação de print

# Programa Principal

if __name__ == "__main__":

    nome_arquivo_entrada = "CLARO.txt"
    nome_arquivo_saida = "claroEcesar.txt" # Nome do arquivo original, mas não será usado para escrita
    nome_arquivo_quebra_fc = "quebra_fc.txt" # Novo: nome do arquivo para a força bruta (Nome original)

    # Lendo o txt
    try:
        # Adicionado para robustez no caminho do arquivo, mantendo os comentários originais
        script_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo_entrada = os.path.join(script_dir, nome_arquivo_entrada)

        with open(caminho_arquivo_entrada, 'r', encoding='utf-8') as arquivo:
            mensagemtxt = arquivo.read()
        print(f"\nConteúdo de '{nome_arquivo_entrada}' lido com sucesso:\n") # Adição de print
        print(mensagemtxt) # Adição de print
        print("\n" + "="*60 + "\n") # Adição de print para separador
    except Exception as e:
        print(f"Erro ao ler o arquivo '{nome_arquivo_entrada}': {e}")
        exit()

    # Solicita k para o usuário
    while True:
        k_str = input("Digite o valor de k: ")
        try:
            k = int(k_str)
            break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro válido.")

    # Chama a função da cifra a mensagem lida do arquivo
    mensagem_cifrada = cifra_cesar(mensagemtxt, k)

    # Salva a mensagem cifrada no novo arquivo (claroEcesar.txt) (Agora imprime na tela)
    try:
        # with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida: # Comentado, não será salvo
            # arquivo_saida.write(mensagem_cifrada) # Comentado, não será salvo
        print(f"\nMensagem cifrada (que seria salva em '{nome_arquivo_saida}'):") # Adaptação de print
        print("="*60) # Adição de print para separador
        print(mensagem_cifrada) # Adição de print
        print("="*60 + "\n") # Adição de print para separador
    except Exception as e:
        print(f"Erro ao tentar exibir a mensagem cifrada: {e}") # Adaptação de print

    # Chamando a função de quebra por força bruta
    quebra_por_fc(mensagem_cifrada, nome_arquivo_quebra_fc)