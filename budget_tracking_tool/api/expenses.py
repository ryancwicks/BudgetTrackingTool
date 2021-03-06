from flask import jsonify, request
from flask_login import login_required, current_user
from . import api
from ..models import Budget

@api.route("/add_expense/", methods=["POST"])
@login_required
def add_expense():
    """
    Add a budget expense.
    """
    budget_spreadsheet = Budget()
    json_request = request.json
    budget_spreadsheet.add_expense(current_user.get_id(), json_request['account'], json_request['amount'], json_request['notes'])
    return jsonify({"success": True})