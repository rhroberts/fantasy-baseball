# Author:   Marcus Bakke

from yahoo_oauth import OAuth2
import ipdb
import pandas as pd
from pandas.io.json import json_normalize

class YahooFantasyAPI:

    def getSession(self):
        oauth = OAuth2(None, None, from_file='./Authorization/oauth.json')

        if not oauth.token_is_valid():
            oauth.refresh_access_token()

        return oauth.session

# Initiate Class
api = YahooFantasyAPI()

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

