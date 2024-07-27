from typing import Any, Optional
from pydantic import BaseModel, Field

class Card(BaseModel):
    id: int = Field(alias="_id")
    iconUrls: Any
    name: str
    rarity: str
    maxLevel: Optional[int] = None
    elixirCost: Optional[int] = None
    maxEvolutionLevel: Optional[int] = None

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
            }
        }
