# OAuth2 documentation found here:
# https://yahoo-oauth.readthedocs.io/en/latest/
from yahoo_oauth import OAuth2
# IPython Debugger
import ipdb
import pandas as pd
from pandas.io.json import json_normalize

class YahooFantasyAPI:

    def fetchGameID(self):
        session = self.getSession()
        url = 'http://fantasysports.yahooapis.com/fantasy/v2/leagues;league_key=mlb.l.69542'
        ses = session.get(url, params={'format': 'json'})
        # This appears to not be working...
        # May need to generate unique URL via yahoo commissioner settings
        # https://help.yahoo.com/kb/SLN6898.html
        ipdb.set_trace()
        print ses.text

    def getSession(self):
        oauth = OAuth2(None, None, from_file='./Authorization/oauth.json')

        if not oauth.token_is_valid():
            oauth.refresh_access_token()

        return oauth.session

# Initiate Class
ipdb.set_trace()
api = YahooFantasyAPI()
api.fetchGameID()
# Open a session

# ipdb.set_trace()
# data = json_normalize(r.json(), [['content']])
ipdb.set_trace()
pprint(r.json())
# Send a query to our league

