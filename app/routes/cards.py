from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.models.cards import Card
from app.repository.cards import CardRepository

router = APIRouter()

@router.get("/books", response_description="Listar livros", response_model=List[Card])
def list_books(request: Request):
    user_repo = CardRepository(request.app.database)
    return user_repo.get_all()