from nba_api.stats.library.parameters import SeasonTypeAllStar
from nba_api.stats.endpoints import (
    leaguegamefinder,
    boxscoretraditionalv2,
    playercareerstats,
    leagueleaders,
)
from collections import defaultdict

# from nba_api.stats.static import players

import time

gamefinder = leaguegamefinder.LeagueGameFinder(
    season_nullable="2023-24", season_type_nullable=SeasonTypeAllStar.regular
)
games_raw = gamefinder.get_data_frames()[0].to_dict("records")  # list of dicts

game_ids = [g["GAME_ID"] for g in games_raw]
all_lineups = []

leaders = leagueleaders.LeagueLeaders(
    season="2023-24",
    season_type_all_star=SeasonTypeAllStar.regular,
    stat_category_abbreviation="PTS",  # Points per game
)

player_ppg_list = leaders.get_data_frames()[0][["PLAYER_ID", "PTS", "GP"]].to_dict(
    "records"
)

all_players = {}
for player in player_ppg_list:
    all_players[player["PLAYER_ID"]] = player["PTS"] / player["GP"]

for game_id in game_ids[:10]:  # limit for testing
    try:
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        players = boxscore.get_data_frames()[0].to_dict("records")
        # print(players)
        starters_by_team = {}
        num = defaultdict(int)
        for player in players:
            if player["START_POSITION"]:  # only starters
                team = player["TEAM_ABBREVIATION"]
                starters_by_team.setdefault(team, []).append(player["PLAYER_NAME"])

                if all_players[player["PLAYER_ID"]] <= 10:
                    num[team] += 1

        for team, starters in starters_by_team.items():
            if num[team] >= 3:
                all_lineups.append(
                    {
                        "game_id": game_id,
                        "team": team,
                        "starters": starters,
                    }
                )

        time.sleep(1)

    except Exception as e:
        print(f"Error with {game_id}: {e}")

for lineup in all_lineups:
    print(lineup)


"""
{'game_id': '0022301197', 'team': 'DET', 'starters': ['Troy Brown Jr.', 'Chimezie Metu', 'James Wiseman', 
'Jaden Ivey', 'Marcus Sasser']}
{'game_id': '0022301197', 'team': 'SAS', 'starters': ['Julian Champagnie', 'Sandro Mamukelashvili', 'Zach 
Collins', 'Blake Wesley', 'Tre Jones']}
{'game_id': '0022301200', 'team': 'POR', 'starters': ['Justin Minaya', 'Kris Murray', 'Moses Brown', 'Rayan Rupert', 'Dalano Banton']}
{'game_id': '0022301198', 'team': 'UTA', 'starters': ['Taylor Hendricks', 'Luka Samanic', 'Omer Yurtseven', 'Keyonte George', 'Johnny Juzang']}
{'game_id': '0022301186', 'team': 'WAS', 'starters': ['Johnny Davis', 'Patrick Baldwin Jr.', 'Anthony Gill', 'Deni Avdija', 'Corey Kispert']}
{'game_id': '0022301186', 'team': 'BOS', 'starters': ['Jordan Walsh', 'Sam Hauser', 'Luke Kornet', 'Svi Mykhailiuk', 'Payton Pritchard']}
"""
