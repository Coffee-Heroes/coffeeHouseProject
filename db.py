from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, RadioField, FileField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileRequired, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password', message="Password in confirm field must be equal to your password")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class OrderForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    delivery_address = StringField('Delivery Address')
    comment = TextAreaField('Comment')
    submit = SubmitField('Create Order')


class AddDishForm(FlaskForm):
    type = RadioField('Вид блюда', choices=[
        ('Напій', 'drink'),
        ('Їжа', 'food')
    ], validators=[DataRequired()])
    name = StringField('Name of dish', validators=[DataRequired()])
    description = TextAreaField('Description of dish')
    price = IntegerField('Price of dish', validators=[DataRequired()])
    image = FileField('Image of dish', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Таке розширення файла не підтримується')])
    submit = SubmitField('Add a new dish')