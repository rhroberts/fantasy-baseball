# Given a user specified week#, plot_standings.py will look for
# csv files (standings_wk*_clean.csv) and plot the weekly standings
# of the hometown homies fantasy league
# NOTE: currently this only works for the most current week
# i.e., trying to plot previous weeks doesn't place the team logos
# corretly -- need to fix this

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.patches as patches
import process_standings as ps

current_week = int(input('Current Week: '))
current_standings, games_back = ps.process_standings(current_week)
# add plot color to dataframe
mbool = current_standings['net_money'] > 0
current_standings['color'] = 'k' 
current_standings['color'][mbool] = 'g'
current_standings['color'][~mbool] = 'r'
print(current_standings)
print(games_back)

sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(9,6), dpi=300)

for i, team in enumerate(games_back.index):
    x = games_back.columns
    x_int = [int(wk.replace('Week ', '')) for wk in x]
    y = games_back.loc[team]
    asp = 1
    rng = 0.4
    # zorder by team place
    zo = len(current_standings.index) - current_standings['place'].loc[i] + 3
    # import team logo
    image = plt.imread('logos/' + team.replace("'","") + '.png')

    # offset labels/logos if two teams have the same win %
    try:
        if games_back.iloc[i,current_week] == games_back.iloc[i+1,current_week]:
            s = 0.4  # shift image in x
            stx = 1  # shift text in x
            sty = 0.25  # shift teyt in y
            im = ax.imshow(
                image, aspect=asp,
                extent=(
                    x_int[current_week]-rng*asp+s,
                    x_int[current_week]+rng*asp+s,
                    y[current_week]+rng*asp,
                    y[current_week]-rng*asp
                ),
                zorder=zo+8,
            )
            patch = patches.Ellipse(
                (
                    x_int[current_week]+s,y[current_week]
                ), width=0.75, height=0.75, transform=ax.transData
            )
            im.set_clip_path(patch)
            ax.autoscale(False)
            ax.text(
                x_int[current_week+1], y[current_week]-sty,
                team + ' ($' + str(current_standings['net_money'].loc[i]) + ')',
                color=current_standings['color'].loc[i]
            )
            # shift last x-val with image plot line plot after try/except block
            x_int[current_week] = x_int[current_week] + s
        else:
            s = 0  # shift image
            im = ax.imshow(
                image, aspect=asp,
                extent=(
                    x_int[current_week]-rng*asp-s,
                    x_int[current_week]+rng*asp-s,
                    y[current_week]+rng*asp,
                    y[current_week]-rng*asp
                ),
                zorder=zo+8
            )
            patch = patches.Ellipse((x_int[current_week]-s,y[current_week]), width=0.75, height=0.75, transform=ax.transData)
            im.set_clip_path(patch)
            ax.autoscale(False)
            ax.text(
                x_int[current_week]+stx, y[current_week],
                team + ' ($' + str(current_standings['net_money'].loc[i]) + ')',
                color=current_standings['color'].loc[i]
            )
    except:
        # for the case where i+current_week is out of bounds
            s = 0  # shift image
            im = ax.imshow(
                image, aspect=asp,
                extent=(
                    x_int[current_week]-rng*asp-s,
                    x_int[current_week]+rng*asp-s,
                    y[current_week]+rng*asp,
                    y[current_week]-rng*asp
                ),
                zorder=zo+8,
            )
            patch = patches.Ellipse((x_int[current_week]-s,y[current_week]), width=0.75, height=0.75, transform=ax.transData)
            im.set_clip_path(patch)
            ax.autoscale(False)
            ax.text(
                x_int[current_week+1], y[current_week],
                team + ' ($' + str(current_standings['net_money'].loc[i]) + ')',
                color=current_standings['color'].loc[i]
            )

    # get most common color from logo for line plot
    rgbs = np.concatenate((image[0], image[1], image[2]))
    rgb = stats.mode(rgbs)[0][0]
    # plot line of games_back data
    ax.plot(x_int, y, linewidth=4, c=rgb, zorder=zo)

ax.set_xticks(np.arange(0,14))
ax.set_xticklabels(games_back.columns)
ax.set_ylabel('Win %')
ax.set_ylabel('Games Back')
ax.set_title('Hardball Homies: Week ' + str(current_week))
ax.set_ylim([8.5, -0.75])
plt.xticks(rotation=50)
fig.tight_layout()
fig.savefig('graphs/week' + str(current_week) + '.png', dpi=300)
