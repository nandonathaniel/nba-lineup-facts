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
    season_nullable="2022-23", season_type_nullable=SeasonTypeAllStar.regular
)
games_raw = gamefinder.get_data_frames()[0].to_dict("records")  # list of dicts
# print(games_raw[0])  # print first game info for debugging

game_ids = [g["GAME_ID"] for g in games_raw]


leaders = leagueleaders.LeagueLeaders(
    season="2022-23",
    season_type_all_star=SeasonTypeAllStar.regular,
    stat_category_abbreviation="PTS",  # Points per game
)

player_ppg_list = leaders.get_data_frames()[0][["PLAYER_ID", "PTS", "GP"]].to_dict(
    "records"
)

all_players = {}
for player in player_ppg_list:
    all_players[player["PLAYER_ID"]] = player["PTS"] / player["GP"]

game_info_by_id = {g["GAME_ID"]: g for g in games_raw}

udah = {}
all_lineups = []

NBA_TEAMS = {
    "ATL",
    "BOS",
    "BKN",
    "CHA",
    "CHI",
    "CLE",
    "DAL",
    "DEN",
    "DET",
    "GSW",
    "HOU",
    "IND",
    "LAC",
    "LAL",
    "MEM",
    "MIA",
    "MIL",
    "MIN",
    "NOP",
    "NYK",
    "OKC",
    "ORL",
    "PHI",
    "PHX",
    "POR",
    "SAC",
    "SAS",
    "TOR",
    "UTA",
    "WAS",
}
byk = 0
# game_ids = game_ids[::-1]
for game_id in game_ids:
    if game_info_by_id[game_id]["TEAM_ABBREVIATION"] not in NBA_TEAMS:
        continue
    if game_id in udah:
        continue
    else:
        udah[game_id] = True
    try:
        byk += 1
        if byk == 200:
            time.sleep(60)
            byk = 0
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        players = boxscore.get_data_frames()[0].to_dict("records")
        # print(players)
        starters_by_team = {}
        num = defaultdict(int)
        num2 = defaultdict(int)
        for player in players:
            if player["START_POSITION"]:  # only starters
                team = player["TEAM_ABBREVIATION"]
                starters_by_team.setdefault(team, []).append(player["PLAYER_NAME"])

                if all_players[player["PLAYER_ID"]] <= 10:
                    num[team] += 1
                if all_players[player["PLAYER_ID"]] <= 16:
                    num2[team] += 1

        for team, starters in starters_by_team.items():
            if num[team] >= 3 and num2[team] == 5:
                game_info = game_info_by_id[game_id]
                matchup = game_info["MATCHUP"]
                game_date = game_info["GAME_DATE"]
                # print(team)
                # print(team2)
                # print(matchup)
                if " @ " in matchup:
                    visitor_abbr, home_abbr = matchup.split(" @ ")
                else:
                    home_abbr, visitor_abbr = matchup.split(" vs. ")
                game_date = game_info["GAME_DATE"]
                opponent = visitor_abbr if team == home_abbr else home_abbr
                is_home = team == home_abbr
                print(
                    {
                        "team": team,
                        "opponent": opponent,
                        "is_home": is_home,
                        "date": game_date,
                        "starters": starters,
                    },
                    end=",\n",
                )
                all_lineups.append(
                    {
                        "team": team,
                        "opponent": opponent,
                        "is_home": is_home,
                        "date": game_date,
                        "starters": starters,
                    }
                )

        time.sleep(1)

    except Exception as e:
        print(f"Error with {game_id}: {e}")

# for lineup in all_lineups:
#     print(lineup)


"""
"
{'game_id': '0022301187', 'team': 'CHA', 'starters': ['Bryce McGowens', 'JT Thor', 'Marques Bolden', 'Tre 
Mann', 'Vasilije Micić']}
{'game_id': '0022301187', 'team': 'CHA', 'starters': ['Bryce McGowens', 'JT Thor', 'Marques Bolden', 'Tre 
Mann', 'Vasilije Micić']}
{'game_id': '0022301186', 'team': 'WAS', 'starters': ['Johnny Davis', 'Patrick Baldwin Jr.', 'Anthony Gill', 'Deni Avdija', 'Corey Kispert']}
{'game_id': '0022301186', 'team': 'BOS', 'starters': ['Jordan Walsh', 'Sam Hauser', 'Luke Kornet', 'Svi Mykhailiuk', 'Payton Pritchard']}
{'game_id': '0022301198', 'team': 'UTA', 'starters': ['Taylor Hendricks', 'Luka Samanic', 'Omer Yurtseven', 'Keyonte George', 'Johnny Juzang']}
{'game_id': '0022301197', 'team': 'DET', 'starters': ['Troy Brown Jr.', 'Chimezie Metu', 'James Wiseman', 
'Jaden Ivey', 'Marcus Sasser']}
{'game_id': '0022301197', 'team': 'SAS', 'starters': ['Julian Champagnie', 'Sandro Mamukelashvili', 'Zach 
Collins', 'Blake Wesley', 'Tre Jones']}
{'game_id': '0022301197', 'team': 'DET', 'starters': ['Troy Brown Jr.', 'Chimezie Metu', 'James Wiseman', 
'Jaden Ivey', 'Marcus Sasser']}
{'game_id': '0022301197', 'team': 'SAS', 'starters': ['Julian Champagnie', 'Sandro Mamukelashvili', 'Zach 
Collins', 'Blake Wesley', 'Tre Jones']}
{'game_id': '0022301200', 'team': 'POR', 'starters': ['Justin Minaya', 'Kris Murray', 'Moses Brown', 'Rayan Rupert', 'Dalano Banton']}
{'game_id': '0022301196', 'team': 'DAL', 'starters': ['Josh Green', 'Olivier-Maxence Prosper', 'Dwight Powell', 'Tim Hardaway Jr.', 'Jaden Hardy']}
{'game_id': '0022301196', 'team': 'DAL', 'starters': ['Josh Green', 'Olivier-Maxence Prosper', 'Dwight Powell', 'Tim Hardaway Jr.', 'Jaden Hardy']}
{'game_id': '0022301200', 'team': 'POR', 'starters': ['Justin Minaya', 'Kris Murray', 'Moses Brown', 'Rayan Rupert', 'Dalano Banton']}
{'game_id': '0022301189', 'team': 'TOR', 'starters': ['Gradey Dick', 'Ochai Agbaji', 'Kelly Olynyk', 'Gary Trent Jr.', 'Javon Freeman-Liberty']}
{'game_id': '0022301189', 'team': 'TOR', 'starters': ['Gradey Dick', 'Ochai Agbaji', 'Kelly Olynyk', 'Gary Trent Jr.', 'Javon Freeman-Liberty']}
{'game_id': '0022301186', 'team': 'WAS', 'starters': ['Johnny Davis', 'Patrick Baldwin Jr.', 'Anthony Gill', 'Deni Avdija', 'Corey Kispert']}
{'game_id': '0022301186', 'team': 'BOS', 'starters': ['Jordan Walsh', 'Sam Hauser', 'Luke Kornet', 'Svi Mykhailiuk', 'Payton Pritchard']}
{'game_id': '0022301199', 'team': 'LAC', 'starters': ['Amir Coffey', 'P.J. Tucker', 'Mason Plumlee', 'Terance Mann', 'Xavier Moon']}
{'game_id': '0022301199', 'team': 'LAC', 'starters': ['Amir Coffey', 'P.J. Tucker', 'Mason Plumlee', 'Terance Mann', 'Xavier Moon']}
{'game_id': '0022301198', 'team': 'UTA', 'starters': ['Taylor Hendricks', 'Luka Samanic', 'Omer Yurtseven', 'Keyonte George', 'Johnny Juzang']}
{'game_id': '0022301173', 'team': 'CHA', 'starters': ['Brandon Miller', 'Miles Bridges', 'Marques Bolden', 'Tre Mann', 'Vasilije Micić']}
{'game_id': '0022301173', 'team': 'BOS', 'starters': ['Svi Mykhailiuk', 'Sam Hauser', 'Luke Kornet', 'Jaden Springer', 'Payton Pritchard']}
{'game_id': '0022301172', 'team': 'CHI', 'starters': ['Dalen Terry', 'Torrey Craig', 'Javonte Green', 'Onuralp Bitim', 'Coby White']}
{'game_id': '0022301172', 'team': 'WAS', 'starters': ['Johnny Davis', 'Patrick Baldwin Jr.', 'Tristan Vukcevic', 'Deni Avdija', 'Corey Kispert']}
{'game_id': '0022301180', 'team': 'SAS', 'starters': ['Julian Champagnie', 'Sandro Mamukelashvili', 'Victor Wembanyama', 'Blake Wesley', 'Tre Jones']}
{'game_id': '0022301183', 'team': 'POR', 'starters': ['Kris Murray', 'Jabari Walker', 'Deandre Ayton', 'Rayan Rupert', 'Scoot Henderson']}
{'game_id': '0022301181', 'team': 'DET', 'starters': ['Troy Brown Jr.', 'Chimezie Metu', 'James Wiseman', 
'Jaden Ivey', 'Marcus Sasser']}
{'game_id': '0022301184', 'team': 'UTA', 'starters': ['Luka Samanic', 'Taylor Hendricks', 'Omer Yurtseven', 'Johnny Juzang', 'Keyonte George']}
{'game_id': '0022301184', 'team': 'UTA', 'starters': ['Luka Samanic', 'Taylor Hendricks', 'Omer Yurtseven', 'Johnny Juzang', 'Keyonte George']}
{'game_id': '0022301180', 'team': 'SAS', 'starters': ['Julian Champagnie', 'Sandro Mamukelashvili', 'Victor Wembanyama', 'Blake Wesley', 'Tre Jones']}
{'game_id': '0022301172', 'team': 'CHI', 'starters': ['Dalen Terry', 'Torrey Craig', 'Javonte Green', 'Onuralp Bitim', 'Coby White']}
{'game_id': '0022301172', 'team': 'WAS', 'starters': ['Johnny Davis', 'Patrick Baldwin Jr.', 'Tristan Vukcevic', 'Deni Avdija', 'Corey Kispert']}
{'game_id': '0022301183', 'team': 'POR', 'starters': ['Kris Murray', 'Jabari Walker', 'Deandre Ayton', 'Rayan Rupert', 'Scoot Henderson']}
{'game_id': '0022301173', 'team': 'CHA', 'starters': ['Brandon Miller', 'Miles Bridges', 'Marques Bolden', 'Tre Mann', 'Vasilije Micić']}
{'game_id': '0022301173', 'team': 'BOS', 'starters': ['Svi Mykhailiuk', 'Sam Hauser', 'Luke Kornet', 'Jaden Springer', 'Payton Pritchard']}
"""
