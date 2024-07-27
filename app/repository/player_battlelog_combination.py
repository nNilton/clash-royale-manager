from typing import List, Dict

from app.models.cards import Card

from enum import Enum


class BattleLogCombination(Enum):
    V1 = "battlelog_combination_v1"
    V2 = "battlelog_combination_v2"
    V3 = "battlelog_combination_v3"
    V4 = "battlelog_combination_v4"
    V5 = "battlelog_combination_v5"
    V6 = "battlelog_combination_v6"
    V7 = "battlelog_combination_v7"
    V8 = "battlelog_combination_v8"


class BattleLogCombinationRepository:
    def __init__(self, database):
        self.database = database
        self.collection = database[BattleLogCombination.V1.value]

    def change_database(self, database_combination: BattleLogCombination):
        self.collection = self.database[database_combination.value]

    def size(self, database_combination: BattleLogCombination):
        self.change_database(database_combination)

        size = self.collection.count_documents({})
        return size