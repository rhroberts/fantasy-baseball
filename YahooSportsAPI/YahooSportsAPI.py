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
        oauth = OAuth2(None, None, from_file='./Authorization/oauth.json')

        if not oauth.token_is_valid():
            oauth.refresh_access_token()

        return oauth.session