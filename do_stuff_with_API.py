from YahooSportsAPI import YahooSportsAPI
import ipdb
import pandas as pd
from pandas.io.json import json_normalize

# Initiate Class
api = YahooSportsAPI.YahooSportsAPI()

# Open a session
ses = api.getSession()

# Get League Info
league_url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/mlb.l.69542'
league_info = ses.get(league_url, params={'format': 'json'})
league_name = league_info.json()['fantasy_content']['league'][0]['name']

print "Our league name is: "+league_name+"!!!"

# Get League Standings
standings_url = "https://fantasysports.yahooapis.com/fantasy/v2/league/mlb.l.69542/standings"
standings_info = ses.get(standings_url, params={'format': 'json'})
# This a big ass dict...

# Get data in form of a Pandas DataFrame
# Need to disect the dictionary now
ipdb.set_trace()
data = json_normalize(standings_info.json(), [['fantasy_content', 'leagues', '0', 'league']])