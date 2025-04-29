from flask_login import current_user
from flask_login import LoginManager, login_user, logout_user
import os
from decouple import config
import json
from flask import Flask, render_template, redirect, url_for, flash, session
from models import db, User, Order, Dish
from db import RegistrationForm, LoginForm, OrderForm, AddDishForm
from models import RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database', 'users.db')}"

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET"])
def base():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    return render_template("base.html", login_form=login_form, registration_form=registration_form, RoleEnum=RoleEnum)


@app.route("/login", methods=["POST"])
def login():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password, login_form.password.data):  # ❗️рекомендується використовувати hashing
            login_user(user, remember=True)
            session['username'] = user.username
            flash("You’ve been signed in successfully!")
            return redirect(url_for('base'))
        else:
            flash("Invalid credentials")
    return render_template("base.html", login_form=login_form, registration_form=registration_form)

@app.route("/register", methods=["GET", "POST"])
def register():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        existing_user = User.query.filter_by(email=registration_form.email.data).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for("base"))
        else:
            email = registration_form.email.data
            username = registration_form.username.data
            role = RoleEnum.USER
            password=registration_form.password.data
            confirm=registration_form.confirm.data
            
            if not email.endswith('@gmail.com'):
                flash('Please, use your google email')
                return redirect(url_for('base'))
            
            if username in ['Semen', 'Andrew', 'Sviatoslav', 'Ivan']:
                role = RoleEnum.ADMIN

            if password != confirm:
                flash('Passwords must be equal')
                return redirect(url_for('base'))
                
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            session['username'] = new_user.username
            flash("You’ve been registered successfully!")
            return redirect(url_for('base'))
    return render_template("base.html", login_form=login_form, registration_form=registration_form)

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    form = OrderForm()
    if form.validate_on_submit():
        if 'username' not in session:
            flash('You need to log in first.')
            return redirect(url_for('login'))
        
        # Получаем текущего пользователя из сессии
        user = User.query.filter_by(username=session['username']).first()

        # Создаём новый заказ
        new_order = Order(
            product_name=form.product_name.data,
            quantity=form.quantity.data,
            customer_id=user.id,
            delivery_address=form.delivery_address.data,
            comment=form.comment.data
        )
        db.session.add(new_order)
        db.session.commit()
        flash('Your order has been created successfully!')
        if current_user.is_authenticated:
          print('auth')
        else:
          print('not')
        return redirect(url_for('profile'))
    return render_template('create_order.html', form=form)

@app.route("/profile")
def profile():
    if current_user.is_authenticated:
        return f"Welcome, {current_user.username}!"
    else:
        return redirect(url_for('base'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("base"))
    

@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/menu/")
def menu():
    form = AddDishForm()
    return render_template("menu.html", form=form, RoleEnum=RoleEnum)

@app.route("/add_dish", methods=['GET', 'POST'])
def add_dish():
    form = AddDishForm()
    if form.validate_on_submit():
        type = form.type.data
        name = form.name.data
        description = form.description.data
        price = form.price.data
        image = form.image.data
        
        new_dish = Dish(
            type = type,
            name = name,
            description = description,
            price = price,
            image = image
        )
        db.session.add(new_dish)
        db.session.commit()
        return redirect(url_for('menu'))
    return render_template('menu.html', form=form, RoleEnum=RoleEnum)
@app.route("/reviews/")
def reviews():
    return render_template("reviews.html")


@app.errorhandler(404)  # для каждой страницы если не тот url
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
      with app.app_context():
        db.create_all()
        print("Database tables created!")
      app.run(port=3001, debug=False)
