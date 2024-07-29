# Usar a imagem oficial do Node.js
FROM node:20

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos package.json e package-lock.json
COPY package.json package-lock.json ./

# Instalar as dependências
RUN npm install

# Copiar o restante do código da aplicação
COPY . .

# Build da aplicação
RUN npm run build

# Expor a porta que o React usará
EXPOSE 3000

# Comando para iniciar a aplicação React
CMD ["npm", "start"]
