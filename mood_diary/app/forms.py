"""
Form classes for user input validation
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from wtforms.fields import DateField
from wtforms import ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Validate username is unique"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already in use. Please choose a different one.')
    
    def validate_email(self, email):
        """Validate email is unique"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered. Please use a different one.')

class MoodEntryForm(FlaskForm):
    """Form for recording daily mood"""
    date = DateField('Date', validators=[DataRequired()])
    mood_score = IntegerField('Mood (1-10)', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Mood must be between 1 and 10")
    ])
    emoji = SelectField('Emoji', choices=[
        ('😀', 'Very Happy (😀)'),
        ('🙂', 'Happy (🙂)'),
        ('😐', 'Neutral (😐)'),
        ('🙁', 'Sad (🙁)'),
        ('😢', 'Very Sad (😢)'),
        ('😡', 'Angry (😡)'),
        ('😴', 'Tired (😴)'),
        ('🤒', 'Sick (🤒)'),
        ('🥰', 'Loved (🥰)'),
        ('😎', 'Cool (😎)')
    ])
    notes = TextAreaField('Notes about your day', validators=[Optional(), Length(max=1000)])
    activities = StringField('Activities (comma separated)', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Save Entry') 