from flask import current_app, make_response, jsonify
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == current_app.config['USERNAME']:
        return current_app.config['PASSWORD']
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from showing the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
