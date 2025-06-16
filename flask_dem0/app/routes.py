from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import User
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import ProfileForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("home.html", title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Query user by username
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )

        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        #Check password using werkzeug directly
        if not check_password_hash(user.password_hash, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        flash(f'Login successful for {form.username.data}')
        return redirect(url_for('index'))
        
    return render_template("login.html", title="Login", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():

        #Check if username already exists
        existing_user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )

        if existing_user:
            flash('Username already exists. Please choose a different one')
            return redirect(url_for('signup'))
        
        #Check if email already exists
        existing_email = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )

        if existing_email:
            flash('Email already registered. Please use a different email')
            return redirect(url_for('signup'))
        
        #Create new user
        user = User(
            username = form.username.data,
            email = form.email.data,
            password_hash = generate_password_hash(form.password.data),
            f_name = '', #Default empty values for now
            l_name = '',
            bio = ''
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Account created successfully for {form.username.data}')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occured while creating your account. Please try again')
            print(f"Database error: {e}")
            return redirect(url_for('signup'))
        
    return render_template("signup.html", title="Sign Up", form=form)

#Debug routes (remove in production)
@app.route("/debug/users")
def debug_users():
    """View all users in database"""
    try:
        users = db.session.scalars(sa.select(User)).all()
        output = "<h2>All Users:</h2>"
        for user in users:
            output += f"<p>ID: {user.id}, Username: {user.username}, Email: {user.email}</p>"
        return output
    except Exception as e:
        return f"Error querying users: {str(e)}"
    
@app.route("/debug/clear-users")
def debug_clear_users():
    """Clear all users"""
    try:
        db.session.query(User).delete()
        db.session.commit()
        return "All users cleared"
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"
    

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # In the future, you'd save to the database here
        flash('Profile created successfully!', 'success')
        return redirect(url_for('create_profile'))  # redirect to same page for now
    return render_template('create_profile.html', form=form)

from app.models import Apartment, User

@app.route("/search/<complex_name>")
def search_results(complex_name):
    users = db.session.scalars(
        sa.select(User)
        .join(User.apartment)
        .where(Apartment.name == complex_name)
    ).all()

    return render_template("search_results.html", complex_name=complex_name, users=users)


