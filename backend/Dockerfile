FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat-traditional
RUN pip install pipenv

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o Pipfile e Pipfile.lock da pasta pai
COPY ../Pipfile ./

# Instalar as dependências do projeto
RUN pipenv install

# Copiar o arquivo .env
COPY ../.env .env

# Copiar o restante do código da aplicação
COPY . .

# Definir o diretório de trabalho correto
WORKDIR /app/backend

# Configurar o PYTHONPATH
ENV PYTHONPATH="/app"

# Tornar o entrypoint.sh executável
COPY /backend/entrypoint.sh /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

# Expor a porta que o FastAPI usará
EXPOSE 8000

# Definir o entrypoint para o contêiner
ENTRYPOINT ["/app/backend/entrypoint.sh"]
