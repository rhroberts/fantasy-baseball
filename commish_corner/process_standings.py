import pandas as pd
import numpy as np
import os
from natsort import natsorted
import clean_standings as cs

def manual_info():
    '''
    manual_info() takes no arguments.
    It will prompt the user for info that can't be gleaned
    from standings_wk*_clean.csv 
    Returns an interger week number and dictionary with each team's
    total match wins.
    '''

    current_week = int(input('Week Number: '))
    match_wins = {}
    team_list = [
        'Soggy Dingers',
        "Curt's American Made",
        "Luke's Legit Team",
        "Hello World",
        "Mookie and the Betts",
        "Chuck Nazty",
        "Lone Star Tallboys",
        "Death By Smalls"
    ]
    for team in team_list:
        match_wins[team] = int(input('Total match wins for ' + team + ': '))
    return(current_week, match_wins)


def get_match_wins():
    mw = pd.read_csv('data/match_wins.csv', index_col=0, header=None)
    match_wins = {}
    for i, row in mw.iterrows():
        match_wins[i] = row[1]
    return match_wins


def process_standings(current_week):
    '''
    process_standings() takes one argument:

    1. current_week (int)
        - Current week of fantasy baseball season (or older week for snapshot)

    Returns two Pandas DataFrames:

    1. current_standings
        - Relevant team info cumulative up to current_week
    2. games_back
        - Tracking how many games back in the standings a team is for each week
    '''

    weeks = np.arange(0, 14)
    weeks = [str(wk) for wk in weeks]
    week_names = ['Week ' + wk for wk in weeks]
    
    weekly_standings = {}
    # clean the data pulled from yahoo as export to csv
    for wk in weeks:
        fname = 'standings_wk' + wk + '.txt'
        if fname in os.listdir('data/'):
            cs.clean_standings(wk)
    
    for wk in weeks:
        fname = 'standings_wk' + wk + '_clean.csv'
        if fname in os.listdir('data/'):
            print("Importing '" + fname + "' ...")
            df = pd.read_csv('data/' + fname)
            weekly_standings['Week ' + wk] = df
    
    print('Done.\n')
    
    current_standings = weekly_standings['Week ' + str(current_week)]
    
    games_back = pd.DataFrame(
        data=None, columns=week_names, index=current_standings.index
    )
    games_back['Week 0'] = 0 
    col_ord = natsorted(games_back.columns)
    games_back = games_back[col_ord]
    games_back.index = current_standings['team']
    games_back = games_back.sort_values(games_back.columns[current_week], ascending=True)
    
    for wk in weekly_standings:
        tmp = pd.DataFrame(
            [weekly_standings[wk]['team'], weekly_standings[wk]['games_back']]
        )
        tmp = tmp.transpose()
        tmp.index = tmp['team']
        games_back[wk] = tmp['games_back']
    

    # add in money stuff
    prize_structure = {
        1: 96,
        2: 32,
        3: 24,
        4: 8,
        5: 0,
        6: 0,
        7: 0,
        8: 0
    }
    match_wins = get_match_wins()
    match_wins = pd.DataFrame.from_dict(
        match_wins, orient='index', columns=['match_wins']
    )
    match_wins['team'] = match_wins.index
    match_wins.index = current_standings.index
    current_standings = pd.merge(current_standings, match_wins, on='team')
    prize_structure = pd.DataFrame.from_dict(prize_structure, orient='index', columns=['prize_money'])
    prize_structure['place'] = prize_structure.index
    prize_structure.index = range(0, len(prize_structure.index))
    current_standings = pd.merge(current_standings, prize_structure, on='place')
    current_standings['weekly_money'] = current_standings['match_wins']*2 - (current_week - current_standings['match_wins'])
    current_standings['total_money'] = current_standings['prize_money'] + current_standings['weekly_money']
    current_standings['net_money'] = current_standings['total_money'] - 20
    return(current_standings, games_back)

if __name__ == '__main__':
    # will need to update this manually every week
    current_week = 2
    mw = pd.read_csv('data/match_wins.csv', index_col=0)
    match_wins = {}
    for i, row in mw.iterrows():
        match_wins[i] = row[0]
    current_standings, games_back = process_standings(current_week)
    print(current_standings)
    print(games_back)
