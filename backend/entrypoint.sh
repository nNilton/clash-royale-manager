#!/bin/sh

# Esperar o MongoDB estar disponível
# Como estamos acessando na nuvem, eu comentei essa parte
#echo "Waiting for MongoDB to be available..."
#until nc -z -v -w30 mongo 27017
#do
#  echo "Waiting for MongoDB..."
#  sleep 1
#done
#
#echo "MongoDB is up and running!"

# Iniciar a aplicação FastAPI
exec pipenv run uvicorn main:app --host 0.0.0.0 --port 8000
