"""
Description: 
route functions and login/logout functions
"""
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from werkzeug.utils import validate_arguments
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, SelectField, BooleanField, SubmitField,  RadioField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, Email
from datetime import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plot
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import math
from datetime import date
from forms import SignUp, Login, SearchType, Search, Reset, Next

#global variables
today = date.today()
day = today.day
month = today.month
year = today.year
name = 'Guest'
login_status = False
select_method = 'Player name'
search_data = 0
player_data = pd.read_csv('player_info_df.csv')
team_data = pd.read_csv('team_info_df.csv')


#initiating app and SQLAlchemy configs
app = Flask(__name__)
app.config["SECRET_KEY"] = "duck"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

#crete database and add bootstrap
db = SQLAlchemy(app)
Bootstrap(app)

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  


#User database model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(15), unique = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String(80))

#load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUp()
    if signup_form.validate_on_submit():
        hashed_pass = generate_password_hash(signup_form.password.data)
        new_account = User(user=signup_form.username.data, email=signup_form.email.data, password=hashed_pass)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=signup_form, name=name)

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    global name
    global login_status
    login_form = Login()
    if login_form.validate_on_submit():
        user = User.query.filter_by(user=login_form.username.data).first()
        if user:
            name = login_form.username.data
            login_status = True
            if check_password_hash(user.password, login_form.password.data):
                return redirect(url_for('dashboard',name=name, login_status=login_status))
        return('<h1>Invalid username or password</h1>')
    return render_template('login.html', form = login_form,name=name, login_status=login_status)

#logout function
@app.route('/logout')
def logout():
    logout_user()
    global login_status
    global name
    login_status = False
    name = 'Guest'
    return redirect(url_for('dashboard', login_status = login_status, name=name))

#dashboard page
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', name=name, login_status=login_status)

#player search page
@app.route('/players', methods = ['GET', 'POST'])
def playerlist():
    global select_method
    global search_data 
    global min_cards
    global max_cards
    global current_page
    global min_cards
    global max_cards
    select_form = SearchType()
    search_form = Search()
    reset_form = Reset()
    next_form = Next()
    min_cards = 0
    max_cards = 12
    player_list = player_data['Player'].tolist()
    player_num = len(player_list)
    team_list = team_data['Names'].tolist()   
    if reset_form.validate_on_submit():
        if (select_method == 'Player name'):
            player_list = player_data['Player'].tolist()
        if (select_method == 'Team name'):
            team_list = team_data['Names'].tolist()
    if select_form.validate_on_submit():
        select_method = select_form.search_type.data  
    if search_form.validate_on_submit():
        print ()
        if search_data != '':
            search_data = search_form.search.data
            if (select_method == 'Player name'):
                temp_player_list = []
                for i in range(len(player_list)):
                    if search_data.lower() in player_list[i].lower():
                        temp_player_list.append(player_list[i])
                player_list = temp_player_list
            if (select_method == 'Team name'):
                temp_team_list = [] 
                for i in range(len(team_list)): 
                    if search_data.lower() in team_list[i].lower():
                        temp_team_list.append(team_list[i])
                team_list = temp_team_list
        else:
            search_data = 0 
    player_list = player_list[min_cards:max_cards]
    if 'Player'  in player_list:
        player_list.remove('Player')
    player_img_dict = {}
    for player in player_list:
        player_img_dict[player] = player_data[player_data['Player'] == player]['Image'].tolist()[0]
        if player_img_dict[player] == '0':
            player_img_dict[player] = 'https://via.placeholder.com/260x190?text=Player+Image'
    player_tm_dict = {}
    for player in player_list:
        player_tm_dict[player] = player_data[player_data['Player'] == player]['Tm'].tolist()[0] 
        if player_tm_dict[player] == '':
            player_tm_dict[player] == 'N/A'
    player_salary_dict = {}
    for player in player_list:
        player_salary_dict[player] = player_data[player_data['Player'] == player]['Salary'].tolist()[0]
        if player_salary_dict[player] == '':
            player_salary_dict[player] == 'N/A'
    player_pos_dict = {}
    for player in player_list:
        player_pos_dict[player] = player_data[player_data['Player'] == player]['Pos'].tolist()[0]
        if player_pos_dict[player] == '':
            player_pos_dict[player] == 'N/A'    
    player_age_dict = {}
    for player in player_list:
        player_age_dict[player] = player_data[player_data['Player'] == player]['Age'].tolist()[0]
        if player_age_dict[player] == '':
            player_age_dict[player] == 'N/A'   
    player_height_dict = {}
    for player in player_list:
        player_height_dict[player] = player_data[player_data['Player'] == player]['height'].tolist()[0]
        if player_height_dict[player] == '':
            player_height_dict[player] == 'N/A'
    player_weight_dict = {}
    for player in player_list:
        player_weight_dict[player] = player_data[player_data['Player'] == player]['weight'].tolist()[0]
        if player_weight_dict[player] == '':
            player_weight_dict[player] == 'N/A'
    team_img_dict = {}
    for team in team_list:
        team_img_dict[team] = team_data [team_data['Names'] == team]['Image'].tolist()[0]
    return render_template('players.html', name=name, 
                            login_status=login_status, 
                            select_form = select_form, 
                            select_method = select_method, 
                            search_form = search_form, 
                            search_data = search_data,
                            next_form = next_form,
                            reset_form = reset_form,
                            player_list = player_list,
                            team_list = team_list,
                            player_img_dict = player_img_dict,
                            player_tm_dict = player_tm_dict,
                            player_salary_dict = player_salary_dict,
                            player_pos_dict = player_pos_dict,
                            player_age_dict = player_age_dict,
                            player_height_dict = player_height_dict,
                            player_weight_dict = player_weight_dict,
                            team_img_dict = team_img_dict)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  
