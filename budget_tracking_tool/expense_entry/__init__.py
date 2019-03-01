from flask import Blueprint

expense_entry = Blueprint('expense_entry', __name__)

from . import views
