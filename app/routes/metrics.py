from fastapi import APIRouter, Request, HTTPException
from typing import Any
from app.repository.player_battlelog_combination import BattleLogCombinationRepository

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

@router.get("/win-rate/{cardId}/{trophiesDiff}", response_description=
'''Calcula a quantidade de vitórias envolvendo a carta X (parâmetro) nos
casos em que o vencedor possui Z% (parâmetro) menos troféus do que
o perdedor e o perdedor derrubou ao menos duas torres do adversário.''', response_model=Any)
def query4(request: Request, cardId: str, trophiesDiff: int):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.find_win_rate_by_cardId_and_trophiesDiff(cardId, trophiesDiff)

@router.get("/query5", response_description="", response_model=Any)
def query5(request: Request):
    #Acessando o mongo  database
    #request.app.database
    pass
