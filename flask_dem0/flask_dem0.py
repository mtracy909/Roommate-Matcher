from app import app, db
from app.models import User, Preference, User_Preference, Apartment

def init_database():
    '''Initialize the database with tables'''
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

        # Add apartment complexes with display names for user-friendly interface
        if Apartment.query.count() == 0:
            # Format: (database_name, display_name, url_slug)
            apartment_data = [
                ('Undecided / Not Sure Yet', 'Undecided', 'undecided'),
                ('Abri Apartments - Men', 'Abri Apartments', 'abri_apartments'),
                ('Abri Apartments - Women', 'Abri Apartments', 'abri_apartments'),
                ('Alldredge House', 'Alldredge House', 'alldredge_house'),
                ('Alpine Chalet', 'Alpine Chalet', 'alpine_chalet'),
                ('American Avenue - Men', 'American Avenue', 'american_avenue'),
                ('American Avenue - Women', 'American Avenue', 'american_avenue'),
                ('At The Grove', 'At The Grove', 'at_the_grove'),
                ('Autumn Winds - Men', 'Autumn Winds', 'autumn_winds'),
                ('Autumn Winds - Women', 'Autumn Winds', 'autumn_winds'),
                ('Abby Lane Manor', 'Abby Lane Manor', 'abby_lane_manor'),
                ('Bayside Manor', 'Bayside Manor', 'bayside_manor'),
                ('Birch Plaza - Men', 'Birch Plaza', 'birch_plaza'),
                ('Birch Plaza - Women', 'Birch Plaza', 'birch_plaza'),
                ('Birch Wood I', 'Birch Wood I', 'birch_wood_i'),
                ('Birch Wood II', 'Birch Wood II', 'birch_wood_ii'),
                ('Blue Door, The - Women', 'The Blue Door', 'blue_door'),
                ('Briarwood Apartments', 'Briarwood Apartments', 'briarwood_apartments'),
                ('Brooklyn Apartments', 'Brooklyn Apartments', 'brooklyn_apartments'),
                ('Brookside Village - Men', 'Brookside Village', 'brookside_village'),
                ('Brookside Village - Women', 'Brookside Village', 'brookside_village'),
                ('Bunkhouse', 'Bunkhouse', 'bunkhouse'),
                ('Carriage House', 'Carriage House', 'carriage_house'),
                ('Centre Square - Men', 'Centre Square', 'centre_square'),
                ('Centre Square - Women', 'Centre Square', 'centre_square'),
                ('Clarke Apartments', 'Clarke Apartments', 'clarke_apartments'),
                ('Colonial Heights Townhouses', 'Colonial Heights Townhouses', 'colonial_heights'),
                ('Colonial House - Men', 'Colonial House', 'colonial_house'),
                ('Colonial House - Women', 'Colonial House', 'colonial_house'),
                ('Cottonwood - Men', 'Cottonwood', 'cottonwood'),
                ('Cottonwood - Women', 'Cottonwood', 'cottonwood'),
                ('Creekside Cottages - Men', 'Creekside Cottages', 'creekside_cottages'),
                ('Creekside Cottages - Women', 'Creekside Cottages', 'creekside_cottages'),
                ('Crestwood Apartments', 'Crestwood Apartments', 'crestwood_apartments'),
                ('Crestwood Cottage', 'Crestwood Cottage', 'crestwood_cottage'),
                ('Crestwood House', 'Crestwood House', 'crestwood_house'),
                ('Davenport Apartments', 'Davenport Apartments', 'davenport_apartments'),
                ('Gates, The - Men', 'The Gates', 'gates'),
                ('Gates, The - Women', 'The Gates', 'gates'),
                ('Georgetown Apartments', 'Georgetown Apartments', 'georgetown_apartments'),
                ('Greenbrier - Women', 'Greenbrier', 'greenbrier'),
                ('Heritage - Men', 'Heritage', 'heritage'),
                ('Heritage - Women', 'Heritage', 'heritage'),
                ('Hillcrest Townhouses - Men', 'Hillcrest Townhouses', 'hillcrest_townhouses'),
                ('Hillcrest Townhouses - Women', 'Hillcrest Townhouses', 'hillcrest_townhouses'),
                ('Jordan Ridge', 'Jordan Ridge', 'jordan_ridge'),
                ('Landing, The - Women', 'The Landing', 'landing'),
                ('Legacy Ridge', 'Legacy Ridge', 'legacy_ridge'),
                ('Milano Flats - Men', 'Milano Flats', 'milano_flats'),
                ('Milano Flats - Women', 'Milano Flats', 'milano_flats'),
                ('Mountain Crest', 'Mountain Crest', 'mountain_crest'),
                ('Northpoint - Men', 'Northpoint', 'northpoint'),
                ('Northpoint - Women', 'Northpoint', 'northpoint'),
                ('Park View Apts - Men', 'Park View Apartments', 'park_view'),
                ('Park View Apts - Women', 'Park View Apartments', 'park_view'),
                ('Pines, The - Men', 'The Pines', 'pines'),
                ('Red Door, The', 'The Red Door', 'red_door'),
                ('Rockland Apartments', 'Rockland Apartments', 'rockland_apartments'),
                ('Royal Crest', 'Royal Crest', 'royal_crest'),
                ('Shelbourne Apartments', 'Shelbourne Apartments', 'shelbourne_apartments'),
                ('Snowview Apartments', 'Snowview Apartments', 'snowview_apartments'),
                ('Somerset Apartments - Women', 'Somerset Apartments', 'somerset_apartments'),
                ('Towers I', 'Towers I', 'towers_i'),
                ('University View - Women', 'University View', 'university_view'),
                ('Whitfield House', 'Whitfield House', 'whitfield_house'),
                ('Windsor Manor - Men', 'Windsor Manor', 'windsor_manor'),
                ('Windsor Manor - Women', 'Windsor Manor', 'windsor_manor')
            ]
            
            for apt_name, display_name, url_slug in apartment_data:
                # Assuming your Apartment model has name, display_name, and url_slug fields
                # If not, you'll need to add these fields to your model
                apartment = Apartment(
                    name=apt_name,
                    display_name=display_name,
                    url_slug=url_slug
                )
                db.session.add(apartment)
            
            print("Added apartment complexes with display names")
            
            db.session.commit()
            print("Database initialized successfully")

        else:
            print("Database already exists")

if __name__ == '__main__':
    #Initialize database first
    init_database()

    print("Starting Flask application...")
    app.run(debug = True, host = '127.0.0.1', port = 5000)