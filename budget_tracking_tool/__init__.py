from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from .config import config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def page_not_found(e):
    return render_template('404.html'), 404

def internal_server_error(e):
    return render_template('500.html'), 500

def main_page():
    return redirect(url_for('expense_entry.index'))

def create_application(config_name="default"):
    """
    Application factory.
    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.add_url_rule('/', 'main_page', main_page)

    login_manager.init_app(app)

    #attach routes and error pages here
    from .expense_entry import expense_entry as expense_entry_blueprint
    app.register_blueprint(expense_entry_blueprint, url_prefix="/expense_entry")
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app