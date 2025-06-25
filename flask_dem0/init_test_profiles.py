from app import app, db
from app.models import User, Preference, User_Preference, Apartment
from werkzeug.security import generate_password_hash
import random

def init_test_profiles():
    """Initialize test profiles for roommate matcher application"""
    with app.app_context():
        
        # Sample user data with diverse profiles - using correct apartment names from database
        test_users = [
            # The Gates
            {
                'username': 'sarah_jones',
                'email': 'sarah.jones@byui.edu',
                'f_name': 'Sarah',
                'l_name': 'Jones',
                'bio': 'Junior studying Business Management. Love hiking and cooking healthy meals. Looking for a clean, organized roommate who enjoys outdoor activities.',
                'apartment': 'Gates, The - Women',
                'preferences': ['Clean and Organized', 'Cooking Enthusiast', 'Early Riser', 'Fitness Oriented']
            },
            {
                'username': 'mike_wilson',
                'email': 'mike.wilson@byui.edu',
                'f_name': 'Mike',
                'l_name': 'Wilson',
                'bio': 'Sophomore in Computer Science. Enjoy gaming and study groups. Night owl who prefers quiet environments for coding.',
                'apartment': 'Gates, The - Men',
                'preferences': ['Night Owl', 'Quiet Study Environment', 'Budget Conscious', 'Social and Outgoing']
            },
            {
                'username': 'emma_davis',
                'email': 'emma.davis@byui.edu',
                'f_name': 'Emma',
                'l_name': 'Davis',
                'bio': 'Senior in Psychology. Pet lover with a friendly cat. Social butterfly who loves hosting study parties and movie nights.',
                'apartment': 'Gates, The - Women',
                'preferences': ['Pet Friendly', 'Social and Outgoing', 'Cooking Enthusiast', 'Non-Smoker']
            },
            
            # Windsor Manor
            {
                'username': 'jacob_smith',
                'email': 'jacob.smith@byui.edu',
                'f_name': 'Jacob',
                'l_name': 'Smith',
                'bio': 'Junior in Engineering. Gym enthusiast and early riser. Looking for someone who values fitness and healthy living.',
                'apartment': 'Windsor Manor - Men',
                'preferences': ['Fitness Oriented', 'Early Riser', 'Clean and Organized', 'Non-Smoker']
            },
            {
                'username': 'olivia_brown',
                'email': 'olivia.brown@byui.edu',
                'f_name': 'Olivia',
                'l_name': 'Brown',
                'bio': 'Sophomore studying Nursing. Budget-conscious student who loves quiet study time. Prefers organized living spaces.',
                'apartment': 'Windsor Manor - Women',
                'preferences': ['Budget Conscious', 'Quiet Study Environment', 'Clean and Organized', 'Early Riser']
            },
            {
                'username': 'alex_johnson',
                'email': 'alex.johnson@byui.edu',
                'f_name': 'Alex',
                'l_name': 'Johnson',
                'bio': 'Senior in Marketing. Social person who enjoys cooking and hosting friends. Night owl who studies late.',
                'apartment': 'Windsor Manor - Men',
                'preferences': ['Social and Outgoing', 'Cooking Enthusiast', 'Night Owl', 'Pet Friendly']
            },
            
            # University View
            {
                'username': 'mia_garcia',
                'email': 'mia.garcia@byui.edu',
                'f_name': 'Mia',
                'l_name': 'Garcia',
                'bio': 'Freshman in Art Education. Creative soul who loves painting and music. Looking for a chill, pet-friendly environment.',
                'apartment': 'University View - Women',
                'preferences': ['Pet Friendly', 'Social and Outgoing', 'Night Owl', 'Budget Conscious']
            },
            {
                'username': 'ryan_miller',
                'email': 'ryan.miller@byui.edu',
                'f_name': 'Ryan',
                'l_name': 'Miller',
                'bio': 'Junior in Exercise Science. Fitness enthusiast who meal preps. Early bird looking for active roommates.',
                'apartment': 'Park View Apts - Men',  # Using Park View since University View is women-only
                'preferences': ['Fitness Oriented', 'Early Riser', 'Cooking Enthusiast', 'Clean and Organized']
            },
            {
                'username': 'chloe_anderson',
                'email': 'chloe.anderson@byui.edu',
                'f_name': 'Chloe',
                'l_name': 'Anderson',
                'bio': 'Senior in Communications. Budget-conscious student who values quiet study time but also enjoys social gatherings.',
                'apartment': 'University View - Women',
                'preferences': ['Budget Conscious', 'Quiet Study Environment', 'Social and Outgoing', 'Non-Smoker']
            },
            
            # Heritage
            {
                'username': 'ethan_thomas',
                'email': 'ethan.thomas@byui.edu',
                'f_name': 'Ethan',
                'l_name': 'Thomas',
                'bio': 'Sophomore in Finance. Clean and organized individual who enjoys cooking and working out. Early riser with disciplined habits.',
                'apartment': 'Heritage - Men',
                'preferences': ['Clean and Organized', 'Cooking Enthusiast', 'Fitness Oriented', 'Early Riser']
            },
            {
                'username': 'sophia_martin',
                'email': 'sophia.martin@byui.edu',
                'f_name': 'Sophia',
                'l_name': 'Martin',
                'bio': 'Junior in Elementary Education. Pet-loving social butterfly who enjoys group activities and quiet study sessions.',
                'apartment': 'Heritage - Women',
                'preferences': ['Pet Friendly', 'Social and Outgoing', 'Quiet Study Environment', 'Non-Smoker']
            },
            {
                'username': 'noah_rodriguez',
                'email': 'noah.rodriguez@byui.edu',
                'f_name': 'Noah',
                'l_name': 'Rodriguez',
                'bio': 'Senior in Computer Information Technology. Night owl programmer who values quiet spaces. Budget-conscious but social.',
                'apartment': 'Heritage - Men',
                'preferences': ['Night Owl', 'Quiet Study Environment', 'Budget Conscious', 'Social and Outgoing']
            },
            
            # Milano Flats
            {
                'username': 'ava_lopez',
                'email': 'ava.lopez@byui.edu',
                'f_name': 'Ava',
                'l_name': 'Lopez',
                'bio': 'Freshman in Pre-Med. Highly organized and fitness-focused. Early riser who maintains a clean living environment.',
                'apartment': 'Milano Flats - Women',
                'preferences': ['Clean and Organized', 'Fitness Oriented', 'Early Riser', 'Quiet Study Environment']
            },
            {
                'username': 'mason_lee',
                'email': 'mason.lee@byui.edu',
                'f_name': 'Mason',
                'l_name': 'Lee',
                'bio': 'Junior in Mechanical Engineering. Social person who loves cooking and hosting game nights. Pet-friendly and outgoing.',
                'apartment': 'Milano Flats - Men',
                'preferences': ['Social and Outgoing', 'Cooking Enthusiast', 'Pet Friendly', 'Night Owl']
            },
            {
                'username': 'zoe_white',
                'email': 'zoe.white@byui.edu',
                'f_name': 'Zoe',
                'l_name': 'White',
                'bio': 'Sophomore in Interior Design. Budget-conscious student who appreciates clean, organized spaces and quiet study time.',
                'apartment': 'Milano Flats - Women',
                'preferences': ['Budget Conscious', 'Clean and Organized', 'Quiet Study Environment', 'Non-Smoker']
            },
            
            # Northpoint
            {
                'username': 'liam_hall',
                'email': 'liam.hall@byui.edu',
                'f_name': 'Liam',
                'l_name': 'Hall',
                'bio': 'Senior in Business Analytics. Fitness enthusiast who meal preps and maintains a structured lifestyle.',
                'apartment': 'Northpoint - Men',
                'preferences': ['Fitness Oriented', 'Cooking Enthusiast', 'Early Riser', 'Clean and Organized']
            },
            {
                'username': 'isabella_clark',
                'email': 'isabella.clark@byui.edu',
                'f_name': 'Isabella',
                'l_name': 'Clark',
                'bio': 'Junior in Social Work. Pet lover who enjoys quiet study sessions and occasional social gatherings.',
                'apartment': 'Northpoint - Women',
                'preferences': ['Pet Friendly', 'Quiet Study Environment', 'Social and Outgoing', 'Budget Conscious']
            },
            
            # Additional apartments
            {
                'username': 'lucas_wright',
                'email': 'lucas.wright@byui.edu',
                'f_name': 'Lucas',
                'l_name': 'Wright',
                'bio': 'Sophomore in Graphic Design. Night owl creative type who enjoys cooking and social activities.',
                'apartment': 'Birch Plaza - Men',
                'preferences': ['Night Owl', 'Cooking Enthusiast', 'Social and Outgoing', 'Pet Friendly']
            },
            {
                'username': 'grace_adams',
                'email': 'grace.adams@byui.edu',
                'f_name': 'Grace',
                'l_name': 'Adams',
                'bio': 'Junior in Accounting. Organized and budget-conscious student who values clean living spaces and quiet study time.',
                'apartment': 'Birch Plaza - Women',
                'preferences': ['Clean and Organized', 'Budget Conscious', 'Quiet Study Environment', 'Early Riser']
            },
            
            # Brookside Village
            {
                'username': 'aiden_baker',
                'email': 'aiden.baker@byui.edu',
                'f_name': 'Aiden',
                'l_name': 'Baker',
                'bio': 'Senior in Recreation Management. Fitness-oriented outdoor enthusiast who enjoys cooking and early morning workouts.',
                'apartment': 'Brookside Village - Men',
                'preferences': ['Fitness Oriented', 'Early Riser', 'Cooking Enthusiast', 'Social and Outgoing']
            },
            {
                'username': 'lily_gonzalez',
                'email': 'lily.gonzalez@byui.edu',
                'f_name': 'Lily',
                'l_name': 'Gonzalez',
                'bio': 'Freshman in English Education. Quiet studious type who loves reading and pets. Budget-conscious and clean.',
                'apartment': 'Brookside Village - Women',
                'preferences': ['Quiet Study Environment', 'Pet Friendly', 'Budget Conscious', 'Clean and Organized']
            },
            
            # Cottonwood
            {
                'username': 'daniel_white',
                'email': 'daniel.white@byui.edu',
                'f_name': 'Daniel',
                'l_name': 'White',
                'bio': 'Junior in Computer Science. Social coder who enjoys group projects and cooking meals with roommates.',
                'apartment': 'Cottonwood - Men',
                'preferences': ['Social and Outgoing', 'Cooking Enthusiast', 'Night Owl', 'Budget Conscious']
            },
            {
                'username': 'hannah_taylor',
                'email': 'hannah.taylor@byui.edu',
                'f_name': 'Hannah',
                'l_name': 'Taylor',
                'bio': 'Senior in Public Health. Fitness enthusiast who enjoys clean living spaces and early morning workouts.',
                'apartment': 'Cottonwood - Women',
                'preferences': ['Fitness Oriented', 'Clean and Organized', 'Early Riser', 'Non-Smoker']
            }
        ]
        
        print("Adding test users...")
        
        # Create users and assign preferences
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
                password_hash=generate_password_hash('Password123!'),  # Default password for testing
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
                    db.select(Preference).where(Preference.name == pref_name)
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

if __name__ == '__main__':
    # Make sure database is initialized first
    from flask_dem0 import init_database
    init_database()
    
    # Add test profiles
    init_test_profiles()