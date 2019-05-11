"""Script to print out team statistics vs. current opponent statistics"""

# Suppress logging in what is a bad way, I assume. 
import logging
oauth_logger = logging.getLogger('matplotlib')
oauth_logger.disabled = True

from hometown_homies import yahoo_api
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import ipdb

def bcolors(k):
    if k == 0:
        return '\033[34m'       # Blue
    elif k == 1:
        return '\033[32m'       # Green
    elif k == 2:
        return '\033[31m'       # Red
    elif k == 3:
        return '\033[36m'       # Cyan
    elif k == 4:
        return '\033[95m'       # Purple
    elif k == 5:
        return '\033[35m'       # Magenta
    elif k == 6:
        return '\033[93m'       # Yellow
    elif k == 7:
        return '\033[33m'       # Orange
    elif k == 'end':
        return '\033[0m'        # End format
    elif k == 100:
        return '\033[33;1;4m'   # Yellow + underlined
    elif k == 101:
        return '\033[1m'        # Bold
    elif k == 102:
        return '\033[4m'        # Underlined
    
def pp_dataframe(df):
    # Convert dataframe to string and split by line
    df_string = df.to_string().split('\n')
    # Split header line by space
    header = df_string[0].split()
    index_header = df_string[1]
    # Get index of all stats not counted in score
    ind = ['*' in head for head in header]
    # Loop through rest of dataframe
    data = []
    max_team = 0
    for i in range(2,len(df_string)):
        # Split line by space
        line = df_string[i].split()
        # Join team names into single index
        delta = len(line)-len(header)
        line[0] = ' '.join(line[0:delta])
        del line[1:delta]
        # Record max length of team name
        if max_team < len(line[0]):
            max_team = len(line[0])
        # Append to data
        data.append(line)
    
    # Initialize win counter
    win_i = [0]*len(header)
    tmp = []
    wid = 7
    min = ['ERA','WHIP']
    for i in range(0,len(header)):
        if header[i] in min:
            # header[i] = header[i].rjust(len(header[i])+2)
            header[i] = header[i].rjust(wid)
            tmp.append(1000)
        else:
            # header[i] = header[i].rjust(len(header[i])+2)
            header[i] = header[i].rjust(wid)
            tmp.append(0)
    
    # Loop through data and determine line of max/min
    min = ['ERA'.rjust(wid),'WHIP'.rjust(wid)]
    for i in range(0,len(header)):
        for j in range(0,len(data)):
            if ind[i]:
                continue
            elif header[i] in min and tmp[i] > float(data[j][i+1]):
                tmp[i] = float(data[j][i+1])
                win_i[i] = j+1
            elif header[i] not in min and tmp[i] < float(data[j][i+1]):
                tmp[i] = float(data[j][i+1])
                win_i[i] = j+1
            elif tmp[i] == float(data[j][i+1]):
                tmp[i] = float(data[j][i+1])
                win_i[i] = 0

    leng = []
    header = [''.ljust(max_team)]+header
    final_string = [bcolors(102)+''.join(header)+'\n'+bcolors('end'),df_string[1]+'\n']
    for i in range(0,len(data)):
        tmp = []
        for j in range(1,len(data[i])):
            if win_i[j-1] == 0:
                data[i][j] = data[i][j].rjust(len(header[j]))
                # data[i][j] = data[i][j].rjust(8)
                continue
            elif win_i[j-1] == i+1:
                if 'HR' in header[j]:
                    data[i][j] = bcolors(i)+data[i][j].rjust(len(header[j]))+bcolors('end')
                else:
                    data[i][j] = bcolors(100)+data[i][j].rjust(len(header[j]))+bcolors('end')
            else:
                data[i][j] = data[i][j].rjust(len(header[j]))
        data[i][0] = bcolors(i)+data[i][0].ljust(max_team)+bcolors('end')
        final_string.append(''.join(data[i])+'\n')
    
    final_string = ''.join(final_string)
    
    return final_string
    

""" MAIN """

# Select team to run script on
# team = 1 # 1 = Lone Star Tallboys    = Rusty
# team = 2 # 2 = Curt's American Made  = Curtis
# team = 3 # 3 = Death By Smalls       = Tjos
team = 4 # 4 = Luke's Legit Team     = Luke
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
matchup_df = pp_dataframe(matchup_df)

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
average_df = pp_dataframe(average_df)

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
print(f"\n{bcolors(0)}{team_name}{bcolors('end')} ({team_standing}) vs. {bcolors(1)}{opponent_name}{bcolors('end')} ({opponent_standing})\n")
print(f"Average Statistics:\n\n{average_df}\n")
print(f"Current Standings:\n\n{matchup_df}\n")


# print(matchup_df)
