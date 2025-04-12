from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class OrderForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    delivery_address = StringField('Delivery Address')
    comment = TextAreaField('Comment')
    submit = SubmitField('Create Order')