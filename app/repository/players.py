from typing import List, Dict

from bson import ObjectId
from pymongo.collection import Collection

from app.models.cards import Card
from app.models.players import Player


class PlayerRepository:
    def __init__(self, database):
        self.collection: Collection = database["players"]

    def size(self):
        size = self.collection.count_documents({})
        return size

    def get_by_id(self, document_id):
        document = self.collection.find_one({'_id': document_id})
        return document

    def get_all(self) -> List[Player]:
        players = self.collection.find()
        return [Player(**player) for player in players]

    def create(self, player: Dict) -> str:
        player_transform = Player.parse_obj(player)
        player_dict = player_transform.dict()
        player_dict["_id"] = player_dict["tag"]
        result = self.collection.insert_one(player_dict)
        return str(result.inserted_id)

    def create_many(self, cards: List[Card]) -> str:
        self.drop()
        transformed_cards = []
        for card in cards:
            card_dict = Card.parse_obj(card).dict()
            card_dict['_id'] = card_dict['tag']
            transformed_cards.append(card_dict)

        result = self.collection.insert_many(transformed_cards)
        return [str(inserted_id) for inserted_id in result.inserted_ids]

    def drop(self):
        self.collection.drop()
