import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from pymongo import MongoClient

from backend.repository.cards import CardRepository
from backend.repository.player_battlelog_combination import BattleLogCombinationRepository, BattleLogCombination
from backend.repository.players import PlayerRepository

from datetime import datetime
from itertools import combinations

basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '../../.env')
load_dotenv(env_path)

# Exemplo de uso de variáveis de ambiente
clash_royale_api_url = os.getenv("CLASH_ROYALE_API_URL")
clash_royale_bearer = os.getenv("CLASH_ROYALE_BEARER")

# Usar a variável em uma f-string corretamente
url = f"{clash_royale_api_url}"
headers = {
    "Authorization": f"Bearer {clash_royale_bearer}"
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


def convert_to_timestamp(battleTime: str):
    return datetime.strptime(battleTime, '%Y%m%dT%H%M%S.%fZ').timestamp()


def card_combination_transform(cards_combination, battletime_to_timestamp, tag, trophiesDiff, team_crowns, opponent_crowns, victory):
    cards_combination_transform = []
    for cards_combination in cards_combination:
        cards_array = [card["id"] for card in cards_combination]
        cards_array_string = "-".join(map(str, cards_array))
        card_dict = {
            "_id": f"{battletime_to_timestamp}-{tag}-{cards_array_string}",
            "cardsIds": cards_array_string,
            "tag": tag,
            "trophiesDiff": trophiesDiff,
            "crowns": team_crowns,
            "crownsOpponent": opponent_crowns,
            "victory": victory,
            "timestamp": battletime_to_timestamp
        }
        cards_combination_transform.append(card_dict)
    return cards_combination_transform

def load_battlelog(players_battlelog: dict):
    if(len(players_battlelog["team"][0]["cards"]) > 8 or players_battlelog["type"] in ('pathOfLegend', 'boatBattle')):
        return

    battletime_to_timestamp = int(datetime.strptime(players_battlelog["battleTime"], '%Y%m%dT%H%M%S.%fZ').timestamp())

    team_Trophies = players_battlelog["team"][0]["startingTrophies"]
    opponent_Trophies = players_battlelog["opponent"][0]["startingTrophies"]

    team_trophiesDiff = int((team_Trophies / opponent_Trophies - 1) * 10000)
    opponent_trophiesDiff = int((opponent_Trophies / team_Trophies - 1) * 10000)

    team_crowns = players_battlelog["team"][0]["crowns"]
    opponent_crowns = players_battlelog["opponent"][0]["crowns"]

    team_victory = team_crowns > opponent_crowns
    opponent_victory = not team_victory

    team_tag = players_battlelog["team"][0]["tag"]
    opponent_tag = players_battlelog["opponent"][0]["tag"]

    team_sorted_array = sorted(players_battlelog["team"][0]["cards"], key=lambda x: x['id'])
    opponent_sorted_array = sorted(players_battlelog["opponent"][0]["cards"], key=lambda x: x['id'])

    first_card_data = battle_log_combination_repo.find_by_timestamp_and_tag(battletime_to_timestamp, team_tag)
    #Verifica se existe, se existir não insere nada no BD
    if first_card_data:
        return None

    for i in range(1, 9):
        battle_log_combination_repo.create(
            BattleLogCombination.list()[i-1],
            card_combination_transform(
                list(combinations(team_sorted_array, i)),
                battletime_to_timestamp,
                team_tag,
                team_trophiesDiff,
                team_crowns,
                opponent_crowns,
                team_victory
            )
        )
    # --------------------OPONNENT

    for i in range(1, 9):
        battle_log_combination_repo.create(
            BattleLogCombination.list()[i - 1],
            card_combination_transform(
                list(combinations(opponent_sorted_array, i)),
                battletime_to_timestamp,
                opponent_tag,
                opponent_trophiesDiff,
                opponent_crowns,
                team_crowns,
                opponent_victory
            )
        )


if __name__ == '__main__':
    atlas_uri = os.getenv("ATLAS_URI")
    db_name = os.getenv("DB_NAME")

    mongodb_client = f"{atlas_uri}"
    database = f"{db_name}"

    mongodb_client = MongoClient(mongodb_client)
    database = mongodb_client[database]

    card_repo = CardRepository(database)
    player_repo = PlayerRepository(database)
    battle_log_combination_repo = BattleLogCombinationRepository(database)

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

        players_in_leaderboard = get_leaderboard(100)

        players_database_empty = False
        if player_repo.size() <= 0:
            players_database_empty = True

        for player in players_in_leaderboard:
            player_tag = player['tag']
            player_data = get_player_info(player_tag)

            player_document = player_repo.get_by_id(player_tag)
            if not player_document:
                player_repo.create(player_data)
                #--- BATTLELOG
                # importing only five matches
                player_battlelog = get_player_battlelog(player_tag)[0:5]
                for battle_log in player_battlelog:
                    load_battlelog(battle_log)



    finally:
        mongodb_client.close()
    pass
