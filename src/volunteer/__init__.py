from flask import Blueprint

volunteer = Blueprint("volunteer", __name__)

from . import views
