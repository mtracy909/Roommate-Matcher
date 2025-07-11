from app import app, db
from app.models import User, Preference, User_Preference, Apartment
from sqlalchemy import select
from werkzeug.security import generate_password_hash
import random

SEED = 56704
PASSWORD = "Password123!"
BIO = "I'm a Test Profile! :)"
PREFERENCES = ['Clean and Organized',
                'Social and Outgoing', 
                'Quiet Study Environment',
                'Pet Friendly',
                'Non-Smoker',
                'Early Riser',
                'Night Owl',
                'Cooking Enthusiast',
                'Fitness Oriented',
                'Budget Conscious']
APARTMENTS = [
    'Undecided',
    'Abri Apartments',
    'Alldredge House',
    'Alpine Chalet',
    'American Avenue',
    'At The Grove',
    'Autumn Winds',
    'Abby Lane Manor',
    'Bayside Manor',
    'Birch Plaza',
    'Birch Wood I',
    'Birch Wood II',
    'The Blue Door',
    'Briarwood Apartments',
    'Brooklyn Apartments',
    'Brookside Village',
    'Bunkhouse',
    'Carriage House',
    'Centre Square',
    'Clarke Apartments',
    'Colonial Heights Townhouses',
    'Colonial House',
    'Cottonwood',
    'Creekside Cottages',
    'Crestwood Apartments',
    'Crestwood Cottage',
    'Crestwood House',
    'Davenport Apartments',
    'The Gates',
    'Georgetown Apartments',
    'Greenbrier',
    'Heritage',
    'Hillcrest Townhouses',
    'Jordan Ridge',
    'The Landing',
    'Legacy Ridge',
    'Milano Flats',
    'Mountain Crest',
    'Northpoint',
    'Park View Apartments',
    'The Pines',
    'The Red Door',
    'Rockland Apartments',
    'Royal Crest',
    'Shelbourne Apartments',
    'Snowview Apartments',
    'Somerset Apartments',
    'Towers I',
    'University View',
    'Whitfield House',
    'Windsor Manor'
]

def generate_profile(first_name_list, last_name_list, appartment, preferences, bio):
    # Grabs a random name and generates a number
    first_name = first_name_list[random.randint(0, len(first_name_list)-1)]
    last_name = last_name_list[random.randint(0, len(last_name_list)-1)]
    user_num = random.randint(1,99)

    # Creates a random set of preferences
    mutable_prefs = []
    for p in preferences:
        mutable_prefs.append(p)
    prefs = []
    for i in range(4):
        pref_index = random.randint(0, len(mutable_prefs)-1)
        preference = mutable_prefs.pop(pref_index)
        prefs.append(preference)
    
    # TODO currently no way to distiguish male or female in the database
    profile = {
        'username': f"{first_name.lower()}_{last_name.lower()}{user_num}",
        'email' : f"{first_name.lower()}.{last_name.lower()}{user_num}@example.com",
        'f_name': first_name,
        'l_name': last_name,
        'bio': bio,
        'apartment': appartment,
        'preferences': prefs
    }
    return profile


def get_names(name_file):
    names = []
    with open(name_file, 'r') as file:
        for name in file:
            names.append(name.strip())
    return names

def generate_profiles(aparts):
    #sets the seed so names can be consitiant accross all instances
    random.seed(SEED)
    females = get_names("test_names/f_names.txt")
    last_names = get_names("test_names/l_names.txt")
    males = get_names("test_names/m_names.txt")

    profiles = []
    for apt in aparts:
        # generates 4 males and 4 females per apartment
        for i in range(4):
            f_profile = generate_profile(females, last_names, apt, PREFERENCES, BIO)
            m_profile = generate_profile(males, last_names, apt, PREFERENCES, BIO)
            profiles.append(f_profile)
            profiles.append(m_profile)

    return profiles

def init_test_profiles2():
    print("Adding test users...")
    
    
    # Create users and assign preferences
    with app.app_context():
        all_apartments = db.session.scalars(select(Apartment.name)).all()
        test_users = generate_profiles(all_apartments)

        for user_data in test_users:
            # Check if user already exists
            existing_user = db.session.scalar(
                db.select(User).where(User.username == user_data['username'])
            )
            
            if existing_user:
                print(f"User {user_data['username']} already exists, skipping...")
                continue
            
            # Find or create apartment
            apartment = db.session.scalar(
                db.select(Apartment).where(Apartment.name == user_data['apartment'])
            )
            
            if not apartment:
                print(f"Apartment '{user_data['apartment']}' not found, skipping user {user_data['username']}")
                continue
            
            # Create user
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(PASSWORD),  # Default password for testing
                f_name=user_data['f_name'],
                l_name=user_data['l_name'],
                bio=user_data['bio'],
                apartment_id=apartment.id
            )
            
            db.session.add(user)
            db.session.flush()  # Get the user ID
            
            # Add user preferences
            for i, pref_name in enumerate(user_data['preferences']):
                preference = db.session.scalar(
                    select(Preference).where(Preference.name == pref_name)
                )
                
                if preference:
                    user_pref = User_Preference(
                        user_id=user.id,
                        preference_id=preference.id,
                        rank=i + 1
                    )
                    db.session.add(user_pref)
            
            print(f"Added user: {user_data['f_name']} {user_data['l_name']} ({user_data['username']}) at {user_data['apartment']}")
        
        # Commit all changes
        db.session.commit()
        print(f"\nSuccessfully added {len(test_users)} test users to the database!")
        print("\nTest users can log in with:")
        print("- Username: any of the usernames above")
        print("- Password: Password123!")
        
        # Print summary by apartment
        print("\n" + "="*50)
        print("USERS BY APARTMENT COMPLEX:")
        print("="*50)
        
        apartments = {}
        for user_data in test_users:
            apt = user_data['apartment']
            if apt not in apartments:
                apartments[apt] = []
            apartments[apt].append(f"{user_data['f_name']} {user_data['l_name']} (@{user_data['username']})")
        
        for apt, users in apartments.items():
            print(f"\n{apt}:")
            for user in users:
                print(f"  - {user}")

if __name__ == "__main__":
    init_test_profiles2()