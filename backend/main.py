import os

from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import cards as cards_router, metrics as metrics_router
from backend.routes import players as players_router

basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '../.env')

config = dotenv_values(env_path)

app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost:3000",  # URL do frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(cards_router.router, tags=["cards_router"], prefix="/card")
app.include_router(players_router.router, tags=["players_router"], prefix="/player")
app.include_router(metrics_router.router, tags=["metrics_router"], prefix="/metrics")