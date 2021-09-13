from Web_Scraper import player_image, gen_player_list, player_team, player_pos, player_age, player_height, player_weight, player_salary
from datetime import date
import time
import unidecode

today = date.today()
day = today.day
month = today.month
year = today.year

def player_info():
    df = gen_player_list(year)
    player_list = df['Player'].tolist()
    image_list = []
    salary_list = []
    team_list = []
    pos_list = []
    age_list = []
    height_list = []
    weight_list = []
    for player in player_list:
        player = player.replace('.', '')
        player = unidecode.unidecode(player)
        try:
            salary_list.append(player_salary(player))
        except:
            salary_list.append('')
        try:
            image_list.append(player_image(player))
        except:
            image_list.append('')
        try:
            team_list.append(player_team(player))
        except:
            team_list.append('')
        try:
            pos_list.append(player_pos(player))
        except:
            pos_list.append('')
        try:
            age_list.append(player_age(player))
        except:
            age_list.append('')
        try:
            height_list.append(player_height(player))
        except:
            height_list.append('')
        try:
            weight_list.append(player_weight(player))
        except:
            weight_list.append('')
    df['Image'] = image_list
    df['Salary'] = salary_list
    df['Tm'] = team_list
    df['Pos'] = pos_list
    df['Age'] = age_list
    df['height'] = height_list
    df['weight'] = weight_list
    df.fillna('N/A')
    df.to_csv('player_info_df.csv')

while True:
    print ('Updating data')
    player_info()
    print ('Data updated')
    print ('Waiting 24 hours...')
    minute_wait = 1440
    time.sleep(minute_wait*60)