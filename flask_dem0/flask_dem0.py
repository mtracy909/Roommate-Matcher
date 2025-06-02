from app import app, db
from app.models import User, Preference, User_Preference

def init_database():
    '''Initialize the dataabase with tables'''
    with app.app_context():

        #Create all tables
        db.create_all()

        #Add some default preferences
        if Preference.query.count() == 0:
            default_preferences = [
                'Clean and Organized',
                'Social and Outgoing', 
                'Quiet Study Environment',
                'Pet Friendly',
                'Non-Smoker',
                'Early Riser',
                'Night Owl',
                'Cooking Enthusiast',
                'Fitness Oriented',
                'Budget Conscious'
            ]

            #Add preferences to the table and commit changes
            for pref_name in default_preferences:
                pref = Preference(name = pref_name)
                db.session.add(pref)
            
            db.session.commit()
            print("Database initialized with default preferences")

        else:
            print("Database already exists")

if __name__ == '__main__':
    #Initialize database first
    init_database()

    print("Starting Flask application...")
    app.run(debug = True, host = '127.0.0.1', port = 5000)