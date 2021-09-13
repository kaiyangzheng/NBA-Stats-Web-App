"""
Description:
Web scrapes NBA statistics and turns them into usable data
"""
from re import I, S
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import nba_api
from nba_api.stats.static import players
from nba_api.stats.static import teams

#web scrapes list of all players 
def gen_player_list(season):
    html_text = urlopen(f'https://www.basketball-reference.com/leagues/NBA_{season}_per_game.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "per_game_stats"})
    df = pd.read_html(str(table))
    df = df[0]
    player_list = df['Player'].tolist()
    temp_list = []
    for player in player_list:
        if player not in temp_list:
            temp_list.append(player)
    player_list = temp_list
    player_list.remove('Player')
    player_list = {'Player' : player_list}
    df = pd.DataFrame(data = player_list)
    return df
    
#generates basketball reference player id for a player
def gen_player_id(player):
    player_id = ''
    player = player.lower()
    player = player.replace('.', '')
    player = player.split(' ')
    first_name = player[0]
    last_name = player[1]
    if len(last_name) >= 5:
        player_id += last_name[0:5]
    else:
        player_id += last_name
    player_id += first_name[0:2]
    player_id += "01"
    return player_id

#web scrapes current_season
def current_season():
    player_id = gen_player_id('Stephen Curry')
    html_text = urlopen(f'https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "per_game"})
    df = pd.read_html(str(table))
    df = df[0]
    current_season = df.loc[len(df)-2]['Season']
    return current_season

#web scrapes per game player stats 
def per_game_player_stats(player):
    player_id = gen_player_id(player)
    html_text = urlopen(f'https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "per_game"})
    df = pd.read_html(str(table))
    df = df[0]
    df = df.fillna('')
    return df

#web scrapes total player stats
def totals_player_stats(player):
    player_id = gen_player_id(player)
    html_text = urlopen(f'https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "totals"})
    df = pd.read_html(str(table))
    df = df[0]
    df= df.fillna('')
    drop = []
    for column in df:
        if 'Unnamed:' in column or column == '':
            drop.append(column)
    df = df.drop(columns=drop)
    return df

#web scrapes NBA team indexes/abbreviations
def NBA_team_indexes():
    indexes = []
    html_text = urlopen('https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table')
    df = pd.read_html(str(table))
    df = df[0]
    df = df.drop([0])
    df.columns = ['Abbreviations', 'Names']
    return df

#web scrapes per game team stats
def per_game_team_stats_all_seasons(team_abbrv):
    html_text = urlopen(f'https://www.basketball-reference.com/teams/{team_abbrv}/stats_per_game_totals.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "stats"})
    df = pd.read_html(str(table))
    df = df[0]
    df= df.fillna('')
    drop = []
    for column in df:
        if 'Unnamed:' in column or column == '':
            drop.append(column)
    df = df.drop(columns=drop)
    return df

#web scrapes per game team stats for every team based on season
def per_game_team_stats_season(season):
    html_text = urlopen(f'https://www.basketball-reference.com/leagues/NBA_{season}.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "per_game-team"})
    df = pd.read_html(str(table))
    df = df[0]
    df = df.fillna('')
    df = df.drop(columns=['Rk'])
    team_list = df['Team'].tolist()
    for i in range(len(team_list)):
        team_list[i] = team_list[i].replace('*', '')
    df['Team'] = team_list
    return df

#web scrapes total teams stats for every team based on season
def totals_team_stats_season(season):
    html_text = urlopen(f'https://www.basketball-reference.com/leagues/NBA_{season}.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "totals-team"})
    df = pd.read_html(str(table))
    df = df[0]
    df = df.fillna('')
    df = df.drop(columns=['Rk'])
    team_list = df['Team'].tolist()
    for i in range(len(team_list)):
        team_list[i] = team_list[i].replace('*', '')
    df['Team'] = team_list
    return df

#web scrapes advanced team stats for ever team based on season
def advanced_team_stats_season(season):
    column_list = []
    html_text = urlopen(f'https://www.basketball-reference.com/leagues/NBA_{season}.html')
    bs = BeautifulSoup(html_text.read(), 'lxml')
    table = bs.find('table', {"id" : "advanced-team"})
    df = pd.read_html((str(table)))
    for col in df[0].columns:
        col = list(col)
        if ('Unnamed' in col[1]):
            col[1] = ''
        column_list.append(col[1])
    df[0].columns = column_list
    del df[0]['Rk']
    team_list = df[0]['Team']
    new_team_list = []
    for team in team_list:
        new_team_list.append(team.replace('*', ''))
    df[0]['Team'] = new_team_list
    df = df[0]
    df = df.fillna('')
    drop = []
    for column in df:
        if column == '' or 'Unnamed:' in column:
            drop.append(column)
    df = df.drop(columns=drop)
    df.to_csv('test.csv')
    return df

#web scrapes player shooting stats
def shooting_player_stats_season(player, season):
    player_id = gen_player_id(player)
    html_text = urlopen(f'https://www.basketball-reference.com/leagues/NBA_{season}_shooting.html')
    bs = BeautifulSoup(html_text.read(), 'lxml')
    table = bs.findAll('table', {"id" : "shooting_stats"})
    df = pd.read_html((str(table)))
    df = df[0]
    df.columns= ['Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'FG%', 'Dist.', '', 
                '%2PFGA', '%0-3FGA', '%3-10FGA', '%10-16FGA', '%16-3PFGA', '%3PFGA', '', 
                '2PFG%', '0-3FG%', '3-10FG%', '10-16FG%', '16-3PFG%', '3PFG%', '',
                '%2PAst''d', '%3PAst''d', '',
                '%DunkFGA', 'Dunk#', '',
                '%CornerThree3PA', 'CornerThree3P%', '',
                'Heaves Att.', '#']
    df = df.drop([1])
    df = df.fillna('')
    for index, row in df.iterrows():
        if row['Player'] == player:
            Rk_index = row['Rk']
            break
    player_series = df[df['Rk'] ==  Rk_index]
    return player_series

#web scrapes team shooting stats
def shooting_team_stats_season(team_name, season):
    html_text = urlopen(f'https://www.basketball-reference.com/leagues/NBA_{season}.html')
    bs = BeautifulSoup(html_text.read(), 'lxml')
    table = bs.findAll('table', {"id" : "shooting-team"})
    df = pd.read_html((str(table)))
    df = df[0]
    df.columns= ['Rk', 'Team', 'G', 'MP', 'FG%', 'Dist.', '', 
                '%2PFGA', '%0-3FGA', '%3-10FGA', '%10-16FGA', '%16-3PFGA', '%3PFGA', '', 
                '2PFG%', '0-3FG%', '3-10FG%', '10-16FG%', '16-3PFG%', '3PFG%', '',
                '%2PAst''d', '%3PAst''d', '',
                '%LayupsFGA', 'Layups#', '',
                '%DunkFGA', 'Dunk#', '',
                '%CornerThree3PA', 'CornerThree3P%', '',
                'Heaves Att.', '#']
    df = df.drop([1])
    df = df.fillna('')
    team_list = df['Team'].tolist()
    for i in range(len(team_list)):
        team_list[i] = team_list[i].replace('*', '')
    df['Team'] = team_list
    for index, row in df.iterrows():
        if row['Team'] == team_name:
            Rk_index = row['Rk']
            break
    team_series = df[df['Rk'] ==  Rk_index]
    return team_series

#gets player ids
def gen_player_id_nba_api(player_name):
    player_dict = players.get_players()
    player = [player for player in player_dict if player["full_name"] == player_name]
    if (len(player) == 0):
        player_id = 0
        return player_id
    player_id = player[0]['id']
    return player_id

#gets team ids
def gen_team_id_nba_api(team_name):
    team_dict = teams.get_teams()
    team = [team for team in team_dict if team["full_name"] == team_name]
    team_id = team[0]['id']
    return team_id

#web scrapes player images
def player_image(player_name):
    player_id = gen_player_id_nba_api(player_name)
    if player_id == 0:
        return 0
    player_image = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
    return player_image

#web scrapes team images
def team_image(team_name):
    html_text = urlopen('https://www.nba.com/teams')
    bs = BeautifulSoup(html_text.read(), 'lxml')
    if team_name == 'Los Angeles Clippers':
        team_name = 'LA Clippers'
    title = team_name + ' Logo'
    img = bs.findAll('img', {"title" : title})
    if len(img) > 0:
        img = str(img[0])
        img = img.split(' ')
        for i in img:
            if "src" in i:
                src = i
        team_image = src[5:]
        length = len(team_image)
        team_image = team_image[:length-1]
        return team_image   

#web scrapes player team
def player_team(player_name):
    player_name = player_name.split(' ')
    first = player_name[0]
    last = player_name[1]
    html_text = urlopen(f'https://hoopshype.com/player/{first}-{last}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    team = soup.find("div", {"class" : "player-team"}).text
    team = team.strip()
    return team

#web scrapes player pos
def player_pos(player_name):
    player_name = player_name.split(' ')
    first = player_name[0]
    last = player_name[1]
    html_text = urlopen(f'https://hoopshype.com/player/{first}-{last}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    pos = soup.findAll("span", {"class" : "player-bio-text-line-value"}) 
    pos = pos[0].text
    return pos

#web scrapes player height
def player_height(player_name):
    player_name = player_name.split(' ')
    first = player_name[0]
    last = player_name[1]
    html_text = urlopen(f'https://hoopshype.com/player/{first}-{last}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    height = soup.findAll("span", {"class" : "player-bio-text-line-value"})
    height = height[2].text
    return height

#web scrapes player weight
def player_weight(player_name):
    player_name = player_name.split(' ')
    first = player_name[0]
    last = player_name[1]
    html_text = urlopen(f'https://hoopshype.com/player/{first}-{last}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    weight = soup.findAll("span", {"class" : "player-bio-text-line-value"})
    weight = weight[3].text
    return weight

#web scrapes player salary
def player_salary(player_name):
    player_name = player_name.split(' ')
    first = player_name[0]
    last = player_name[1]
    html_text = urlopen(f'https://hoopshype.com/player/{first}-{last}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    salary = soup.findAll("span", {"class" : "player-bio-text-line-value"})
    salary = salary[4].text
    return salary

#web scrapes player age (last season)
def player_age(player_name):
    player_id = gen_player_id('Stephen Curry')
    html_text = urlopen(f'https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.findAll('table', {"id" : "per_game"})
    df = pd.read_html(str(table))
    df = df[0]
    current_season = df.loc[len(df)-2]['Season']
    age = df[df['Season'] == current_season]['Age'].tolist()[0]
    return age

#generates team abbrv from name
def gen_team_abbrv(team_name):
    df = NBA_team_indexes()
    team_abbrv = df[df['Names'] == team_name]['Abbreviations'].tolist()[0]
    if team_name == 'Brooklyn Nets':
        team_abbrv = 'NJN'
    if team_name == 'New Orleans Pelicans':
        team_abbrv = 'NOH'
    if team_name == 'Phoenix Suns':
        team_abbrv = 'PHO'
    return team_abbrv    
    
#web scrapes team location
def team_location(team_name):
    team_abbrv = gen_team_abbrv(team_name)
    html_text = urlopen(f'https://www.basketball-reference.com/teams/{team_abbrv}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    team_location = soup.findAll('p')[2].text
    team_location = team_location.strip()
    team_location = team_location.split(':\n ')
    team_location = team_location[1].strip()
    return team_location
    
#web scrapes team playoff appearances
def team_playoff_appearances(team_name):
    team_abbrv = gen_team_abbrv(team_name)
    html_text = urlopen(f'https://www.basketball-reference.com/teams/{team_abbrv}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    team_playoff = soup.findAll('p')[6].text
    team_playoff = team_playoff.strip()
    team_playoff = team_playoff.split(':\n ')
    team_playoff = team_playoff[1].strip()
    return team_playoff

#web scrapes team champisonships
def team_championships(team_name):
    team_abbrv = gen_team_abbrv(team_name)
    html_text = urlopen(f'https://www.basketball-reference.com/teams/{team_abbrv}/')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    team_championships = soup.findAll('p')[7].text
    team_championships = team_championships.strip()
    team_championships = team_championships.split(':\n ')
    team_championships = team_championships[1].strip()
    return team_championships

#web scrapes team coach
def team_coach(team_name):
    name = team_name.split(' ')
    length = len(name)
    name = name[length-1]
    team_id = gen_team_id_nba_api(team_name)
    html_text = urlopen(f'https://www.nba.com/team/{team_id}')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    team_coach = soup.find('ul', {'class' : 'TeamCoaches_list__3EDq-'}).li.text
    return team_coach

#web scrapes team roster
def team_roster(team_name):
    name = team_name.split(' ')
    length = len(name)
    name = name[length-1]
    team_id = gen_team_id_nba_api(team_name)
    html_text = urlopen(f'https://www.nba.com/team/{team_id}')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    table = soup.find('table')
    df = pd.read_html(str(table))
    df = df[0]
    df.to_csv(f'{name}_roster.csv')

#web scrapes team record
def team_record(team_name):
    name = team_name.split(' ')
    length = len(name)
    name = name[length-1]
    team_id = gen_team_id_nba_api(team_name)
    html_text = urlopen(f'https://www.nba.com/team/{team_id}')
    soup = BeautifulSoup(html_text.read(), 'lxml')
    record = soup.find('div', {'class' :'TeamHeader_record__609BJ'}).span.text
    return record