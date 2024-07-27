from fastapi import APIRouter, Request
from typing import Any

router = APIRouter()

@router.get("/query1", response_description="", response_model=Any)
def query1(request: Request):
    #Acessando o mongo  database
    #request.app.database
    pass

@router.get("/query2", response_description="", response_model=Any)
def query2(request: Request):
    #Acessando o mongo  database
    #request.app.database
    pass

@router.get("/query3", response_description="", response_model=Any)
def query3(request: Request):
    #Acessando o mongo  database
    #request.app.database
    pass

@router.get("/query4", response_description="", response_model=Any)
def query4(request: Request):
    #Acessando o mongo  database
    #request.app.database
    pass

@router.get("/query5", response_description="", response_model=Any)
def query5(request: Request):
    #Acessando o mongo  database
    #request.app.database
    pass
