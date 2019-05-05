from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from ..model import User

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account

    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('telephone', validators=[DataRequired()])
    full_names = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')
     

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(self, field):
            if Employee.query.filter_by(username=field.data).first():
                raise ValidationError('Username is already in use')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddPoliceStationForm(FlaskForm):
    """
    Form to register the police stations

    """
    StationName = StringField('Station Name', validators=[DataRequired()])
    division = StringField('Police Division', validators=[DataRequired()])
    submit = SubmitField('Add Station')

