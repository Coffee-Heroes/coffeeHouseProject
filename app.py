import os
from flask import Flask, render_template, redirect, url_for, flash, session, request
from models import db, User, Order
from db import RegistrationForm, LoginForm, OrderForm
from models import RoleEnum

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u3g4v3xdc4'  

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database', 'users.db')}"

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def base():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    return render_template('base.html', login_form=login_form, registration_form=registration_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        current_user = User.query.filter_by(email = registration_form.email.data).first()
        if current_user:
            flash('This email is already registered')
        else:
            username = registration_form.username.data
            role = RoleEnum.USER
            if username in ['Semen', 'Andrew', 'Sviatoslav', 'Ivan']:
                role = RoleEnum.ADMIN
            
            new_user = User(
                username = username,
                email = registration_form.email.data,
                password = registration_form.password.data,
                role = role
            )
            db.session.add(new_user)
            db.session.commit()
            flash('You`ve been registered successfully!')
            return redirect(url_for('profile'))
    return render_template('base.html', login_form=login_form, registration_form=registration_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.password == login_form.password.data:
            session['username'] = user.username
            flash('You`ve been signed in successfully!')
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials')
    return render_template('base.html', login_form=login_form, registration_form=registration_form) 

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
        return redirect(url_for('profile'))
    return render_template('create_order.html', form=form)


@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f"Welcome, {session['username']}!"

@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/menu/")
def menu():
    return render_template("menu.html")


@app.route("/reviews/")
def reviews():
    return render_template("reviews.html")


@app.errorhandler(404)  # для каждой страницы если не тот url
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        print(app.url_map)
    app.run(port=3001, debug=False)
