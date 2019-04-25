import sys
import re
import pandas as pd

# IMPORTANT: There must be a file in the working directory titled:
# 'standings_wk*.txt' that is includes the copied text from the
# standings table in yahoo fantasy league view
# https://baseball.fantasysports.yahoo.com/b1/69542
# this script will clean and save that text to a dataframe,
# and then save to a file called 'standings_wk*_clean.csv'

def clean_standings(week):
    standings_dict = {}
    with open('data/standings_wk' + str(week) + '.txt') as f:
        s = f.read().split('\n')
        for item in s:
            standings = item.split('\t') 
            if re.match(r'[0-9]', standings[0]) != None:
                place = int(standings[0])
                team = standings[1].replace('logo ', '').replace("’", "'")
                team = team[:-1]  # remove space at end
                record = standings[2].split('-')
                record = tuple(int(x) for x in record)
                win_pct = float(standings[3])*100
                GB = standings[4]
                if GB == '- ':
                    GB = 0
                else:
                    GB = float(GB)
                moves = standings[7]
                if moves == '-':
                    moves = 0
                else:
                    moves = int(moves)
                standings_dict[team] = [place, record, win_pct, GB, moves]
    
    df_standings = pd.DataFrame.from_dict(standings_dict, orient='index')
    df_standings.columns = [
        'place', 'record', 'win_pct', 'games_back', 'moves'
    ]
    df_standings.index.name = 'team'
    fname = 'data/standings_wk' + str(week) + '_clean.csv'
    df_standings.to_csv(fname)
    return df_standings

if __name__ == '__main__':
    week = input('Week Number: ')
    df_standings = clean_standings(week)
    print(df_standings)
    fname = 'data/standings_wk' + str(week) + '_clean.csv'
    print('Saved as: ' + fname)
