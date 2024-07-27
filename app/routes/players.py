from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException

from app.models.players import Player
from app.repository.players import PlayerRepository

router = APIRouter()

@router.get("/document/{id}", response_description="Get Player By ID", response_model=Player)
def get_player_by_id(request: Request, id: str):
    player_repo = PlayerRepository(request.app.database)
    document = player_repo.get_by_id(id)

    if document:
        return document
    else:
        raise HTTPException(status_code=404, detail="Documento não encontrado")


@router.get("/", response_description="List Players",  response_model_by_alias=False,)
def get_all_players(request: Request):
    player_repo = PlayerRepository(request.app.database)
    return player_repo.get_all()


@router.delete("/", response_description="Drop Players Database")
def drop_players(request: Request):
    player_repo = PlayerRepository(request.app.database)
    return player_repo.drop()