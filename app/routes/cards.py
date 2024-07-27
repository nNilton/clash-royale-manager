from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.models.cards import Card
from app.repository.cards import CardRepository

router = APIRouter()

@router.get("/", response_description="List All Cards", response_model=List[Card])
def list_cards(request: Request):
    user_repo = CardRepository(request.app.database)
    return user_repo.get_all()