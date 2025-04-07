from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired()])  
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])  

class LoginForm(FlaskForm):
    email = PasswordField('Email', validators=[DataRequired()])  
    password = PasswordField('Password', validators=[DataRequired()])  
    submit = SubmitField('Login') 