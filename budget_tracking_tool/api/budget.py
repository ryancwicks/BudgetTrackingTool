from flask import jsonify
from . import api
from ..models import Budget

@api.route("/budget/")
def get_budget():
    """
    Return a budget summary.
    """
    budget_spreadsheet = Budget()
    return jsonify(budget_spreadsheet.budget_current)