from flask import render_template, jsonify, session, url_for
from . import expense_entry

@expense_entry.route('/', methods=['GET', 'POST'])
def index ():
    return render_template('expense_entry.html')