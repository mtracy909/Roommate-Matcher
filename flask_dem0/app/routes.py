from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import User, Apartment, Preference, User_Preference
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
        
        # Store user ID in session (simple session management)
        session['user_id'] = user.id
        session['username'] = user.username
        
        flash(f'Login successful for {form.username.data}')
        return redirect(url_for('index'))
        
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('index'))

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

def get_current_user():
    """Helper function to get the current logged-in user"""
    if 'user_id' not in session:
        return None
    return db.session.get(User, session['user_id'])

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    # Check if user is logged in
    current_user = get_current_user()
    if not current_user:
        flash('Please log in first to create a profile', 'error')
        return redirect(url_for('login'))
    
    form = ProfileForm()
    if form.validate_on_submit():
        try:
            # Update user profile information
            current_user.f_name = form.first_name.data
            current_user.l_name = form.last_name.data
            current_user.bio = form.bio.data
            
            # Get the apartment name from the form choice
            apartment_name = dict(form.apartment_complex.choices)[form.apartment_complex.data]
            
            # Find or create the apartment complex
            apartment = db.session.scalar(
                sa.select(Apartment).where(Apartment.name == apartment_name)
            )
            
            if not apartment:
                # Create new apartment if it doesn't exist
                apartment = Apartment(name=apartment_name)
                db.session.add(apartment)
                db.session.flush()  # Get the apartment ID
            
            current_user.apartment_id = apartment.id
            
            # Clear existing preferences for this user
            db.session.execute(
                sa.delete(User_Preference).where(User_Preference.user_id == current_user.id)
            )
            
            # Add new preferences
            for i, pref_key in enumerate(form.preferences.data):
                # Get the preference name from the form choices
                pref_name = dict(form.preferences.choices)[pref_key]
                
                # Find the preference in the database
                preference = db.session.scalar(
                    sa.select(Preference).where(Preference.name == pref_name)
                )
                
                if preference:
                    user_pref = User_Preference(
                        user_id=current_user.id,
                        preference_id=preference.id,
                        rank=i + 1  # Simple ranking based on order
                    )
                    db.session.add(user_pref)
            
            db.session.commit()
            flash('Profile created successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your profile. Please try again.', 'error')
            print(f"Profile creation error: {e}")
            return redirect(url_for('create_profile'))
    
    return render_template('create_profile.html', form=form)

@app.route("/search/<complex_name>")
def search_results(complex_name):
    try:
        # Query users by apartment complex name
        users = db.session.scalars(
            sa.select(User)
            .join(User.apartment)
            .where(Apartment.name == complex_name)
            .where(User.f_name.isnot(None))  # Only show users with completed profiles
            .where(User.f_name != '')
        ).all()
        
        # Add preferences to each user for display
        for user in users:
            user.preferences_list = []
            user_prefs = db.session.scalars(
                sa.select(User_Preference, Preference)
                .join(Preference, User_Preference.preference_id == Preference.id)
                .where(User_Preference.user_id == user.id)
                .order_by(User_Preference.rank)
            ).all()
            
            for user_pref in user_prefs:
                pref_name = db.session.scalar(
                    sa.select(Preference.name).where(Preference.id == user_pref.preference_id)
                )
                user.preferences_list.append(pref_name)

        return render_template("search_results.html", complex_name=complex_name, users=users)
        
    except Exception as e:
        flash('An error occurred while searching. Please try again.', 'error')
        print(f"Search error: {e}")
        return redirect(url_for('index'))

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


