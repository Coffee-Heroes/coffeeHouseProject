from flask import Flask, render_template, abort
app = Flask(__name__)


@app.route("/")
def base():
    render_template("base.html")


@app.route("/about/")
def about():
    render_template("about.html")


@app.route("/contact/")
def contact():
    render_template("contact.html")


@app.route("/menu/")
def menu():
    render_template("menu.html")


@app.route("/reviews/")
def reviews():
    render_template("rewiews.html")


app.run(port=3001, debug=True)
# не запускається тому що не відкриває якийсь файл main.py(принайині у мене)
