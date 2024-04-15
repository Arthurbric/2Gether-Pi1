from flask import Flask, render_template, redirect, url_for
from auth import auth

app = Flask(__name__)
app.register_blueprint(auth)

app.secret_key = "uhrq3ur23guyrh"

@app.route("/")
def default():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port="3030")
