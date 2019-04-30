"""You can run this to test your creds are ok."""

from hometown_homies import yahoo_api
import pandas as pd
from pandas.io.json import json_normalize
# import ipdb

sess = yahoo_api.get_session()

league_info = yahoo_api.get_league_info(sess)
league_name = league_info.json()['fantasy_content']['league'][0]['name']
print(f"Our league name is: {league_name}!!!")

standings_info = yahoo_api.get_league_standings(sess)
standings_dict = standings_info.json()
print("We got the standings but it's a big-ass dict.")

matchup_info = yahoo_api.get_league_matchup(sess)
matchup_dict = matchup_info.json()

team_info = yahoo_api.get_league_team(sess)
