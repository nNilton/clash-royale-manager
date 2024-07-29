from pydantic import BaseModel, Field
from typing import List, Optional, Any


class IconUrls(BaseModel):
    medium: str
    evolutionMedium: Optional[str] = None

class Card(BaseModel):
    name: str
    id: int
    level: int
    starLevel: Optional[int] = None
    maxLevel: int
    maxEvolutionLevel: Optional[int] = None
    rarity: str
    elixirCost: int
    iconUrls: IconUrls
    evolutionLevel: Optional[int] = None

class SupportCard(BaseModel):
    name: str
    id: int
    level: int
    maxLevel: int
    rarity: str
    iconUrls: IconUrls

class Clan(BaseModel):
    tag: str
    name: str
    badgeId: int

class RoundCard(BaseModel):
    name: str
    id: int
    level: int
    starLevel: Optional[int] = None
    maxLevel: int
    maxEvolutionLevel: Optional[int] = None
    rarity: str
    used: bool
    elixirCost: int
    iconUrls: IconUrls
    evolutionLevel: Optional[int] = None

class Round(BaseModel):
    crowns: int
    kingTowerHitPoints: int
    princessTowersHitPoints: List[int]
    cards: List[RoundCard]
    elixirLeaked: int

class Player(BaseModel):
    tag: str
    name: str
    startingTrophies: Optional[int] = None
    crowns: int
    kingTowerHitPoints: int
    princessTowersHitPoints: List[int]
    clan: Clan
    cards: List[Card]
    supportCards: List[SupportCard]
    globalRank: Optional[int] = None
    rounds: Optional[List[Round]] = None
    elixirLeaked: int
    trophyChange: Optional[int] = None

class Arena(BaseModel):
    id: int
    name: str

class GameMode(BaseModel):
    id: int
    name: str

class Battle(BaseModel):
    type: str
    battleTime: Any
    isLadderTournament: bool
    arena: Arena
    gameMode: GameMode
    deckSelection: str
    team: List[Player]
    opponent: List[Player]
    isHostedMatch: Optional[bool] = None
    leagueNumber: Optional[int] = None
    boatBattleSide: Optional[str] = None
    boatBattleWon: Optional[bool] = None
    newTowersDestroyed: Optional[int] = None
    prevTowersDestroyed: Optional[int] = None
    remainingTowers: Optional[int] = None