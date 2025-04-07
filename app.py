from flask import Flask, render_template, redirect, url_for, flash, session
from models import db, User
from db import RegistrationForm, LoginForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u3g4v3xdc4'  

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database', 'users.db')}"

db.init_app(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Успешная регистрация!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['username'] = user.username  
            flash('Вход выполнен!')
            return redirect(url_for('profile'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html', form=form)



@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f"Добро пожаловать, {session['username']}!"

@app.route("/")
def base():
    return render_template("base.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/menu/")
def menu():
    return render_template("menu.html")


@app.route("/reviews/")
def reviews():
    return render_template("rewiews.html")


@app.errorhandler(404)  # для каждой страницы если не тот url
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(port=3001, debug=False)
