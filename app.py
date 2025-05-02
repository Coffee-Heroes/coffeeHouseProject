from flask_login import current_user
from flask_login import LoginManager, login_user, logout_user
import os
from decouple import config
from flask import Flask, render_template, redirect, url_for, flash, session, request
from models import db, User, Order, Dish
from db import RegistrationForm, LoginForm, OrderForm, AddDishForm
from models import RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash
import base64

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

@app.template_filter('b64encode')
def b64encode_filter(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

@app.route("/", methods=["GET"])
def base():
    reg_form = RegistrationForm()
    log_form = LoginForm()
    add_dish_form = AddDishForm()
    order_form = OrderForm()
    return render_template("base.html", order_form=order_form, log_form=log_form, reg_form=reg_form, add_dish_form=add_dish_form, RoleEnum=RoleEnum)


@app.route("/login", methods=["POST"])
def login():
    reg_form = RegistrationForm()
    log_form = LoginForm()
    add_dish_form = AddDishForm()
    order_form = OrderForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(email=log_form.email.data).first()
        if user and check_password_hash(user.password, log_form.password.data):
            login_user(user, remember=True)
            session['username'] = user.username
            flash("You’ve been signed in successfully!")
            return redirect(url_for('base'))
        else:
            flash("Invalid credentials")
    return render_template("base.html", order_form=order_form, log_form=log_form, reg_form=reg_form, add_dish_form=add_dish_form, RoleEnum=RoleEnum)

@app.route("/register", methods=["GET", "POST"])
def register():
    reg_form = RegistrationForm()
    log_form = LoginForm()
    add_dish_form = AddDishForm()
    order_form = OrderForm()
    if reg_form.validate_on_submit():
        existing_user = User.query.filter_by(email=reg_form.email.data).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for("base"))
        else:
            email = reg_form.email.data
            username = reg_form.username.data
            role = RoleEnum.USER
            password=reg_form.password.data
            
            if email.endswith('@gmail.com') or email.endswith('@ukr.net'):         
                if email == 'coffeeHeroes@ukr.net':
                    role = RoleEnum.ADMIN
                    
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
            else:
                flash('Please, use your google or ukr.net email')
                return redirect(url_for('base'))
    return render_template("base.html", order_form=order_form, log_form=log_form, reg_form=reg_form, add_dish_form=add_dish_form, RoleEnum=RoleEnum)

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    order_form = OrderForm()
    reg_form = RegistrationForm()
    log_form = LoginForm()
    add_dish_form = AddDishForm()
    print("PRODUCT ID:", order_form.product_id.data)
    if order_form.validate_on_submit():
        print("Received product ID:", product_id)
        product_id = order_form.product_id.data
        quantity = order_form.quantity.data
        customer_id = current_user.id 
        delivery_address = order_form.delivery_address.data
        comment = order_form.comment.data

        new_order = Order(
            product_id = product_id,
            quantity = quantity,
            customer_id = customer_id,
            delivery_address = delivery_address,
            comment = comment
        )
        db.session.add(new_order)
        db.session.commit()
        flash('Your order has been created successfully!')
        return redirect(url_for('menu'))
    return render_template('menu.html', order_form=order_form, log_form=log_form, reg_form=reg_form, add_dish_form=add_dish_form, RoleEnum=RoleEnum)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("base"))
    

@app.route("/about")
def about():
    reg_form = RegistrationForm()
    log_form = LoginForm()
    add_dish_form = AddDishForm()
    order_form = OrderForm()
    return render_template("about.html", order_form=order_form, log_form=log_form, reg_form=reg_form, add_dish_form=add_dish_form, RoleEnum=RoleEnum)


@app.route("/menu")
def menu():
    order_form = OrderForm()
    reg_form = RegistrationForm()
    log_form = LoginForm()
    add_dish_form = AddDishForm()
    
    drinks = Dish.query.filter_by(type='drink').all()    
    food = Dish.query.filter_by(type='food').all()

    return render_template("menu.html",order_form=order_form, drinks=drinks, food=food, log_form=log_form, reg_form=reg_form, add_dish_form=add_dish_form, RoleEnum=RoleEnum)

@app.route("/add_dish", methods=['GET', 'POST'])
def add_dish():
    reg_form = RegistrationForm()
    log_form = LoginForm()
    add_dish_form = AddDishForm()
    order_form = OrderForm()
    if add_dish_form.validate_on_submit():
        type = add_dish_form.type.data
        name = add_dish_form.name.data
        description = add_dish_form.description.data
        price = add_dish_form.price.data
        image_file = add_dish_form.image.data
        image_mime = image_file.mimetype
        
        image_bytes = image_file.read()
        
        
        new_dish = Dish(
            type = type,
            name = name,
            description = description,
            price = price,
            image = image_bytes,
            image_mime = image_mime
        )
        db.session.add(new_dish)
        db.session.commit()
        return redirect(url_for('menu'))
    return render_template('menu.html',order_form=order_form, log_form=log_form, reg_form=reg_form, add_dish_form=add_dish_form, RoleEnum=RoleEnum)
@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


@app.errorhandler(404) 
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3001, debug=True)
