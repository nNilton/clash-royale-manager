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

@router.get("/loses/{cardsIds}/{min_timestamp}/{max_timestamp}", response_description='''
Calcula a quantidade de derrotas utilizando o combo de cartas
(X1,X2, ...) (parâmetro) ocorridas em um intervalo de timestamps
(parâmetro).''', response_model=Any)
def query3(request: Request, cardsIds: str, min_timestamp: int, max_timestamp: int ):
    battlelog_combination_repository = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repository.get_lose_count_by_cardIds_and_timestamps(cardsIds, [min_timestamp, max_timestamp])

@router.get("/win-rate/{cardId}/{trophiesDiff}", response_description=
'''Calcula a quantidade de vitórias envolvendo a carta X (parâmetro) nos
casos em que o vencedor possui Z% (parâmetro) menos troféus do que
o perdedor e o perdedor derrubou ao menos duas torres do adversário.''', response_model=Any)
def query4(request: Request, cardId: str, trophiesDiff: int):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.get_matches_by_cardId_and_trophiesDiff_and_victory(cardId, trophiesDiff)

@router.get("/combo-cards/{size}/{min_timestamp}/{max_timestamp}/{winrate}", response_description='''
Lista o combo de cartas (eg: carta 1, carta 2, carta 3... carta n) de
tamanho N (parâmetro) que produziram mais de Y% (parâmetro) de
vitórias ocorridas em um intervalo de timestamps (parâmetro).''', response_model=Any)
def query5(request: Request, size: int, min_timestamp: int, max_timestamp: int, winrate: float):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.get_combo_cards_by_size_and_timestamp_and_win_rate(size, [min_timestamp,max_timestamp], winrate)
