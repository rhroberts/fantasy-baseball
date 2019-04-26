from YahooSportsAPI import YahooSportsAPI
import pandas as pd
from pandas.io.json import json_normalize
import ipdb

# Initiate Class
api = YahooSportsAPI.YahooSportsAPI()

# Open a session
ses = api.getSession()

# Get League Info
league_info = api.getLeagueInfo(ses)
league_name = league_info.json()['fantasy_content']['league'][0]['name']
print "Our league name is: "+league_name+"!!!"

# Get League Standings
standings_info = api.getLeagueStandings(ses)
# This a big ass dict...

# Get data in form of a Pandas DataFrame
# Need to disect the dictionary now
ipdb.set_trace()
data = json_normalize(standings_info.json(), [['fantasy_content', 'leagues', '0', 'league']])