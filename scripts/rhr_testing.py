from hometown_homies import yahoo_api as ya

sess = ya.get_session()

print(ya.get_league_standings(sess))

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


team_stats_string = pp_dataframe(ya.get_team_stats(sess))
print('\n'+team_stats_string)