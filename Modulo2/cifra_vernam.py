import os

def aumenta_chave(chave_bytes, tamanho_necessario):
    chave_expandida = bytearray()
    chave_len = len(chave_bytes)
    
    if chave_len == 0:
        raise ValueError("A chave não pode ser vazia para expansão.")

    for i in range(tamanho_necessario):
        chave_expandida.append(chave_bytes[i % chave_len])
        
    return bytes(chave_expandida)

def aplicar_xor(texto_bytes, chave_expandida_bytes):
    # Aplica a operação XOR entre os bytes do texto e os bytes da chave expandida.
    
    if len(texto_bytes) != len(chave_expandida_bytes):
        raise ValueError("O texto e a chave expandida devem ter o mesmo tamanho para a operação XOR.")

    resultado_bytes = bytearray(len(texto_bytes))
    
    for i in range(len(texto_bytes)):
        resultado_bytes[i] = texto_bytes[i] ^ chave_expandida_bytes[i]
        
    return bytes(resultado_bytes)


if __name__ == "__main__":
    arquivo_claro = "CLARO.txt"
    arquivo_chave = "CHAVE.txt"
    # Essas variáveis serão mantidas para referência, mas os arquivos não serão salvos
    arquivo_vernam_raw = "VernamRAW.txt" 
    arquivo_vernam_bin = "VernamBin.txt"
    arquivo_vernam_utf8 = "VernamUtf8.txt"
    
    print(" Início do Processamento Vernam ")

    # Adicionado para robustez no caminho dos arquivos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo_claro = os.path.join(script_dir, arquivo_claro)
    caminho_arquivo_chave = os.path.join(script_dir, arquivo_chave)

    # Lê e converte CLARO.txt para bytes (UTF-8) 
    print(f"\nLendo '{arquivo_claro}' e convertendo para bytes (UTF-8)...")
    if not os.path.exists(caminho_arquivo_claro): # Usando o caminho robusto
        print(f"Erro: O arquivo '{arquivo_claro}' não foi encontrado.")
        exit()
    try:
        with open(caminho_arquivo_claro, 'r', encoding='utf-8') as f:
            texto_claro_str = f.read()
            texto_claro_bytes = texto_claro_str.encode('utf-8')
        print(f"'{arquivo_claro}' lido e convertido para {len(texto_claro_bytes)} bytes.")
        print(f"Conteúdo de '{arquivo_claro}':\n{texto_claro_str}\n") # Adição de print
    except UnicodeDecodeError:
        print(f"Erro: Não foi possível decodificar '{arquivo_claro}' como UTF-8. Verifique a codificação do arquivo.")
        exit()
    except Exception as e:
        print(f"Erro ao ler '{arquivo_claro}': {e}")
        exit()

    # Lê e converte CHAVE.txt para bytes (UTF-8)
    print(f"\nLendo '{arquivo_chave}' e convertendo para bytes (UTF-8)...")
    if not os.path.exists(caminho_arquivo_chave): # Usando o caminho robusto
        print(f"Erro: O arquivo de chave '{arquivo_chave}' não foi encontrado.")
        print(f"Por favor, crie um arquivo '{arquivo_chave}' no mesmo diretório do script")
        print(f"e insira a chave (ex: 'cauaguencauaguencauaguenca') como seu conteúdo.")
        exit()
    try:
        with open(caminho_arquivo_chave, 'r', encoding='utf-8') as f:
            chave_str = f.read().strip()
            chave_bytes = chave_str.encode('utf-8')
        if not chave_bytes:
            print("Erro: A chave lida está vazia após a conversão para bytes.")
            exit()
        print(f"Chave lida de '{arquivo_chave}' ('{chave_str}') e convertida para {len(chave_bytes)} bytes.") # Adição de print da chave
    except UnicodeDecodeError:
        print(f"Erro: Não foi possível decodificar '{arquivo_chave}' como UTF-8.")
        exit()
    except Exception as e:
        print(f"Erro ao ler '{arquivo_chave}': {e}")
        exit()

    # Expande a chave para o tamanho do texto claro 
    print(f"\nExpandindo a chave ({len(chave_bytes)} bytes) para o tamanho do texto claro ({len(texto_claro_bytes)} bytes)...")
    try:
        chave_expandida = aumenta_chave(chave_bytes, len(texto_claro_bytes))
        print(f"Chave expandida para {len(chave_expandida)} bytes.")
        # print(f"Chave expandida (primeiros 20 bytes): {chave_expandida[:20]!r}...") # Opcional: para ver a chave expandida
    except ValueError as e:
        print(f"Erro ao expandir chave: {e}")
        exit()

    # Aplica XOR (Cifra de Vernam)
    print("\nAplicando a operação XOR (Cifra de Vernam)...")
    try:
        resultado_xor_bytes = aplicar_xor(texto_claro_bytes, chave_expandida)
        print("Operação XOR concluída.")
        print("\n" + "="*60) # Adição de print para separador
        print(f"RESULTADO XOR (em bytes - representação bruta):") # Adição de print
        print("="*60) # Adição de print para separador
        print(resultado_xor_bytes) # Adição de print
        print("="*60 + "\n") # Adição de print para separador
    except ValueError as e:
        print(f"Erro ao aplicar XOR: {e}")
        exit()
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a operação XOR: {e}")
        exit()

    # Salvando VernamRAW.txt (resultado XOR como texto bruto) (AGORA PRINTA)
    print(f"\nO resultado XOR bruto (que seria salvo em '{arquivo_vernam_raw}') foi exibido acima em bytes.") # Adaptação de print


    # Salvando VernamBin.txt (resultado XOR em formato binário puro)  (AGORA PRINTA)
    print(f"O resultado XOR em formato binário puro (que seria salvo em '{arquivo_vernam_bin}') é o mesmo exibido acima em bytes.") # Adaptação de print


    # Tenta converter para UTF-8 e salvar VernamUtf8.txt (AGORA TENTA DECODIFICAR E PRINTAR)
    print(f"\nTentando decodificar o resultado XOR para UTF-8 (que seria salvo em '{arquivo_vernam_utf8}')...") # Adaptação de print
    try:
        # A decodificação só terá sucesso se os bytes resultantes forem uma sequência UTF-8 válida.
        # É muito provável que falhe para um texto cifrado XOR.
        resultado_xor_str_decoded = resultado_xor_bytes.decode('utf-8')
      
        print(f"Sucesso ao decodificar! Resultado decodificado para UTF-8:\n{resultado_xor_str_decoded}\n") # Adição de print
    except UnicodeDecodeError:
        print(f"Falha ao decodificar o resultado XOR para UTF-8. Isso é esperado, pois o resultado de uma cifra XOR geralmente não é texto UTF-8 válido.") # Adaptação de print

    except Exception as e:
        print(f"Erro ao tentar decodificar ou exibir o resultado UTF-8: {e}") # Adaptação de print

    print("\nFim do Processamento Vernam")