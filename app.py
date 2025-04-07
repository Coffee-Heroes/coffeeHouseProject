from flask import Flask, render_template, abort

app = Flask(__name__)


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
