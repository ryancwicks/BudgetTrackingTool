from flask import jsonify
from flask_login import login_required
from . import api
from ..models import Budget

@api.route("/budget/")
@login_required
def get_budget():
    """
    Return a budget summary.
    """
    budget_spreadsheet = Budget()
    return jsonify(budget_spreadsheet.budget_current)