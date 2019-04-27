from yahoo_oauth import OAuth2
from pathlib import Path


LEAGUE_URL = 'https://fantasysports.yahooapis.com/fantasy/v2/league/mlb.l.69542'

def get_session():
    """Get a valid yahoo session object"""

    oauth = OAuth2(None, None, from_file=Path.home() / '.yahoo_oauth.json')

    if not oauth.token_is_valid():
        oauth.refresh_access_token()

    return oauth.session

def get_league_info(session):
    """Get league info from a Yahoo session object"""
    league_info = session.get(LEAGUE_URL, params={'format': 'json'})
    
    return league_info

def getLeagueStandings(session):
    """Get leage standings from a Yahoo session object"""

    standings_info = session.get(LEAGUE_URL + '/standings', params={'format': 'json'})
    
    return standings_info