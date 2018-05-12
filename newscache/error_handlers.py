from requests import codes
from flask import Blueprint
blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(codes.not_found)
def page_not_found(e):
    return 'Nothing to see here', codes.not_found


@blueprint.app_errorhandler(codes.unauthorized)
def unauthorized(e):
    return 'Unauthorized', codes.unauthorized


@blueprint.app_errorhandler(codes.method_not_allowed)
def method_not_allowed(e):
    return 'Method not allowed', codes.method_not_allowed

