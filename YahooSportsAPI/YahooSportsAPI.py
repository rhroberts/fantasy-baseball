#
# Author:   Marcus Bakke
#
# Description:  This file defines a class variable which is used 
#               to initialize Yahoo Sports API authorization.
#
# oauth.json:   User must create an app via the Yahoo Developer
#               Network here:  https://developer.yahoo.com/apps/
#               Once the app is created, the user must create
#               an oauth.json file with the following format:
#
#               {
#                   "consumer_key": "Your Key Here", 
#                   "consumer_secret": "Your Secret Here", 
#               }
#
#               This oauth.json file should be within a folder
#               named Authorization in the root directory.
#
from yahoo_oauth import OAuth2

class YahooSportsAPI:

    def getSession(self):
        # Open Yahoo API Session
        oauth = OAuth2(None, None, from_file='./Authorization/oauth.json')

        if not oauth.token_is_valid():
            oauth.refresh_access_token()

        return oauth.session
        
    def getLeagueInfo(self,session):
        # session = self.getSession()
        # Get League Info
        league_url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/mlb.l.69542'
        league_info = session.get(league_url, params={'format': 'json'})
        
        return league_info
        
    def getLeagueStandings(self,session):
        # session = self.getSession()
        # Get League Standings
        standings_url = "https://fantasysports.yahooapis.com/fantasy/v2/league/mlb.l.69542/standings"
        standings_info = session.get(standings_url, params={'format': 'json'})
        
        return standings_info