from hometown_homies import yahoo_api as ya

sess = ya.get_session()

tk = ya.match_team_keys(sess, ['boys'])

print(ya.get_league_matchup(sess, 'boys', 4))
