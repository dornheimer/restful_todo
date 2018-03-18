from flask import Blueprint, jsonify, make_response

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@bp.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
