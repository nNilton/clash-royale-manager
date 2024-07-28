from typing import List, Dict

from pymongo.collection import Collection

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

    @classmethod
    def list(self):
        return [self.V1, self.V2, self.V3, self.V4, self.V5, self.V6, self.V7, self.V8]


class BattleLogCombinationRepository:
    def __init__(self, database):
        self.database = database
        self.collection: Collection = database[BattleLogCombination.V1.value]

    def change_database(self, database_combination: BattleLogCombination):
        self.collection = self.database[database_combination.value]

    def size(self, database_combination: BattleLogCombination):
        self.change_database(database_combination)

        size = self.collection.count_documents({})
        return size

    def get_by_id(self, document_id):
        document = self.collection.find_one({'_id': document_id})
        return document

    def find_by_timestamp_and_tag(self, battletime_to_timestamp, tag):
        self.change_database(BattleLogCombination.V8)
        document = self.collection.find_one({"_id": {"$regex": f"{battletime_to_timestamp}-{tag}.*"}})
        return document

    def create(self, database_combination: BattleLogCombination, cards_combination: Dict) -> str:
        self.change_database(database_combination)
        self.collection.insert_many(cards_combination)

    def find_win_rate_by_cardId_and_trophiesDiff(self, cardId, trophiesDiff):
        self.change_database(BattleLogCombination.V1)
        return self.collection.find(
            {
                'cardsIds': f'{cardId}',
                'victory': True,
                'crownsOpponent': {'$gte': 2},
                'trophiesDiff': {'$lte': trophiesDiff}
            }
        )