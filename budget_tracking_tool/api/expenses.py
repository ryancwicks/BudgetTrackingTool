from flask import jsonify, request
from . import api
from ..spreadsheet import Spreadsheet

@api.route("/add_expense/", methods=["POST"])
def add_expense():
    """
    Add a budget expense.
    """
    budget_spreadsheet = Spreadsheet()
    json_request = request.json
    budget_spreadsheet.add_expense(json_request['user'], json_request['account'], json_request['amount'], json_request['notes'])
    return jsonify({"success": True})