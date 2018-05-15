from requests import codes
from flask import Blueprint, jsonify
blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(codes.not_found)
def page_not_found(e):
    return jsonify({'message': 'Nothing to see here'}), codes.not_found


@blueprint.app_errorhandler(codes.unauthorized)
def unauthorized(e):
    return jsonify({'message': 'Unauthorized'}), codes.unauthorized


@blueprint.app_errorhandler(codes.method_not_allowed)
def method_not_allowed(e):
    return jsonify({'message': 'Method not allowed'}), codes.method_not_allowed


@blueprint.app_errorhandler(codes.server_error)
def server_error(e):
    return jsonify({'message': 'Internal server error'}), codes.server_error
