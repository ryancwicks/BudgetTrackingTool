from flask import render_template, jsonify, session, url_for
from . import expense_entry
from datetime import date

@expense_entry.route('/')
def index ():
    return render_template('expense_entry.html', month_year=date.today().strftime("%B, %Y"))