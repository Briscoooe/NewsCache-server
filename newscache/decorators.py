from flask import abort, jsonify, request
from functools import wraps
from newsapi.newsapi_exception import NewsAPIException
from newscache.utils import api_key_is_match
from requests import codes

error_message_format = 'Error: {}'
error_key = 'Error:'


def exception_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (TypeError, ValueError) as e:
            print(error_message_format.format(str(e)))
            response_body = {
                error_key: str(e)
            }
            response_code = codes.bad_request
            return jsonify(response_body), response_code
        except NewsAPIException as e:
            print(e)
            response_body = {
                error_key: e.get_message()
            }
            response_code = codes.bad_request
            return jsonify(response_body), response_code
        except Exception as e:
            print(error_message_format.format(str(e)))
            response_body = {
                error_key: str(e)
            }
            response_code = codes.server_error
            return jsonify(response_body), response_code

    return wrapper


def requires_key(api_key):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if api_key_is_match(api_key, request.headers):
                return f(*args, **kwargs)
            else:
                abort(codes.unauthorized)

        return decorated_function
    return decorator
