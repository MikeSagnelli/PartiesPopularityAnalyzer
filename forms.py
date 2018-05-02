# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter your first name.")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your last name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password."), Length(min=6, message="Passwords must be at least 6 characters.")])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
    submit = SubmitField("Sign in")

class CandidatesForm(FlaskForm):
    candidates = RadioField('Candidates', choices=[('AMLO','Andrés Manuel López Obrador'), ('Anaya','Ricardo Anaya Cortés'), ('Meade', 'José Antonio Meade Kuribeña'), ('Zavala', 'Margarita Ester Zavala Gómez del Campo'), ('Bronco', 'Jaime Rodríguez Calderón'), ('Overview', 'Overview')], default='Overview')
    submit = SubmitField("Select Candidate")