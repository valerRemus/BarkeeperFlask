from flask import Blueprint
bar = Blueprint('bar', __name__)

from . import views