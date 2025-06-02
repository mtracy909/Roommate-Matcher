from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import LoginForm, SignupForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("home.html", title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for {form.username.data}")
        return redirect(url_for("index"))
    return render_template("login.html", title="Login", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}")
        return redirect(url_for("index"))
    return render_template("signup.html", title="Sign Up", form=form)
