from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from ..model import Category,Crime,CrimeScene

class CrimeCategory(FlaskForm):
    """
    Form to register the crime categories
    """
    violet_type = StringField('Violet Type', validators=[DataRequired()])
    submit = SubmitField('Add Crime Category')