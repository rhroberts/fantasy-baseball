"""You can run this to test your creds are ok."""

# Suppress logging in what is a bad way, I assume. 
import logging
oauth_logger = logging.getLogger('matplotlib')
oauth_logger.disabled = True

from hometown_homies import yahoo_api
import pandas as pd
from pandas.io.json import json_normalize

sess = yahoo_api.get_session()

# Example usage for get_league_info()
league_info, team_info = yahoo_api.get_league_info(sess)
league_name = league_info.loc['name'].values[0]
print(f"Our league name is: {league_name}!!!")
print()

standings_df = yahoo_api.get_league_standings(sess)
print("Here's the current status of the league:")
print(standings_df)
print()

# Example usage for get_team_info()
team_info  = yahoo_api.get_team_info(sess,[1,2,3,4])  # Get team info for Rusty, Curtis, Tjos, and Luke
team_dmarc = yahoo_api.get_team_info(sess,[5])        # Get team info for Marcus only
team_info2 = yahoo_api.get_team_info(sess)            # Get team info for everyone

# Example usage for get_league_matchup()
team = 'Hello World'
weeks = [1,2,3,4,5]
matchup_info = yahoo_api.get_league_matchup(sess,team,weeks)

# Temporary print to visualize matchup_info
for i in range(0,len(matchup_info)):
    print(matchup_info[i])
    print()

# Example usage for calculating average weekly statistics
# 1 = Lone Star Tallboys    = Rusty
# 2 = Curt's American Made  = Curtis
# 3 = Death By Smalls       = Tjos
# 4 = Luke's Legit Team     = Luke
# 5 = Hello World           = Marcus
# 6 = Mookie and the Betts  = Peter
# 7 = Soggy Dingers         = Cody W
# 8 = Chuck Nazty           = Cody H
average_df = yahoo_api.get_team_averages(sess,1)
print("Statistical Summary for Rusty's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,'American ')
print("Statistical Summary for Curtis' Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,3)
print("Statistical Summary for Tjos' Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,'Legit')
print("Statistical Summary for Luke's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,'Hello World')
print("Statistical Summary for Marcus' Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,6)
print("Statistical Summary for Peter's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,7)
print("Statistical Summary for Cody W's Team")
print(average_df)
print()

average_df = yahoo_api.get_team_averages(sess,'Nazty')
print("Statistical Summary for Cody H's Team")
print(average_df)
print()

