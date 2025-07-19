## Overview

**Project Title**: Roommate Matcher

**Project Description**: 
A web-based roommate matching application designed specifically for BYU-Idaho students. The platform allows students to create profiles, specify their apartment complex and lifestyle preferences, and connect with potential roommates living in the same housing complex. Users can search for roommates by apartment complex, filter by shared preferences, and communicate through an integrated messaging system.

**Project Goals**:
- Simplify the roommate finding process for BYU-Idaho students
- Enable students to find compatible roommates based on lifestyle preferences and housing location
- Provide a secure platform for students to connect and communicate
- Reduce housing stress by matching students with similar living preferences
- Create a centralized hub for apartment-specific roommate searching

## Instructions for Build and Use

Steps to build and/or run the software:

1. Clone the repository and navigate to the project directory
2. Install Python 3.12.1 and create a virtual environment
3. Activate the virtual environment
4. Install required dependencies
5. Run the database initialization
6. The application will start automatically and be available at `http://127.0.0.1:5000`

Instructions for using the software:

1. **Sign Up**: Create an account using your BYU-Idaho email (@byui.edu)
2. **Create Profile**: Fill out your personal information, select your apartment complex, and choose lifestyle preferences
3. **Search for Roommates**: Use the search bar or click on popular complexes to find potential roommates
4. **Filter Results**: Use preference filters to find roommates with similar lifestyles
5. **Connect**: Send connection requests to potential roommates you're interested in
6. **Message**: Use the inbox system to communicate with interested roommates
7. **Find Your Match**: Continue conversations until you find the perfect roommate match

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.12.1
* Flask==3.1.0
* Flask-SQLAlchemy==3.1.1
* Flask-Migrate==4.1.0
* Flask-WTF==1.2.2
* Flask-Login==0.7.0
* WTForms==3.2.1
* email-validator==2.2.0
* Werkzeug==3.1.3
* SQLAlchemy==2.0.41
* psutil (for system utilities)

**Additional Requirements:**
* HTML/CSS/JavaScript for frontend
* SQLite database (automatically created)
* Modern web browser for testing

## Useful Websites to Learn More

We found these websites useful in developing this software:

* [Miguel Grinberg Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
* [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
* [Flask-Login Documentation](https://flask-login.readthedocs.io/)
* [WTForms Documentation](https://wtforms.readthedocs.io/)
* [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Implement advanced matching algorithm based on compatibility scores
* [ ] Add photo upload functionality for user profiles  
* [ ] Create a rating/review system for roommate experiences