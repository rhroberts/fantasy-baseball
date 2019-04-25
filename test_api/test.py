# trying to access the yahoo api
from rauth import OAuth1Service
import json

auth_key = 'YOURAUTHKEY'
auth_secret = 'YOURAUTHSECRET'

def new_decoder(payload):
    return json.loads(payload.decode('utf-8'))

yahoo = OAuth1Service(
    name='yahoo',
    consumer_key=auth_key,
    consumer_secret=auth_secret,
    request_token_url='https://api.login.yahoo.com/oauth/v2/get_request_token',
    authorize_url='https://api.login.yahoo.com/oauth/v2/request_auth',
    access_token_url='https://api.login.yahoo.com/oauth/v2/get_token',
    base_url='http://fantasysports.yahooapis.com/'
)

request_token = yahoo.get_request_token(decoder=new_decoder)
