from flask import Flask, render_template, abort

app = Flask(__name__)


@app.route("/")
def about(file):
    if file:
        return render_template("about.html")
    abort(403)


@app.route("/menu/")
def menu(file):
    if file:
        return render_template("menu.html")
    abort(403)


@app.route("/reviews/")
def reviews(file):
    if file:
        return render_template("rewiews.html")
    abort(403)


if __name__ == "__main__":
    app.run(port=3001, debug=True)
