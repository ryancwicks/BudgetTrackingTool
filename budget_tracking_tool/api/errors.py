from flask import render_template, request, jsonify
from . import api

@api.app_errorhandler(404)
def page_not_found(e):
    """
    Overrides 404 to return json if an api request is made
    """
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template("404.html")

def forbidden(message):
    """
    Returns resource forbidden to json aware applications.
    """
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def unauthorized(message):
    """
    Returns resource unauthorized to json aware applications.
    """
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response
