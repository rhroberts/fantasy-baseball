#
# Author:   Marcus Bakke
#
# Description:  This file defines a class variable which is used 
#               to initialize Yahoo Sports API authorization.
#
from yahoo_oauth import OAuth2

class YahooSportsAPI:

    def getSession(self):
        oauth = OAuth2(None, None, from_file='./Authorization/oauth.json')

        if not oauth.token_is_valid():
            oauth.refresh_access_token()

        return oauth.session