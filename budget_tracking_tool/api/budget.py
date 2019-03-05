from flask import jsonify
from . import api
from ..spreadsheet import Spreadsheet

@api.route("/budget/")
def get_budget():
    """
    Return a budget summary.
    """
    budget_spreadsheet = Spreadsheet()
    return jsonify(budget_spreadsheet.budget_current)