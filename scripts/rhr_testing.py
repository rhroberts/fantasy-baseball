from hometown_homies import yahoo_api as ya

sess = ya.get_session()

print(ya.get_league_matchup(sess, 'boys', [2,3]))
# print(ya.get_team_info(sess, [1]))
league_df, teams_df = ya.get_league_info(sess)

# print(ya.get_team_info(sess, 1))
# print(ya.get_team_averages(sess, 4))
# print(ya.match_team_keys(teams_df, 'lone'))

