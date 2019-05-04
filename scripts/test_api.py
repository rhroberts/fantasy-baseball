"""You can run this to test your creds are ok."""

from hometown_homies import yahoo_api
import pandas as pd
from pandas.io.json import json_normalize

sess = yahoo_api.get_session()

# Example usage for get_league_info()
league_info = yahoo_api.get_league_info(sess)
league_name = league_info.loc['name'].values[0]
print(f"Our league name is: {league_name}!!!")
print()

standings_df = yahoo_api.get_league_standings(sess)
print("Here's the current status of the league:")
print(standings_df)
print()

# Example usage for get_league_team()
team_info  = yahoo_api.get_team_info(sess,[0,1,2,3])  # Get team info for Rusty, Curtis, Tjos, and Luke
team_dmarc = yahoo_api.get_team_info(sess,[4])        # Get team info for Marcus only
team_info2 = yahoo_api.get_team_info(sess)            # Get team info for everyone

# Example usage for get_league_matchup()
team_key = team_dmarc.loc['team_key','Marcus']
weeks = [1,2,3,4,5]
matchup_info = yahoo_api.get_league_matchup(sess,team_key,weeks)

# Temporary print to visualize matchup_info
for i in range(0,len(matchup_info)):
    print(matchup_info[i])
    print()

# Example usage for calculating average weekly statistics
# 0 = Rusty
# 1 = Curtis
# 2 = Tjos
# 3 = Luke
# 4 = Marcus
# 5 = Peter
# 6 = Cody W
# 7 = Cody H
average_df = yahoo_api.get_team_averages(sess,0)
print("Statistical Summary for Rusty's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,1)
print("Statistical Summary for Curtis' Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,2)
print("Statistical Summary for Tjos' Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,3)
print("Statistical Summary for Luke's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,4)
print("Statistical Summary for Marcus' Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,5)
print("Statistical Summary for Peter's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,6)
print("Statistical Summary for Cody W's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,7)
print("Statistical Summary for Cody H's Team")
print(average_df)
print()

