from flask import Flask, render_template, abort
app = Flask(__name__)


@app.route("/")
def base():
    return render_template("base.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/menu/")
def menu():
    return render_template("menu.html")


@app.route("/reviews/")
def reviews():
    return render_template("rewiews.html")


if __name__ == '__main__':
    app.run(port=3001, debug=True)