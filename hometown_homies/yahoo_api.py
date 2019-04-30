from yahoo_oauth import OAuth2
from pathlib import Path
import pandas as pd


LEAGUE_URL = 'https://fantasysports.yahooapis.com/fantasy/v2/league/mlb.l.69542'

def get_session(auth_file=None):
    """Get a valid yahoo session object"""

    if auth_file is None:
        auth_file = Path.home() / '.yahoo_oauth.json'

    oauth = OAuth2(None, None, from_file=auth_file)

    if not oauth.token_is_valid():
        oauth.refresh_access_token()

    return oauth.session

def get_league_info(session):
    """Get league info from a Yahoo session object"""
    league_info = session.get(LEAGUE_URL, params={'format': 'json'})
    
    return league_info

def get_league_standings(session):
    """Get leage standings from a Yahoo session object"""
    standings_info = session.get(LEAGUE_URL + '/standings', params={'format': 'json'})
    
    return standings_info

def get_league_matchup(session):
    """Get leage matchup from a Yahoo session object"""
    matchup_info = session.get(LEAGUE_URL + '/matchup', params={'format': 'json'})
    
    return matchup_info

def get_league_team(session):
    """Get leage matchup from a Yahoo session object"""
    team_info = session.get(LEAGUE_URL + '/teams', params={'format': 'json'})
    
    # Get info as dict
    team_dict = team_info.json()
    
    # Preallocate variables
    complete_dict = {}
    tmp_dict = []
    
    # Name string associated with each team
    names = ['Rusty','Curtis','Tjos','Luke','Marcus','Peter','Cody W','Cody H']
    
    # Loop through each team in the dictionary
    for i in range(0,len(names)):
        team  = team_dict['fantasy_content']['league'][1]['teams'][str(i)]['team'][0]
        team = [x for x in team if x != []]
        team = {k: v for d in team for k, v in d.items()}
        tmp_dict.append(team)
    
    # Combine all dicts
    skip = ['managers','roster_adds','team_logos','is_owned_by_current_login']
    for j in range(0,len(tmp_dict)):
        d = tmp_dict[j]
        name = names[j]
        k = list(d.keys())
        if j == 0:
            k_tmp = [x for i, x in enumerate(k) if x not in skip]
            complete_dict['Variable'] = k_tmp
        for i in range(0,len(d)):
            if k[i] in skip:
                continue
            complete_dict.setdefault(name, []).append(d[k[i]])
    
    # Append Variable to names
    names.append('Variable')
    
    # Combine dictionary into dataframe
    team_df = pd.DataFrame(complete_dict,columns=names)
    team_df = team_df.set_index('Variable')
    
    return team_df