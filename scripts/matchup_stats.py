"""Script to print out team statistics vs. current opponent statistics"""
from hometown_homies import yahoo_api
import pandas as pd

def highlight_winner(df):
    # Highlight the winning team per category yellow.
    stats = df.columns.values.tolist()
    names = df.index.tolist()
    team = df.loc[names[0]].values.tolist()
    opponent = df.loc[names[1]].values.tolist()
    team_win = []
    opponent_win = []
    for i in range(0,len(stats)):
        if '*' in stats[i]:
            team_win.append(False)
            opponent_win.append(False)
            continue
        elif 'ERA' in stats[i] or 'WHIP' in stats[i]:
            if team[i] < opponent[i]:
                team_win.append(True)
                opponent_win.append(False)
            else:
                team_win.append(False)
                opponent_win.append(True)
        else:
            if team[i] > opponent[i]:
                team_win.append(True)
                opponent_win.append(False)
            else:
                team_win.append(False)
                opponent_win.append(True)

    ipdb.set_trace()
    ['background-color: yellow' if v else '' for v in team_win]
    return 

def highlight_max(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]
    
def highlight_min(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    is_min = s == s.min()
    return ['background-color: yellow' if v else '' for v in is_min]

""" MAIN """

# Select team to run script on
team = 1 # 1 = Lone Star Tallboys    = Rusty
# team = 2 # 2 = Curt's American Made  = Curtis
# team = 3 # 3 = Death By Smalls       = Tjos
# team = 4 # 4 = Luke's Legit Team     = Luke
# team = 5 # 5 = Hello World           = Marcus
# team = 6 # 6 = Mookie and the Betts  = Peter
# team = 7 # 7 = Soggy Dingers         = Cody W
# team = 8 # 8 = Chuck Nazty           = Cody H

# Get session object
sess = yahoo_api.get_session()

# Get league info and current_week
league_df = yahoo_api.get_league_info(sess)
current_week = [league_df.loc['current_week','Value']]

# Get team_name and team_key
team_df = yahoo_api.get_team_info(sess)
team_key = yahoo_api.match_team_keys(team_df, [team])[0]

# Get current week matchup for team_name
matchup_df = yahoo_api.get_league_matchup(sess,team_key,current_week)[0]
team_name = matchup_df.index.tolist()[0]
opponent_name = matchup_df.index.tolist()[1]
# matchup_df = highlight_winner(matchup_df)
# matchup_df.style.apply(highlight_max)

# Get standings info
standings_df = yahoo_api.get_league_standings(sess)
team_standing = standings_df['rank'].values[standings_df.index == team_name][0]
opponent_standing = standings_df['rank'].values[standings_df.index == opponent_name][0]

# Get team average stats
team_average_df     = yahoo_api.get_team_averages(sess,team)
opponent_average_df = yahoo_api.get_team_averages(sess,opponent_name)
team_average     = list(team_average_df.loc['Average'].values)
opponent_average = list(opponent_average_df.loc['Average'].values)
# Predefine average_dict
average_dict = {'H/AB*': [],
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
                'Points':[],
                'Team':  [team_name,opponent_name]}
columns = list(average_dict.keys())
for i in range(0,len(columns)-1):
    average_dict[columns[i]].append(team_average[i])
    average_dict[columns[i]].append(opponent_average[i])

# Combine into dataframe
average_df = pd.DataFrame(average_dict,columns=columns)
average_df = average_df.set_index('Team')

# Print results
dict_style = {'H/AB*':    "{:,.3f}",
              'R':        "{:,.1f}",
              'HR':       "{:,.1f}",
              'RBI':      "{:,.1f}",
              'SB':       "{:,.1f}",
              'AVG':      "{:,.3f}",
              'IP*':      "{:,.1f}",
              'W':        "{:,.1f}",
              'SV':       "{:,.1f}",
              'K':        "{:,.1f}",
              'ERA':      "{:,.3f}",
              'WHIP':     "{:,.3f}",
              'Points':   "{:,.1f}"}
print(f"\n{team_name} ({team_standing}) vs. {opponent_name} ({opponent_standing})\n")
average_df.style.format(dict_style)
average_df.style.apply(highlight_max, subset=['R','HR','RBI','SB','AVG','W','SV','K','Points'])
average_df.style.apply(highlight_min, subset=['ERA','WHIP'])
print('Average Statistics:')
print(average_df)
matchup_df.style.format(dict_style)
matchup_df.style.apply(highlight_max, subset=['R','HR','RBI','SB','AVG','W','SV','K','Points'])
matchup_df.style.apply(highlight_min, subset=['ERA','WHIP'])
print('Current Standings:')
print(matchup_df)
