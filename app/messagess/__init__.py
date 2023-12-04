from flask import Blueprint
messagess = Blueprint('messagess', __name__)

from . import views