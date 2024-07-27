import os
import requests
from urllib.parse import quote
from dotenv import dotenv_values
from pymongo import MongoClient

from app.repository.cards import CardRepository
from app.repository.player_battlelog_combination import BattleLogCombinationRepository, BattleLogCombination
from app.repository.players import PlayerRepository

from datetime import datetime
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

def load_battlelog(tag: str):
    #TODO: COLOCAR NUM FOR PARA INSERIR TODAS PARTIDAS
    players_battlelog = get_player_battlelog(tag)[0]

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

    players_battlelog["battleTime"] = battletime_to_timestamp

    team_sorted_array = sorted(players_battlelog["team"][0]["cards"], key=lambda x: x['id'])
    opponent_sorted_array = sorted(players_battlelog["opponent"][0]["cards"], key=lambda x: x['id'])

    first_card_id_string = players_battlelog["team"][0]["cards"][0]["id"]

    first_card_data = battle_log_combination_repo.find_by_timestamp_and_tag(battletime_to_timestamp, first_card_id_string)
    #Verifica se existe, se existir não insere nada no BD
    if first_card_data:
        return None


    # sorted_data = sorted(team_sorted_array, key=lambda x: x['id'])
    team_sorted_array_1 = list(combinations(team_sorted_array, 1))
    team_sorted_array_2 = list(combinations(team_sorted_array, 2))
    team_sorted_array_3 = list(combinations(team_sorted_array, 3))
    team_sorted_array_4 = list(combinations(team_sorted_array, 4))
    team_sorted_array_5 = list(combinations(team_sorted_array, 5))
    team_sorted_array_6 = list(combinations(team_sorted_array, 6))
    team_sorted_array_7 = list(combinations(team_sorted_array, 7))
    team_sorted_array_8 = list(combinations(team_sorted_array, 8))

    team_card_combination_1 = card_combination_transform(team_sorted_array_1, battletime_to_timestamp,
                                                         team_tag,  # alterar
                                                         team_trophiesDiff,  # alterar
                                                         team_crowns, opponent_crowns,
                                                         team_victory  # alterar
                                                         )
    team_card_combination_2 = card_combination_transform(team_sorted_array_2, battletime_to_timestamp,
                                                        team_tag,  # alterar
                                                        team_trophiesDiff,  # alterar
                                                        team_crowns, opponent_crowns,
                                                        team_victory  # alterar
                                                        )
    team_card_combination_3 = card_combination_transform(team_sorted_array_3, battletime_to_timestamp,
                                                        team_tag,  # alterar
                                                        team_trophiesDiff,  # alterar
                                                        team_crowns, opponent_crowns,
                                                        team_victory  # alterar
                                                        )
    team_card_combination_4 = card_combination_transform(team_sorted_array_4, battletime_to_timestamp,
                                                        team_tag,  # alterar
                                                        team_trophiesDiff,  # alterar
                                                        team_crowns, opponent_crowns,
                                                        team_victory  # alterar
                                                        )
    team_card_combination_5 = card_combination_transform(team_sorted_array_5, battletime_to_timestamp,
                                                         team_tag,  # alterar
                                                         team_trophiesDiff,  # alterar
                                                         team_crowns, opponent_crowns,
                                                         team_victory  # alterar
                                                         )
    team_card_combination_6 = card_combination_transform(team_sorted_array_6, battletime_to_timestamp,
                                                        team_tag,  # alterar
                                                        team_trophiesDiff,  # alterar
                                                        team_crowns, opponent_crowns,
                                                        team_victory  # alterar
                                                        )
    team_card_combination_7 = card_combination_transform(team_sorted_array_7, battletime_to_timestamp,
                                                        team_tag,  # alterar
                                                        team_trophiesDiff,  # alterar
                                                        team_crowns, opponent_crowns,
                                                        team_victory  # alterar
                                                        )

    team_card_combination_8 = card_combination_transform(team_sorted_array_8, battletime_to_timestamp,
                                                         team_tag,  # alterar
                                                         team_trophiesDiff,  # alterar
                                                         team_crowns, opponent_crowns,
                                                         team_victory  # alterar
                                                         )

    battle_log_combination_repo.create(BattleLogCombination.V1, team_card_combination_1)
    battle_log_combination_repo.create(BattleLogCombination.V2, team_card_combination_2)
    battle_log_combination_repo.create(BattleLogCombination.V3, team_card_combination_3)
    battle_log_combination_repo.create(BattleLogCombination.V4, team_card_combination_4)
    battle_log_combination_repo.create(BattleLogCombination.V5, team_card_combination_5)
    battle_log_combination_repo.create(BattleLogCombination.V6, team_card_combination_6)
    battle_log_combination_repo.create(BattleLogCombination.V7, team_card_combination_7)
    battle_log_combination_repo.create(BattleLogCombination.V8, team_card_combination_8)



    # battle_log_combination_repo.create(BattleLogCombination.V8, team_card_combination_8)
    # --------------------OPONNENT
    opponent_sorted_array_1 = list(combinations(opponent_sorted_array, 1))
    opponent_sorted_array_2 = list(combinations(opponent_sorted_array, 2))
    opponent_sorted_array_3 = list(combinations(opponent_sorted_array, 3))
    opponent_sorted_array_4 = list(combinations(opponent_sorted_array, 4))
    opponent_sorted_array_5 = list(combinations(opponent_sorted_array, 5))
    opponent_sorted_array_6 = list(combinations(opponent_sorted_array, 6))
    opponent_sorted_array_7 = list(combinations(opponent_sorted_array, 7))
    opponent_sorted_array_8 = list(combinations(opponent_sorted_array, 8))

    opponent_card_combination_1 = card_combination_transform(opponent_sorted_array_1, battletime_to_timestamp,
                                                             opponent_tag,  # alterar
                                                             opponent_trophiesDiff,  # alterar
                                                             opponent_crowns, team_crowns,
                                                             opponent_victory  # alterar
                                                             )
    opponent_card_combination_2 = card_combination_transform(opponent_sorted_array_2, battletime_to_timestamp,
                                                            opponent_tag,  # alterar
                                                            opponent_trophiesDiff,  # alterar
                                                            opponent_crowns, team_crowns,
                                                            opponent_victory  # alterar
                                                            )
    opponent_card_combination_3 = card_combination_transform(opponent_sorted_array_3, battletime_to_timestamp,
                                                            opponent_tag,  # alterar
                                                            opponent_trophiesDiff,  # alterar
                                                            opponent_crowns, team_crowns,
                                                            opponent_victory  # alterar
                                                            )
    opponent_card_combination_4 = card_combination_transform(opponent_sorted_array_4, battletime_to_timestamp,
                                                            opponent_tag,  # alterar
                                                            opponent_trophiesDiff,  # alterar
                                                            opponent_crowns, team_crowns,
                                                            opponent_victory  # alterar
                                                            )
    opponent_card_combination_5 = card_combination_transform(opponent_sorted_array_5, battletime_to_timestamp,
                                                            opponent_tag,  # alterar
                                                            opponent_trophiesDiff,  # alterar
                                                            opponent_crowns, team_crowns,
                                                            opponent_victory  # alterar
                                                            )
    opponent_card_combination_6 = card_combination_transform(opponent_sorted_array_6, battletime_to_timestamp,
                                                            opponent_tag,  # alterar
                                                            opponent_trophiesDiff,  # alterar
                                                            opponent_crowns, team_crowns,
                                                            opponent_victory  # alterar
                                                            )
    opponent_card_combination_7 = card_combination_transform(opponent_sorted_array_7, battletime_to_timestamp,
                                                            opponent_tag,  # alterar
                                                            opponent_trophiesDiff,  # alterar
                                                            opponent_crowns, team_crowns,
                                                            opponent_victory  # alterar
                                                            )


    opponent_card_combination_8 = card_combination_transform(opponent_sorted_array_8, battletime_to_timestamp,
                                                             opponent_tag,  # alterar
                                                             opponent_trophiesDiff,  # alterar
                                                             opponent_crowns, team_crowns,
                                                             opponent_victory  # alterar
                                                             )

    battle_log_combination_repo.create(BattleLogCombination.V1, opponent_card_combination_1)
    battle_log_combination_repo.create(BattleLogCombination.V2, opponent_card_combination_2)
    battle_log_combination_repo.create(BattleLogCombination.V3, opponent_card_combination_3)
    battle_log_combination_repo.create(BattleLogCombination.V4, opponent_card_combination_4)
    battle_log_combination_repo.create(BattleLogCombination.V5, opponent_card_combination_5)
    battle_log_combination_repo.create(BattleLogCombination.V6, opponent_card_combination_6)
    battle_log_combination_repo.create(BattleLogCombination.V7, opponent_card_combination_7)
    battle_log_combination_repo.create(BattleLogCombination.V8, opponent_card_combination_8)


if __name__ == '__main__':
    mongodb_client = MongoClient(config["ATLAS_URI"])
    database = mongodb_client[config["DB_NAME"]]

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

        players_in_leaderboard = get_leaderboard(2)

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
                load_battlelog(player_tag)



    finally:
        mongodb_client.close()
    pass
