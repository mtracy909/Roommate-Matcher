from flask import render_template, redirect, url_for, flash, request, session
from psutil import users
from app import app, db, login
from app.forms import LoginForm, SignupForm
from app.models import User, Apartment, Preference, User_Preference
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import ProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

# Updated apartment display name mapping to match your database
apartment_display_names = {
    'undecided': 'Undecided / Not Sure Yet',
    'abri_apartments': 'Abri Apartments',
    'alldredge_house': 'Alldredge House',
    'alpine_chalet': 'Alpine Chalet',
    'american_avenue': 'American Avenue',
    'at_the_grove': 'At The Grove',
    'autumn_winds': 'Autumn Winds',
    'abby_lane_manor': 'Abby Lane Manor',
    'bayside_manor': 'Bayside Manor',
    'birch_plaza': 'Birch Plaza',
    'birch_wood_i': 'Birch Wood I',
    'birch_wood_ii': 'Birch Wood II',
    'blue_door': 'The Blue Door',
    'briarwood_apartments': 'Briarwood Apartments',
    'brooklyn_apartments': 'Brooklyn Apartments',
    'brookside_village': 'Brookside Village',
    'bunkhouse': 'Bunkhouse',
    'carriage_house': 'Carriage House',
    'centre_square': 'Centre Square',
    'clarke_apartments': 'Clarke Apartments',
    'colonial_heights': 'Colonial Heights Townhouses',
    'colonial_house': 'Colonial House',
    'cottonwood': 'Cottonwood',
    'creekside_cottages': 'Creekside Cottages',
    'crestwood_apartments': 'Crestwood Apartments',
    'crestwood_cottage': 'Crestwood Cottage',
    'crestwood_house': 'Crestwood House',
    'davenport_apartments': 'Davenport Apartments',
    'gates': 'The Gates',
    'georgetown_apartments': 'Georgetown Apartments',
    'greenbrier': 'Greenbrier',
    'heritage': 'Heritage',
    'hillcrest_townhouses': 'Hillcrest Townhouses',
    'jordan_ridge': 'Jordan Ridge',
    'landing': 'The Landing',
    'legacy_ridge': 'Legacy Ridge',
    'milano_flats': 'Milano Flats',
    'mountain_crest': 'Mountain Crest',
    'northpoint': 'Northpoint',
    'park_view': 'Park View Apartments',
    'pines': 'The Pines',
    'red_door': 'The Red Door',
    'rockland_apartments': 'Rockland Apartments',
    'royal_crest': 'Royal Crest',
    'shelbourne_apartments': 'Shelbourne Apartments',
    'snowview_apartments': 'Snowview Apartments',
    'somerset_apartments': 'Somerset Apartments',
    'towers_i': 'Towers I',
    'university_view': 'University View',
    'whitfield_house': 'Whitfield House',
    'windsor_manor': 'Windsor Manor'
}

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
        
        # Using flask_login to login the user
        # Useful for blocking routes that we want users to be logged in to use
        login_user(user, remember=form.remember_me.data)

        flash(f'Login successful for {form.username.data}')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    session.clear()
    logout_user()
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
@login_required
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
            
            # Get the apartment slug from the form choice
            apartment_slug = form.apartment_complex.data  # e.g., 'gates'
            apartment_display = apartment_display_names.get(apartment_slug, apartment_slug)
            
            # Find apartment by display_name OR url_slug
            apartment = db.session.scalar(
                sa.select(Apartment).where(
                    sa.or_(
                        Apartment.display_name == apartment_display,
                        Apartment.url_slug == apartment_slug,
                        Apartment.name.like(f"%{apartment_display}%")
                    )
                )
            )
            
            if not apartment:
                # Create new apartment if it doesn't exist
                apartment = Apartment(
                    name=apartment_display,
                    display_name=apartment_display,
                    url_slug=apartment_slug
                )
                db.session.add(apartment)
                db.session.flush()  # Get the apartment ID
            
            current_user.apartment_id = apartment.id
            
            # Clear existing preferences for this user
            db.session.execute(
                sa.delete(User_Preference).where(User_Preference.user_id == current_user.id)
            )
            
            # Add new preferences with proper mapping
            preference_mapping = {
                'clean': 'Clean and Organized',
                'social': 'Social and Outgoing',
                'quiet': 'Quiet Study Environment',
                'pet': 'Pet Friendly',
                'non_smoker': 'Non-Smoker',
                'early': 'Early Riser',
                'night': 'Night Owl',
                'cooking': 'Cooking Enthusiast',
                'fitness': 'Fitness Oriented',
                'budget': 'Budget Conscious'
            }
            
            for i, pref_key in enumerate(form.preferences.data):
                # Get the preference name from the mapping
                pref_name = preference_mapping.get(pref_key, pref_key)
                
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
        # Convert slug to display name
        display_name = apartment_display_names.get(complex_name, complex_name)
        
        print(f"Searching for apartment: {complex_name} -> {display_name}")

        # Query users by multiple apartment name patterns to handle inconsistencies
        users = db.session.scalars(
            sa.select(User)
            .join(User.apartment)
            .where(
                sa.or_(
                    Apartment.name == display_name,
                    Apartment.display_name == display_name,
                    Apartment.url_slug == complex_name,
                    Apartment.name.like(f"%{display_name}%"),
                    # Handle cases where apartment names have "- Men" or "- Women"
                    Apartment.name.like(f"{display_name}%"),
                    # Handle "The" prefix variations
                    Apartment.name.like(f"%, {display_name}%") if display_name.startswith('The ') else sa.text('false')
                )
            )
            .where(User.f_name.isnot(None))
            .where(User.f_name != '')
        ).all()
        
        print(f"Found {len(users)} users")
        
        # Add preferences to each user for display
        for user in users:
            user.preferences_list = []
            user_prefs = db.session.scalars(
                sa.select(User_Preference)
                .where(User_Preference.user_id == user.id)
                .order_by(User_Preference.rank)
            ).all()
            
            for user_pref in user_prefs:
                pref_name = db.session.scalar(
                    sa.select(Preference.name).where(Preference.id == user_pref.preference_id)
                )
                if pref_name:
                    user.preferences_list.append(pref_name)

        return render_template("search_results.html", complex_name=display_name, users=users)

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
            apartment_name = "No apartment"
            if user.apartment:
                apartment_name = user.apartment.name
            output += f"<p>ID: {user.id}, Username: {user.username}, Name: {user.f_name} {user.l_name}, Apartment: {apartment_name}</p>"
        return output
    except Exception as e:
        return f"Error querying users: {str(e)}"

@app.route("/debug/apartments")
def debug_apartments():
    """View all apartments in database"""
    try:
        apartments = db.session.scalars(sa.select(Apartment)).all()
        output = "<h2>All Apartments:</h2>"
        for apt in apartments:
            user_count = db.session.scalar(sa.select(sa.func.count(User.id)).where(User.apartment_id == apt.id))
            output += f"<p>ID: {apt.id}, Name: '{apt.name}', Display: '{apt.display_name}', Slug: '{apt.url_slug}', Users: {user_count}</p>"
        return output
    except Exception as e:
        return f"Error querying apartments: {str(e)}"
    
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