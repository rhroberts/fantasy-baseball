import logging
mpl_logger = logging.getLogger('matplotlib') 
mpl_logger.setLevel(logging.WARNING) 
mpl_logger = logging.getLogger('matplotlib.dates') 
mpl_logger.setLevel(logging.WARNING) 
mpl_logger = logging.getLogger('matplotlib.ticker') 
mpl_logger.setLevel(logging.WARNING) 
from yahoo_oauth import OAuth2
import logging
oauth_logger = logging.getLogger('yahoo_oauth')
oauth_logger.disabled = True
from pathlib import Path
import pandas as pd
import numpy as np
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
    """Get dataframe of league standings from a Yahoo session object"""
    standings_info = session.get(
        LEAGUE_URL + 'league/' + LEAGUE_ID + \
        '/standings', params={'format': 'json'}
    ).json()
    # digging out the relevent standings information
    standings_dict = standings_info['fantasy_content']['league'][1]['standings'][0]['teams']
    
    current_standings = {}
    # keys are ['0', '1', ..., X', 'count'],
    # where '0'-'X' are the teams
    for key in standings_dict: 
        if key != 'count':
            team_info = standings_dict[key]['Team']
            team_name = team_info[0][2]['name']
            team_standings = team_info[2]['team_standings']

            # avoid type issues for '-' games back
            if team_standings['games_back'] == '-':
                team_standings['games_back'] = 0

            team_standings_clean = {
                'rank': int(team_standings['rank']),
                'record': tuple(
                    [
                        team_standings['outcome_totals']['wins'],
                        team_standings['outcome_totals']['losses'],
                        team_standings['outcome_totals']['ties']
                    ]
                ),
                'games_back': float(team_standings['games_back']),
                'win_rate': float(team_standings['outcome_totals']['percentage'])
            }
            current_standings[team_name] = team_standings_clean
    
    # put standings table into dataframe and sort by team rank
    standings_df = pd.DataFrame.from_dict(
        current_standings, orient='index'
    )        
    standings_df.sort_values('rank', inplace=True)
    standings_df.index.name = 'Team'
    
    return standings_df


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


def get_team_info(*arg):
    """Get basic team information from a Yahoo session object
    
    1. First argument is the sessions object for get_session().
    2. Second argument is a list of indices (or team names) to specify which teams to pull data for.
        1 = Lone Star Tallboys    = Rusty
        2 = Curt's American Made  = Curtis
        3 = Death By Smalls       = Tjos
        4 = Luke's Legit Team     = Luke
        5 = Hello World           = Marcus
        6 = Mookie and the Betts  = Peter
        7 = Soggy Dingers         = Cody W
        8 = Chuck Nazty           = Cody H
    3. If there is no second argument, returns a dataframe for all teams in the league.
    
    """
    
    # Split arguments
    if len(arg) > 1:
        teams = arg[1]
    else:
        teams = range(1,9)
    session = arg[0]
    
    # Get info from API
    team_info = session.get(LEAGUE_URL + 'league/' + LEAGUE_ID + '/teams', params={'format': 'json'})
    
    # Reformat info as dict
    team_dict = team_info.json()
    
    # Preallocate variables
    complete_dict = {}
    tmp_dict = []
    
    # Loop through each team in the dictionary
    for i in teams:
        team  = team_dict['fantasy_content']['league'][1]['teams'][str(i-1)]['team'][0]
        team = [x for x in team if x != []]
        team = {k: v for d in team for k, v in d.items()}
        tmp_dict.append(team)
    
    # Combine all dicts
    for team_dict in tmp_dict:
        # d = tmp_dict[key_td]
        team_name = team_dict['name']
        # deal with those pesky nested dicts
        for key in team_dict:
            if key == 'managers':
                team_dict[key] = team_dict[key][0]['manager']
            if key == 'team_logos':
                team_dict[key] = team_dict[key][0]['team_logo']
        complete_dict[team_name] = team_dict

    team_info_df = pd.DataFrame.from_dict(complete_dict)
    team_info_df.drop('name', axis=0, inplace=True)
    
    return team_info_df


def get_team_stats(session):
    """
        Get basic team stats (season to date) from a Yahoo session object
        Return a dataframe with info for all teams
    """

    # Preallocate variables
    team_stats_clean = {}

    # Map yahoo stat_id numbers to stat names
    stat_id_map = {
        '7': 'R',
        '12': 'HR',
        '13': 'RBI',
        '16': 'SB',
        '3': 'AVG',
        '50': 'IP',
        '28': 'W',
        '32': 'SV',
        '42': 'K',
        '26': 'ERA',
        '27': 'WHIP'
    }
    
    # Get info from API
    team_info = session.get(
        LEAGUE_URL + 'league/' + LEAGUE_ID + '/standings',
        params={'format': 'json'}
    )
    
    # Reformat info as dict
    team_dict = team_info.json()['fantasy_content']['league'][1]['standings'][0]
    team_dict = team_dict['Team']
    # keys are ['0', '1', ..., X', 'count'],
    # where '0'-'X' are the teams
    for team in team_dict: 
        if team != 'count':
            team_info = team_dict[team]['Team']
            team_name = team_info[0][2]['name']
            team_stats = team_info[1]['team_stats']['stats']
            tmp = {}
            for stat_dict in team_stats:
                s_id = stat_dict['stat']['stat_id']
                s_val = stat_dict['stat']['value']
                if s_id in stat_id_map:
                    tmp[stat_id_map[s_id]] = float(s_val)
            team_stats_clean[team_name] = tmp

    # convert to dataframe
    stats_df = pd.DataFrame.from_dict(team_stats_clean, orient='index')
    stats_df.index.name = 'Team'

    return stats_df


def get_team_averages(session,team):
    """Get statistical summary for a particular team
    Returns dataframe with statistics up to current week
    
    1. First argument is the sessions object for get_session().
    2. Second argument is the team_no.
        1 = Lone Star Tallboys    = Rusty
        2 = Curt's American Made  = Curtis
        3 = Death By Smalls       = Tjos
        4 = Luke's Legit Team     = Luke
        5 = Hello World           = Marcus
        6 = Mookie and the Betts  = Peter
        7 = Soggy Dingers         = Cody W
        8 = Chuck Nazty           = Cody H
    
    """
    
    # Get league info and grab current_week information
    league_df = get_league_info(session)
    current_week = league_df.loc['current_week','Value']
    
    # Get team information and grab team_key and team_name
    team_df = get_team_info(session)
    team_key = match_team_keys(team_df, [team])[0] # Interpret team variables
    team_name = team_df.columns.values[int(team_key[-1])-1]
    
    # Get standings information
    standings_df = get_league_standings(session)
    
    # Create list of weeks
    weeks = range(1,current_week)

    # Get matchup information
    matchup_df = get_league_matchup(session,team_key,weeks)

    # Predefine stat_dict
    stat_dict = {'H/AB*': [],
                 'R':     [],
                 'HR':    [],
                 'RBI':   [],
                 'SB':    [],
                 'AVG':   [],
                 'IP*':   [],
                 'W':     [],
                 'SV':    [],
                 'K':     [],
                 'ERA':   [],
                 'WHIP':  [],
                 'Points':[]}
    stat_key = list(stat_dict.keys())

    # Preallocate win counter
    wins_per_category = [0]*len(stat_key)

    # Loop through each weeks results and record stats. 
    # Count the number of wins per category
    for i in range(0,len(matchup_df)):
        for j in range(0,len(stat_key)):
            team_stat = matchup_df[i][stat_key[j]].iloc[0]
            if '*' in stat_key[j]:
                wins_per_category[j] = '-'
            else:
                opponent_stat = matchup_df[i][stat_key[j]].iloc[1]
                if team_stat > opponent_stat:
                    wins_per_category[j] += 1
            stat_dict[stat_key[j]].append(matchup_df[i][stat_key[j]].iloc[0])       

    # Loop through each stat and assign an average and win percentage
    for i in range(0,len(stat_key)):
        if 'H/AB*' in stat_key[i]:
            total_avg = np.average(stat_dict['AVG'])
            total_at_bats = [int(x.split('/')[1]) for x in stat_dict[stat_key[i]]]
            average_at_bats = np.average(total_at_bats)
            average_hits = int(total_avg*average_at_bats)
            stat_dict[stat_key[i]].append(str(average_hits)+'/'+str(int(average_at_bats)))
            stat_dict[stat_key[i]].append(wins_per_category[i])
            continue
        elif '*' in stat_key[i]:
            stat_dict[stat_key[i]].append(np.average(stat_dict[stat_key[i]]))
            stat_dict[stat_key[i]].append(wins_per_category[i])
            continue
        elif 'Points' in stat_key[i]:
            stat_dict[stat_key[i]].append(np.average(stat_dict[stat_key[i]]))
            stat_dict[stat_key[i]].append(standings_df.loc[team_name,'win_rate'])
            continue
        stat_dict[stat_key[i]].append(np.average(stat_dict[stat_key[i]]))
        stat_dict[stat_key[i]].append(wins_per_category[i]/float(len(weeks)))

    # Create row names from weeks
    indeces = []
    for i in weeks:
        indeces.append('Week '+str(i))
        
    # Add Average and Win %
    indeces.append('Average')
    indeces.append('Win %')
    stat_dict['Week'] = indeces
    stat_key.append('Week')

    # Combine dictionary into dataframe
    average_df = pd.DataFrame(stat_dict,columns=stat_key)
    average_df = average_df.set_index('Week')
    
    return average_df


def match_team_keys(team_info, team_list):
    """
        takes a list of full OR partial team names OR team indices and
        converts each respective item to it's unique yahoo team_key,
        returning a list of all matching keys
        Issues:
            - if partial name matches multiple team names
            no error occurs and first matching name will be used
    """
    # Editted to pass team_info dataframe into definition
    # team_info = get_team_info(session) 
    team_keys = []
    for team in team_list:
        if type(team) is int:
            # return team_key for respective team_id
            team_key = team_info.loc['team_key'][
                team_info.loc['team_id'] == str(team)
            ].values[0]
            team_keys.append(team_key)
        elif type(team) is str:
            # match partial team name to full team name
            for name in team_info.columns:
                if name.lower().find(team.lower()) != -1:
                    team = name
            # return team_key for respective team name
            team_key = team_info.loc['team_key'][
                team_info.columns == str(team)
            ].values[0]
            team_keys.append(team_key)
        else:
            print('Error: Team identifier not recognized!')
    
    return team_keys
