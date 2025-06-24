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

    apartment_complex = SelectField(
        'Apartment Complex',
        choices=[
            ('undecided', 'Undecided / Not Sure Yet'),
            ('abri_apartments', 'Abri Apartments'),
            ('alldredge_house', 'Alldredge House'),
            ('alpine_chalet', 'Alpine Chalet'),
            ('american_avenue', 'American Avenue'),
            ('at_the_grove', 'At The Grove'),
            ('autumn_winds', 'Autumn Winds'),
            ('abby_lane_manor', 'Abby Lane Manor'),
            ('bayside_manor', 'Bayside Manor'),
            ('birch_plaza', 'Birch Plaza'),
            ('birch_wood_1', 'Birch Wood I'),
            ('birch_wood_2', 'Birch Wood II'),
            ('blue_door', 'The Blue Door'),
            ('briarwood_apartments', 'Briarwood Apartments'),
            ('brooklyn_apartments', 'Brooklyn Apartments'),
            ('brookside_village', 'Brookside Village'),
            ('bunkhouse', 'Bunkhouse'),
            ('carriage_house', 'Carriage House'),
            ('centre_square', 'Centre Square'),
            ('clarke_apartments', 'Clarke Apartments'),
            ('colonial_heights', 'Colonial Heights Townhouses'),
            ('colonial_house', 'Colonial House'),
            ('cottonwood', 'Cottonwood'),
            ('creekside_cottages', 'Creekside Cottages'),
            ('crestwood_apartments', 'Crestwood Apartments'),
            ('crestwood_cottage', 'Crestwood Cottage'),
            ('crestwood_house', 'Crestwood House'),
            ('davenport_apartments', 'Davenport Apartments'),
            ('delta_phi_apartments', 'Delta Phi Apartments'),
            ('gates', 'The Gates'),
            ('georgetown_apartments', 'Georgetown Apartments'),
            ('greenbrier', 'Greenbrier'),
            ('heritage', 'Heritage'),
            ('hillcrest_townhouses', 'Hillcrest Townhouses'),
            ('jordan_ridge', 'Jordan Ridge'),
            ('kensington_manor', 'Kensington Manor'),
            ('la_jolla', 'La Jolla'),
            ('lifting_placeholder', 'The Lodge'),
            ('landing', 'The Landing'),
            ('legacy_ridge', 'Legacy Ridge'),
            ('milano_flats', 'Milano Flats'),
            ('mountain_crest', 'Mountain Crest'),
            ('northpoint', 'NorthPoint'),
            ('park_view_apts', 'Park View Apartments'),
            ('pines', 'The Pines'),
            ('pincock_house', 'Pincock House'),
            ('pinnacle_point', 'Pinnacle Point'),
            ('red_door', 'The Red Door'),
            ('rivieria_apartments', 'Riviera Apartments'),
            ('rock_casa', 'Rock Casa'),
            ('rockland_apartments', 'Rockland Apartments'),
            ('rose_casa', 'Rose Casa'),
            ('royal_crest', 'Royal Crest'),
            ('shelbourne_apartments', 'Shelbourne Apartments'),
            ('snowview_apartments', 'Snowview Apartments'),
            ('somerset_apartments', 'Somerset Apartments'),
            ('sundance_apartments', 'Sundance Apartments'),
            ('the_cove', 'The Cove'),
            ('towers_i', 'Towers I'),
            ('towers_ii', 'Towers II'),
            ('university_view', 'University View'),
            ('webster_house', 'Webster House'),
            ('whitfield_house', 'Whitfield House'),
            ('windsor_manor', 'Windsor Manor'),
            ('sunrise_village', 'Sunrise Village'),
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