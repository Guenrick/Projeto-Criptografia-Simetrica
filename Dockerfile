FROM python:3.9-slim-buster

# Diretório de trabalho dentro do contêiner.
WORKDIR /app

# Copiando todos os arquivos .py e .txt em suas pastas.
COPY . /app

# Comando padrão a ser executado quando o contêiner inicia.
CMD ["python"]