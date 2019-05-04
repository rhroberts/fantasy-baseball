from hometown_homies import yahoo_api as ya

sess = ya.get_session()

print(ya.get_league_standings(sess))
