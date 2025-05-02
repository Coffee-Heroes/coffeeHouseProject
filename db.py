from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, TextAreaField, RadioField, FileField
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
    product_id = HiddenField('Product ID')
    product_name = StringField('Product Name', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    delivery_address = StringField('Delivery Address')
    comment = TextAreaField('Comment')
    submit = SubmitField('Замовити')
    
class AddDishForm(FlaskForm):
    type = RadioField('Вид блюда', choices=[
        ('drink', 'Напій'),
        ('food', 'Їжа')
    ], validators=[DataRequired()])
    name = StringField('Name of dish', validators=[DataRequired()])
    description = TextAreaField('Description of dish')
    price = StringField('Price of dish', validators=[DataRequired()])
    image = FileField('Image of dish', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], message='Таке розширення файла не підтримується')])
    submit = SubmitField('Add a new dish')