from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from btracker.models import User

class RegistrationForm(FlaskForm): # IMPORT: from flask_wtf import FlaskForm -> to make this work. Passing in the FlaskForm as a parameter for the class
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) # IMPORT: from wtforms.validators import DataRequired, Lenght | from wtforms import StringField
    email = StringField('Email', validators=[DataRequired(), Email()]) # IMPORT: from wtforms.validators import Email
    password = PasswordField('Password', validators=[DataRequired()]) # IMPORT: from wtforms import PasswordField
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')] ) # IMPORT: from wtforms.validators import EqualTo 
    submit = SubmitField('Sign Up') # IMPORT: from wtforms import SubmitField

    def validate_username(self, username): 
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists. Please choose a different one')  # IMPORT: from wtforms.validators import ValidationError

    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please choose a different one')  # IMPORT: from wtforms.validators import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') # IMPORT: from wtforms import BooleanField
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    submit = SubmitField('Update') 

    def validate_username(self, username): 
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists. Please choose a different one')  # IMPORT: from wtforms.validators import ValidationError

    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please choose a different one')  # IMPORT: from wtforms.validators import ValidationError

class NewEntryForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Category', validators=[DataRequired(),  Length(min=2, max=50)])
    comment = TextAreaField('Comments')
    submit = SubmitField('Submit')

class NewBudgetForm(FlaskForm):
    budget = IntegerField('Set Budget', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Mail')

    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()]) # IMPORT: from wtforms import PasswordField
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')] ) # IMPORT: from wtforms.validators import EqualTo 
    
    submit = SubmitField('Reset Password')
    