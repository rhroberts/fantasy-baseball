from hometown_homies import yahoo_api


session = yahoo_api.get_session()

team_key_list = yahoo_api.match_team_keys(session, [3, 'Legit', 7, 'Tall'])
print(team_key_list)
