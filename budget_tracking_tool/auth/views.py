from flask import render_template, flash, request, url_for, redirect
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print (form.validate_on_submit())
    if form.validate_on_submit():
        user = User(form.username.data)
        if user.authenticate_user(form.password.data):
            login_user(user, form.remember_me.data)
            print ("Validating user {}".format(form.username.data))
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main_page')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))