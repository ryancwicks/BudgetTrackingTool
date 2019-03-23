from flask import render_template, jsonify, session, url_for
from . import expense_entry
from datetime import date
from flask_login import login_required

@expense_entry.route('/')
@login_required
def index ():
    return render_template('expense_entry.html', month_year=date.today().strftime("%B, %Y"))