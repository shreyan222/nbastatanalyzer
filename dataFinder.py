from bs4 import BeautifulSoup
import requests
def truncate_list_after_two_empty_elements(lst):

    for i in range(len(lst) - 1):
        if lst[i] == "" and lst[i + 1] == "":
            return lst[:i]  
    return lst
def against_team(team):
    html_text = requests.get(f'https://www.statmuse.com/nba/ask/what-team-are-the-{team}-playing-next').text
    soup = BeautifulSoup(html_text, 'lxml')
    opp = soup.find('span',
                    class_='my-[1em] [&>a]:underline [&>a]:text-team-secondary whitespace-pre-wrap text-pretty').text

    start_index = opp.find('@ ')
    if start_index != -1:
        start_index += 2 
    else:
        start_index = opp.find('vs ')
        if start_index != -1:
            start_index += 3  

    if start_index != -1:
        end_index = opp.find(' ', start_index)
        if end_index == -1:  
            end_index = len(opp)

        substring = opp[start_index:end_index].strip()

        if substring.upper() != "MIN":
            return substring
        else:
            return "minnesota"

    return None
def stats_against_team_t_season(name, team, timeframe):
    if team == "MIN":
        team = "Minesota"

    if name == "Nicolas Claxton":
        name = "Claxton"
    url = f'https://www.statmuse.com/nba/ask/{name}-against-{team}-{timeframe}'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find('table', class_='whitespace-nowrap w-full')
    stats = []
    if not table:
        return stats
    else:
        for row in table.find_all("tr"):
            cells = row.findAll("td")
            if cells == []:
                cells = row.find_all("th")
            for i in cells:
                stat = i.text
                stats.append(stat)
        final = truncate_list_after_two_empty_elements(stats)
    return final
def find_stat(num,arr):
    arr1 = []
    arr2 = []
    arr3 = []
    for i in range(28, len(arr)):
        if (i - num) % 28 == 0:
            arr1.append(arr[i])
    arr2 = [s.replace(" ", "") for s in arr1]
    arr3 = [int(x) for x in arr2]
    return arr3
def specific_stat_vs_opp_games_arr(arr,stat):



    arr1 = []
    arr3 = []
    'return list above'

    stat1 = []
    stat4 = []
    stat7 = []
    if stat == "Points":
        arr3 = find_stat(8, arr)
    elif stat == "Min":
        arr3 = find_stat(7, arr)
    elif stat == "Rebounds":
        arr3 = find_stat(9, arr)
    elif stat == "Assists":
        arr3 = find_stat(10, arr)
    elif stat == "Steals":
        arr3 = find_stat(11, arr)
    elif stat == "Blocked Shots":
        arr3 = find_stat(12, arr)
    elif stat == "Turnovers":
        arr3 = find_stat(25, arr)
    elif stat == "fgm":
        arr3 = find_stat(13, arr)
    elif stat == "FG Attempted":
        arr3 = find_stat(14, arr)
    elif stat == "3-PT Made":
        arr3 = find_stat(16, arr)
    elif stat == "3-PT Attempted":
        arr3 = find_stat(17, arr)
    elif stat == "Free Throws Made":
        arr3 = find_stat(19, arr)
    elif stat == "Offensive Rebounds":
        '''arr = stats_against_team_t_season_oreb(name, team)'''
        arr3 = find_stat(23, arr)
    elif stat == "Defensive Rebounds":
        '''arr = stats_against_team_t_season_dreb(name, team)'''
        arr3 = find_stat(24, arr)
    elif stat == "Pts+Rebs":
        stat3 = find_stat(8, arr)
        stat6 = find_stat(9, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Pts+Asts":
        stat3 = find_stat(8, arr)
        stat6 = find_stat(10, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Rebs+Asts":
        stat3 = find_stat(9, arr)
        stat6 = find_stat(10, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Blks+Stls":
        stat3 = find_stat(11, arr)
        stat6 = find_stat(12, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Pts+Rebs+Asts":
        stat3 = find_stat(8, arr)
        stat6 = find_stat(9, arr)
        stat9 = find_stat(10, arr)

        arr3 = [x + y + z for x, y, z in zip(stat3, stat6, stat9)]

    return arr3
def specific_stat_l10_games(arr,stat):




    arr1 = []
    arr3 = []
    'return list above'

    stat1 = []
    stat4 = []
    stat7 = []
    if stat == "Points":
        arr3 = find_stat(8, arr)
    elif stat == "Min":
        arr3 = find_stat(7, arr)
    elif stat == "Rebounds":
        arr3 = find_stat(9, arr)
    elif stat == "Assists":
        arr3 = find_stat(10, arr)
    elif stat == "Steals":
        arr3 = find_stat(11, arr)
    elif stat == "Blocked Shots":
        arr3 = find_stat(12, arr)
    elif stat == "Turnovers":
        arr3 = find_stat(25, arr)
    elif stat == "FG Made":
        arr3 = find_stat(13, arr)
    elif stat == "FG Attempted":
        arr3 = find_stat(14, arr)
    elif stat == "3-PT Made":
        arr3 = find_stat(16, arr)
    elif stat == "3-PT Attempted":
        arr3 = find_stat(17, arr)
    elif stat == "Free Throws Made":
        arr3 = find_stat(19, arr)
    elif stat == "Offensive Rebounds":
        '''arr = stats_against_team_t_season_oreb(name, team)'''
        arr3 = find_stat(23, arr)
    elif stat == "Defensive Rebounds":
        '''arr = stats_against_team_t_season_dreb(name, team)'''
        arr3 = find_stat(24, arr)
    elif stat == "Pts+Rebs":
        stat3 = find_stat(8, arr)
        stat6 = find_stat(9, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Pts+Asts":
        stat3 = find_stat(8, arr)
        stat6 = find_stat(10, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Rebs+Asts":
        stat3 = find_stat(9, arr)
        stat6 = find_stat(10, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Blks+Stls":
        stat3 = find_stat(11, arr)
        stat6 = find_stat(12, arr)
        arr3 = [x + y for x, y in zip(stat3, stat6)]
    elif stat == "Pts+Rebs+Asts":
        stat3 = find_stat(8, arr)
        stat6 = find_stat(9, arr)
        stat9 = find_stat(10, arr)

        arr3 = [x + y + z for x, y, z in zip(stat3, stat6, stat9)]

    return arr3

    if team == "MIN":
        team = "Minesota"
    html_text = requests.get(f'https://www.statmuse.com/nba/ask/{name}-against-{team}-{timeframe}').text
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find('table', class_='whitespace-nowrap w-full')
    stats = []
    if not table:
        return stats
    else:
        for row in table.find_all("tr"):
            cells = row.findAll("td")
            if cells == []:
                cells = row.find_all("th")
            for i in cells:
                stat = i.text
                stats.append(stat)
        final = truncate_list_after_two_empty_elements(stats)
    return final
def stats_ten_games(name):
    if name == "Nicolas Claxton":
        name = "Claxton"
    html_text = requests.get(f'https://www.statmuse.com/nba/ask/{name}-last-10-games').text
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find('table', class_='whitespace-nowrap w-full')
    stats = []
    if not table:
        return stats
    else:
        for row in table.find_all("tr"):
            cells = row.findAll("td")
            if cells == []:
                cells = row.find_all("th")
            for i in cells:
                stat = i.text
                stats.append(stat)
        final = truncate_list_after_two_empty_elements(stats)
    return final
