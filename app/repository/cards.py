from typing import List, Dict

from app.models.cards import Card


class CardRepository:
    def __init__(self, database):
        self.collection = database["cards"]

    def create(self, card: Card) -> str:
        result = self.collection.insert_one(card.dict(by_alias=True))
        return str(result.inserted_id)

    def drop(self):
        self.collection.drop()
    def create_many(self, cards: List[Card]) -> str:
        self.drop()
        transformed_cards = []
        for card in cards:
            if 'id' in card:
                card['_id'] = card.pop('id')
            transformed_cards.append(Card.parse_obj(card))

        print(transformed_cards)
        result = self.collection.insert_many([card.dict(by_alias=True) for card in transformed_cards])
        return [str(inserted_id) for inserted_id in result.inserted_ids]

    def get_all(self) -> List[Card]:
        cards = self.collection.find()
        return [Card(**card) for card in cards]