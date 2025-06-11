from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    SelectField,
    SelectMultipleField,
    widgets
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
    Regexp
)
from app.models import User
import sqlalchemy as sa
from app import db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min = 4, max = 20, message = "Username must be between 4 and 20 characters")
    ])
    email = StringField('Email', validators=[DataRequired(), Regexp(r'.+@byui\.edu$', message="Email must end with @byui.edu")])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8, message="Password must be at least 8 characters long"),Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
        message="Password must contain one uppercase letter, one lowercase letter, and one number.")
])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), 
        EqualTo('password', message = "Passwords must match")
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        try:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Username already exists. Please choose a different one')
        except Exception as e:
            #If there is a database error we will catch in in the route.py
            pass

    def validate_email(self, email):
        try:
            user = db.session.scalar(sa.select(User).where(User.email == email.data))
            if user is not None:
                raise ValidationError('Email already registered. Please use a different email')
        except Exception as e:
            #If there is a database error we will catch in in the route.py
            pass

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])
    
    # Dropdown of Rexburg apartments
    apartment_complex = SelectField(
        'Apartment Complex',
        choices=[
        ('undecided', 'Undecided / Not Sure Yet'),
        ('abri_apartments_men', 'Abri Apartments - Men'),
        ('abri_apartments_women', 'Abri Apartments - Women'),
        ('alldredge_house', 'Alldredge House'),
        ('alpine_chalet', 'Alpine Chalet'),
        ('american_avenue_men', 'American Avenue - Men'),
        ('american_avenue_women', 'American Avenue - Women'),
        ('at_the_grove', 'At The Grove'),
        ('autumn_winds_men', 'Autumn Winds - Men'),
        ('autumn_winds_women', 'Autumn Winds - Women'),
        ('abby_lane_manor', 'Abby Lane Manor'),
        ('bayside_manor', 'Bayside Manor'),
        ('birch_plaza_men', 'Birch Plaza - Men'),
        ('birch_plaza_women', 'Birch Plaza - Women'),
        ('birch_wood_1', 'Birch Wood I'),
        ('birch_wood_2', 'Birch Wood II'),
        ('blue_door_women', 'Blue Door, The - Women'),
        ('briarwood_apartments', 'Briarwood Apartments'),
        ('brooklyn_apartments', 'Brooklyn Apartments'),
        ('brookside_village_men', 'Brookside Village - Men'),
        ('brookside_village_women', 'Brookside Village - Women'),
        ('bunkhouse', 'Bunkhouse'),
        ('carriage_house', 'Carriage House'),
        ('centre_square_men', 'Centre Square - Men'),
        ('centre_square_women', 'Centre Square - Women'),
        ('clarke_apartments', 'Clarke Apartments'),
        ('colonial_heights_townhouses', 'Colonial Heights Townhouses'),
        ('colonial_house_men', 'Colonial House - Men'),
        ('colonial_house_women', 'Colonial House - Women'),
        ('cottonwood_men', 'Cottonwood - Men'),
        ('cottonwood_women', 'Cottonwood - Women'),
        ('creekside_cottages_men', 'Creekside Cottages - Men'),
        ('creekside_cottages_women', 'Creekside Cottages - Women'),
        ('crestwood_apartments', 'Crestwood Apartments'),
        ('crestwood_cottage', 'Crestwood Cottage'),
        ('crestwood_house', 'Crestwood House'),
        ('davenport_apartments', 'Davenport Apartments'),
        ('gates_men', 'Gates, The - Men'),
        ('gates_women', 'Gates, The - Women'),
        ('georgetown_apartments', 'Georgetown Apartments'),
        ('greenbrier_women', 'Greenbrier - Women'),
        ('heritage_men', 'Heritage - Men'),
        ('heritage_women', 'Heritage - Women'),
        ('hillcrest_townhouses_men', 'Hillcrest Townhouses - Men'),
        ('hillcrest_townhouses_women', 'Hillcrest Townhouses - Women'),
        ('jordan_ridge', 'Jordan Ridge'),
        ('landing_women', 'Landing, The - Women'),
        ('legacy_ridge', 'Legacy Ridge'),
        ('milano_flats_men', 'Milano Flats - Men'),
        ('milano_flats_women', 'Milano Flats - Women'),
        ('mountain_crest', 'Mountain Crest'),
        ('northpoint_men', 'Northpoint - Men'),
        ('northpoint_women', 'Northpoint - Women'),
        ('park_view_apts_men', 'Park View Apts - Men'),
        ('park_view_apts_women', 'Park View Apts - Women'),
        ('pines_men', 'Pines, The - Men'),
        ('red_door', 'Red Door, The'),
        ('rockland_apartments', 'Rockland Apartments'),
        ('royal_crest', 'Royal Crest'),
        ('shelbourne_apartments', 'Shelbourne Apartments'),
        ('snowview_apartments', 'Snowview Apartments'),
        ('somerset_apartments_women', 'Somerset Apartments - Women'),
        ('towers_i', 'Towers I'),
        ('university_view_women', 'University View - Women'),
        ('whitfield_house', 'Whitfield House'),
        ('windsor_manor_men', 'Windsor Manor - Men'),
        ('windsor_manor_women', 'Windsor Manor - Women'),
        ],
        validators=[DataRequired()]
    )

    bio = TextAreaField('Short Introduction About Yourself', validators=[Length(max=300)])

    preferences = SelectMultipleField(
        'Lifestyle Preferences',
        choices=[
            ('clean', 'Clean and Organized'),
            ('social', 'Social and Outgoing'),
            ('quiet', 'Quiet Study Environment'),
            ('pet', 'Pet Friendly'),
            ('non_smoker', 'Non-Smoker'),
            ('early', 'Early Riser'),
            ('night', 'Night Owl'),
            ('cooking', 'Cooking Enthusiast'),
            ('fitness', 'Fitness Oriented'),
            ('budget', 'Budget Conscious')
        ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    submit = SubmitField('Create Profile')