from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # to allow user to upload
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user # check current user that is updating their account
from flaskblog.models import User # helps validating fields. need to check if user exists in db, etc

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username): # to help validate if username already exists in db. WTForms functionality

        user = User.query.filter_by(username = username.data).first()

        if user: # that user already exists in db
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email): # to help validate if email already exists in db.

        email = User.query.filter_by(email = email.data).first()

        if email: # that email already exists in db
            raise ValidationError('That email is taken. Please choose a different one.')    


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Account')

    def validate_username(self, username): # to help validate if username already exists in db. WTForms functionality
        if username.data != current_user.username: # username IS wanting to change their username. without this, it'd return error since the user doesn't HAVE to change username
            
            user = User.query.filter_by(username = username.data).first()

            if user: # that user already exists in db
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email): # to help validate if email already exists in db.
        if email.data != current_user.email:

            email = User.query.filter_by(email = email.data).first()

            if email: # that email already exists in db
                raise ValidationError('That email is taken. Please choose a different one.') 




















