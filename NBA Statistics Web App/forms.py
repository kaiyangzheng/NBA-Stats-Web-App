from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, RadioField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, Email
from wtforms.widgets.core import Input 

#signup form
class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=15)]) 
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    password_check = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password')])
    submit = SubmitField('Sign Up')

#login form
class Login(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min=5, max=80)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

#search type form
class SearchType(FlaskForm):
    search_type = RadioField('', choices = [('Player name', 'Players'), ('Team name', 'Teams')], validators=[InputRequired()])
    submit = SubmitField('Select')

#search form
class Search(FlaskForm):
    search = StringField('', validators=[InputRequired()], render_kw={"placeholder": "Enter Keywords"})
    submit = SubmitField('Search')

#rest form
class Reset(FlaskForm):
    submit = SubmitField('Reset')

#pagination next form
class Next(FlaskForm):
    submit = SubmitField('Next>>')