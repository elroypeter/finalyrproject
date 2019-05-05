from flask import Blueprint
crimes = Blueprint('crimes', __name__)
from . import views