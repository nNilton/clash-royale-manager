from typing import List, Optional, Any
from pydantic import BaseModel, Field


class IconUrls(BaseModel):
    medium: Optional[str] = None
    evolutionMedium: Optional[str] = None

class SupportCard(BaseModel):
    name: str
    id: int
    level: int
    maxLevel: int
    rarity: str
    count: int
    iconUrls: IconUrls

class CurrentDeckCard(BaseModel):
    name: str
    id: int
    level: int
    starLevel: Optional[int] = None
    evolutionLevel: Optional[int] = None
    maxLevel: int
    maxEvolutionLevel: Optional[int] = None
    rarity: str
    count: int
    elixirCost: int
    iconUrls: IconUrls

class FavouriteCard(BaseModel):
    name: str
    id: int
    maxLevel: int
    elixirCost: int
    iconUrls: IconUrls
    rarity: str

class Clan(BaseModel):
    tag: str
    name: str
    badgeId: int

class Arena(BaseModel):
    id: int
    name: str

class Season(BaseModel):
    id: Optional[Any] = None
    rank: Optional[int] = None
    trophies: Optional[int] = None
    bestTrophies: Optional[int] = None

class LeagueStatistics(BaseModel):
    currentSeason: Optional[Season] = None
    previousSeason: Optional[Season] = None
    bestSeason: Optional[Season] = None

class Badge(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    maxLevel: Optional[int] = None
    progress: Optional[int] = None
    target: Optional[int] = None
    iconUrls: IconUrls

class Achievement(BaseModel):
    name: str
    stars: int
    value: int
    target: int
    info: str
    completionInfo: Optional[None] = None

class ProgressArena(BaseModel):
    id: int
    name: str

class Progress(BaseModel):
    goblin_road: Optional[dict] = None
    arena: Optional[ProgressArena] = None
    trophies: Optional[int] = None
    bestTrophies: Optional[int] = None
class Player(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tag: str
    name: str
    expLevel: int
    trophies: int
    bestTrophies: int
    wins: int
    losses: int
    battleCount: int
    threeCrownWins: int
    challengeCardsWon: int
    challengeMaxWins: int
    tournamentCardsWon: int
    tournamentBattleCount: int
    role: Optional[str] = None
    donations: int
    donationsReceived: int
    totalDonations: int
    warDayWins: int
    clanCardsCollected: int
    clan: Optional[Clan] = None
    arena: Arena
    leagueStatistics: LeagueStatistics
    badges: List[Badge]
    achievements: List[Achievement]
    supportCards: List[SupportCard]
    currentDeck: List[CurrentDeckCard]
    currentDeckSupportCards: List[SupportCard]
    currentFavouriteCard: FavouriteCard
    starPoints: int
    expPoints: int
    legacyTrophyRoadHighScore: int
    currentPathOfLegendSeasonResult: Season
    lastPathOfLegendSeasonResult: Season
    bestPathOfLegendSeasonResult: Season
    progress: Progress
    totalExpPoints: int
