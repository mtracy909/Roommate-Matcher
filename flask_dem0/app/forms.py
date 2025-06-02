from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min = 6, message = "Password must be at least 6 characters long")
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
