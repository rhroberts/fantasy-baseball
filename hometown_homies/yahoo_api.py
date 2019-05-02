from yahoo_oauth import OAuth2
from pathlib import Path
import pandas as pd
# import ipdb


LEAGUE_URL = 'https://fantasysports.yahooapis.com/fantasy/v2/'
LEAGUE_ID = 'mlb.l.69542'

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
    
    # Get info from API
    league_info = session.get(LEAGUE_URL + 'league/' + LEAGUE_ID, params={'format': 'json'})
    
    # Reformat info as dict
    league_dict = league_info.json()['fantasy_content']['league'][0]
    
    # Get dict keys
    k = list(league_dict.keys())
    
    # Preallocate dict and assign variables from keys
    complete_dict = {}
    complete_dict['Variable'] = k
    
    # Loop through dict and save results
    for i in range(0,len(league_dict)):
        complete_dict.setdefault('Value', []).append(league_dict[k[i]])
    
    # Combine dictionary into dataframe
    league_df = pd.DataFrame(complete_dict,columns=['Value','Variable'])
    league_df = league_df.set_index('Variable')
    
    return league_df

def get_league_standings(session):
    """Get leage standings from a Yahoo session object"""
    standings_info = session.get(LEAGUE_URL + 'league/' + LEAGUE_ID + '/standings', params={'format': 'json'})
    
    return standings_info

def get_league_matchup(session,team_key,weeks):
    """Get leage matchup from a Yahoo session object"""
    
    # Get URL with team_key and weeks
    url = LEAGUE_URL + 'team/' + LEAGUE_ID + team_key[-4:]+'/matchups;weeks='
    if len(weeks) > 1:
        for i in range(0,len(weeks)-1):
            url = url+str(weeks[i])+','
    url = url+str(weeks[-1])
    
    # Get info from API
    matchup_info = session.get(url, params={'format': 'json'})
    
    # Reformat info as dict
    matchup_dict = matchup_info.json()

    # Define stat key
    stat_key = ['H/AB*','R','HR','RBI','SB','AVG','IP*','W','SV','K','ERA','WHIP','Points']
    
    # Loop through each weeks
    matchup_df = []
    for i in range(0,len(weeks)):

        week_i_dict = matchup_dict['fantasy_content']['team'][1]['matchups'][str(i)]['matchup']
                
        # Parse team 1 information
        team_1_dict = {}
        team_1_info  = week_i_dict['0']['teams']['0']['team'][0]
        team_1_info = [x for x in team_1_info if x != []]
        team_1_info = {k: v for d in team_1_info for k, v in d.items()}
        team_1_name = team_1_info['name']
        team_1_dict['Team'] = team_1_name
        team_1_results = week_i_dict['0']['teams']['0']['team'][1]
        team_1_dict['Points'] = float(team_1_results['team_points']['total'])
        team_1_stats = team_1_results['team_stats']['stats']
        for j in range(0,len(stat_key)-1):
            stat_i = team_1_stats[j]['stat']['value']
            stat_name = stat_key[j]
            team_1_dict[stat_name] = stat_i
        
        # Parse team 2 information
        team_2_dict = {}
        team_2_info  = week_i_dict['0']['teams']['1']['team'][0]
        team_2_info = [x for x in team_2_info if x != []]
        team_2_info = {k: v for d in team_2_info for k, v in d.items()}
        team_2_name = team_2_info['name']
        team_2_dict['Team'] = team_2_name
        team_2_results = week_i_dict['0']['teams']['1']['team'][1]
        team_2_dict['Points'] = float(team_2_results['team_points']['total'])
        team_2_stats = team_2_results['team_stats']['stats']
        stats = []
        for j in range(0,len(stat_key)-1):
            stat_i = team_2_stats[j]['stat']['value']
            stat_name = stat_key[j]
            team_2_dict[stat_name] = stat_i
        
        # Combine team dicts
        complete_dict = {}
        combine_dict = [team_1_dict,team_2_dict]
        k = list(team_1_dict.keys())
        complete_dict['Team'] = [team_1_name,team_2_name]
        for j in range(0,len(combine_dict)):
            d = combine_dict[j]
            for h in range(0,len(stat_key)):
                if 'H/AB*' in stat_key[h]:
                    complete_dict.setdefault(stat_key[h], []).append(d[stat_key[h]])
                else:
                    complete_dict.setdefault(stat_key[h], []).append(float(d[stat_key[h]]))
        
        # Combine dictionary into dataframe
        tmp = stat_key + ['Team']
        week_i_df = pd.DataFrame(complete_dict,columns=tmp)
        week_i_df = week_i_df.set_index('Team')
        
        # Append dataframe
        matchup_df.append(week_i_df)

    return matchup_df

def get_league_team(*arg):
    """Get basic team information from a Yahoo session object
    
    1. First argument is the sessions object for get_session().
    2. Second argument is a list of indices (0-7) to specify which teams to pull data for.
        0 = Rusty
        1 = Curtis
        2 = Tjos
        3 = Luke
        4 = Marcus
        5 = Peter
        6 = Cody W
        7 = Cody H
    3. If there is no second argument, returns a dataframe for all teams in the league.
    
    """
    
    # Split arguments
    if len(arg) > 1:
        teams = arg[1]
    else:
        teams = range(0,8)
    session = arg[0]
    
    # Get info from API
    team_info = session.get(LEAGUE_URL + 'league/' + LEAGUE_ID + '/teams', params={'format': 'json'})
    
    # Reformat info as dict
    team_dict = team_info.json()
    
    # Preallocate variables
    complete_dict = {}
    tmp_dict = []
    
    # Name string associated with each team
    all_names = ['Rusty','Curtis','Tjos','Luke','Marcus','Peter','Cody W','Cody H']
    
    # Get reduced set of names
    names = [all_names[i] for i in teams]
    
    # Loop through each team in the dictionary
    for i in teams:
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