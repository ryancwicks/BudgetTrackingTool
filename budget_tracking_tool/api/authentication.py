from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from ..spreadsheet import User
from .errors import unauthorized, forbidden
from . import api
auth = HTTPBasicAuth()

@auth.verify_password_callback
def verify_password(username_or_token, password):
    """
    Check provided info again google sheet data.
    """
    if username_or_token == "":
        return False
    if password == "":
        g.current_user == User.verify_auth_token(username_or_token)
        g.token_used = True
        return g.current_user is not None
    user_auth_spreadsheet = User(username_or_token)
    authenticated = user_auth_spreadsheet.authenticate_user(password)
    if authenticated:
        g.current_user = username_or_token
        g.token_used = False
        return True
    g.current_user = None
    g.token_used = False
    return False

@auth.error_handler
def auth_error():
    return unauthorized("Invalid Credentials")

@api.route('/tokens/', methods=['POST'])
def get_token():
    """
    Reqeuest a token through the API. This prevents previous tokens from being used to get new ones.
    """
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized("Invalid Credentials")
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})