from app import app, db
from app.models import User, Preference, User_Preference, Apartment

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

            print("Added default preferences")

            # Add apartment complexes
        if Apartment.query.count() == 0:
            apartment_names = [
                'Undecided / Not Sure Yet',
                'Abri Apartments - Men',
                'Abri Apartments - Women',
                'Alldredge House',
                'Alpine Chalet',
                'American Avenue - Men',
                'American Avenue - Women',
                'At The Grove',
                'Autumn Winds - Men',
                'Autumn Winds - Women',
                'Abby Lane Manor',
                'Bayside Manor',
                'Birch Plaza - Men',
                'Birch Plaza - Women',
                'Birch Wood I',
                'Birch Wood II',
                'Blue Door, The - Women',
                'Briarwood Apartments',
                'Brooklyn Apartments',
                'Brookside Village - Men',
                'Brookside Village - Women',
                'Bunkhouse',
                'Carriage House',
                'Centre Square - Men',
                'Centre Square - Women',
                'Clarke Apartments',
                'Colonial Heights Townhouses',
                'Colonial House - Men',
                'Colonial House - Women',
                'Cottonwood - Men',
                'Cottonwood - Women',
                'Creekside Cottages - Men',
                'Creekside Cottages - Women',
                'Crestwood Apartments',
                'Crestwood Cottage',
                'Crestwood House',
                'Davenport Apartments',
                'Gates, The - Men',
                'Gates, The - Women',
                'Georgetown Apartments',
                'Greenbrier - Women',
                'Heritage - Men',
                'Heritage - Women',
                'Hillcrest Townhouses - Men',
                'Hillcrest Townhouses - Women',
                'Jordan Ridge',
                'Landing, The - Women',
                'Legacy Ridge',
                'Milano Flats - Men',
                'Milano Flats - Women',
                'Mountain Crest',
                'Northpoint - Men',
                'Northpoint - Women',
                'Park View Apts - Men',
                'Park View Apts - Women',
                'Pines, The - Men',
                'Red Door, The',
                'Rockland Apartments',
                'Royal Crest',
                'Shelbourne Apartments',
                'Snowview Apartments',
                'Somerset Apartments - Women',
                'Towers I',
                'University View - Women',
                'Whitfield House',
                'Windsor Manor - Men',
                'Windsor Manor - Women'
            ]
            
            for apt_name in apartment_names:
                apartment = Apartment(name=apt_name)
                db.session.add(apartment)
            
            print("Added apartment complexes")
            
            db.session.commit()
            print("Database initialized successfully")

        else:
            print("Database already exists")

if __name__ == '__main__':
    #Initialize database first
    init_database()

    print("Starting Flask application...")
    app.run(debug = True, host = '127.0.0.1', port = 5000)