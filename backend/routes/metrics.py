from fastapi import APIRouter, Request, HTTPException
from typing import Any
from backend.repository.player_battlelog_combination import BattleLogCombinationRepository

router = APIRouter()

@router.get("/win-rate/lose-rate/{cardId}/{min_timestamp}/{max_timestamp}", response_description='''
Calcula a porcentagem de vitórias e derrotas utilizando a carta X
(parâmetro) ocorridas em um intervalo de timestamps (parâmetro).''', response_model=Any)
def query1(request: Request,cardId: str,min_timestamp: int, max_timestamp: int):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.get_win_rate_and_lose_rate_by_cardIds_and_timestamps(cardId, [min_timestamp, max_timestamp])


@router.get("/deck/{min_timestamp}/{max_timestamp}/{winrate}", response_description='''
Lista os decks completos que produziram mais de X% (parâmetro) de
vitórias ocorridas em um intervalo de timestamps (parâmetro).''', response_model=Any)
def query2(request: Request, min_timestamp: int, max_timestamp: int, winrate: float):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.get_combo_cards_by_size_and_timestamp_and_win_rate(8, [min_timestamp,max_timestamp], winrate)

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

@router.get("/ten-most-picked-cards/{size}", response_description='''
Lista os 10 combo de cartas (eg: carta 1, carta 2, carta 3... carta n) de
tamanho N (parâmetro) que foram mais jogadas.''', response_model=Any)
def query6(request: Request, size:int):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.get_ten_most_picked_cards(size)

@router.get("/ten-most-popular-decks/{criteria]", response_description='''
Lista os 10 decks de 8 cartas que foram mais populares (jogados entre jogadores
diferentes) obedecendo um criterio minimo de popularidade (parametro) (ex: ao 
menos 3 jogadores diferentes)''', response_model=Any)
def query7(request: Request, criteria:int):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.get_ten_most_popular_decks(criteria)

@router.get("/card/highest-crownDiff", response_description='''
Retorna a carta que conquistou maior diferença de coroas até o momento
(coroas conquistadas pelo usuario da carta - coroas conquistadas pelo
adversario)''', response_model=Any)
def query8(request: Request):
    battlelog_combination_repo = BattleLogCombinationRepository(request.app.database)
    return battlelog_combination_repo.get_card_with_highest_crownDiff()