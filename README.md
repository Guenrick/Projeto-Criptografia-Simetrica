## Comandos para executar na instância da Imagem:

```bash
# --- Módulo 1 ---
docker run --rm -it criptotp1cauaguenrick bash -c "cd 'Modulo1' && python cesar.py"
docker run --rm -it criptotp1cauaguenrick bash -c "cd 'Modulo1' && python monoalfa.py"

# --- Módulo 2 ---
docker run --rm -it criptotp1cauaguenrick bash -c "cd 'Modulo2' && python cifra_vernam.py"
docker run --rm -it criptotp1cauaguenrick bash -c "cd 'Modulo2' && python vigenere.py"

# --- Módulo 3 ---
docker run --rm -it criptotp1cauaguenrick bash -c "cd 'Modulo3' && python <nome_do_script>.py"
