import os
import requests
from urllib.parse import quote
from dotenv import dotenv_values
from pymongo import MongoClient

from app.repository.cards import CardRepository
from app.repository.players import PlayerRepository

from itertools import combinations

basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '../../.env')

config = dotenv_values(env_path)

url = f"{config["CLASH_ROYALE_API_URL"]}"
headers = {
    "Authorization": f"Bearer {config["CLASH_ROYALE_BEARER"]}"
}


def get_cards():
    endpoint_url = f"{url}/cards"
    response = requests.get(endpoint_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")


def get_leaderboard(limit=20):
    endpoint_url = f"{url}/leaderboard/170000001"
    response = requests.get(endpoint_url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Cartas
        items = data.get('items', [])
        # print(items[0:limit])
        return items[0:limit]
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []


def get_player_info(tag):
    encoded_value = quote(tag)
    endpoint_url = f"{url}/players/{encoded_value}"
    response = requests.get(endpoint_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


def get_player_battlelog(tag):
    encoded_value = quote(tag)
    endpoint_url = f"{url}/players/{encoded_value}/battlelog"
    response = requests.get(endpoint_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


from datetime import datetime

if __name__ == '__main__':
    mongodb_client = MongoClient(config["ATLAS_URI"])
    database = mongodb_client[config["DB_NAME"]]

    card_repo = CardRepository(database)
    player_repo = PlayerRepository(database)

    try:
        cards_data = get_cards()
        cards_data_items = cards_data.get('items', [])

        if card_repo.size() > 0:
            for card in cards_data_items:
                card_document = card_repo.get_by_id(card["id"])
                if not card_document:
                    card_repo.create(card)
        else:
            card_repo.create_many(cards_data_items)

        players_in_leaderboard = get_leaderboard(2)

        players_database_empty = False
        if player_repo.size() <= 0:
            players_database_empty = True

        for player in players_in_leaderboard:
            player_tag = player['tag']
            player_data = get_player_info(player_tag)

            if players_database_empty:
                player_repo.create(player_data)
                # players_battlelog = get_player_battlelog(player['tag'])
                # print(players_battlelog)
            else:
                player_document = player_repo.get_by_id(player_tag)
                if not player_document:
                    player_repo.create(player_data)
            '''
            for player_battle in players_battlelog:
                battle_time = player_battle["battleTime"]

                #Converter data string para numerica
                dt = datetime.strptime(battle_time, "%Y%m%dT%H%M%S.%fZ")
                timestamp = dt.timestamp()

                print(player_battle["battleTime"], int(timestamp))
                player_battle["battleTime"] = int(timestamp)
            '''
    finally:
        mongodb_client.close()
    pass
