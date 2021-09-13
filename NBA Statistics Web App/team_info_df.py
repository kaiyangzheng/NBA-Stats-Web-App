from Web_Scraper import NBA_team_indexes, team_image, team_location, team_playoff_appearances, team_championships, team_coach, team_record
from datetime import date
import time

today = date.today()
day = today.day
month = today.month
year = today.year

def team_info():
    df = NBA_team_indexes()
    team_list = df['Names'].tolist()
    image_list = []
    coach_list = []
    record_list = []
    location_list = []
    playoff_app_list = []
    championships_list = []
    for team in team_list:
        print (team)
        image_list.append(team_image(team))
        coach_list.append(team_coach(team))
        record_list.append(team_record(team))
        location_list.append(team_location(team))
        playoff_app_list.append(team_playoff_appearances(team))
        championships_list.append(team_championships(team))
    df['Image'] = image_list
    df['Coach'] = coach_list
    df['Record'] = record_list
    df['Loc'] = location_list
    df['Playoff_App'] = playoff_app_list
    df['Championships'] = championships_list
    df.to_csv('team_info_df.csv')

while True:
    print ('Updating data')
    team_info()
    print ('Data updated')
    print ('Waiting 24 hours...')
    minute_wait = 1440
    time.sleep(minute_wait*60)