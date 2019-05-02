"""You can run this to test your creds are ok."""

from hometown_homies import yahoo_api
import pandas as pd
from pandas.io.json import json_normalize
# import ipdb

sess = yahoo_api.get_session()

# Example usage for get_league_info()
league_info = yahoo_api.get_league_info(sess)
league_name = league_info.loc['name'].values[0]
print(f"Our league name is: {league_name}!!!")

standings_info = yahoo_api.get_league_standings(sess)
standings_dict = standings_info.json()
print("We got the standings but it's a big-ass dict.")

# Example usage for get_league_team()
team_info  = yahoo_api.get_league_team(sess,[0,1,2,3])  # Get team info for Rusty, Curtis, Tjos, and Luke
team_dmarc = yahoo_api.get_league_team(sess,[4])        # Get team info for Marcus only
team_info2 = yahoo_api.get_league_team(sess)            # Get team info for everyone

# Example usage for get_league_matchup()
team_key = team_dmarc.loc['team_key','Marcus']
weeks = [1,2,3,4,5]
matchup_info = yahoo_api.get_league_matchup(sess,team_key,weeks)

# Temporary print to visualize matchup_info
print()
for i in range(0,len(matchup_info)):
    print(matchup_info[i])
    print()
    print()
