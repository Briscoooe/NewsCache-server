import os
from functools import wraps
from flask import Flask, abort, jsonify, request
from newsapi import NewsApiClient, newsapi_exception
from newscache.np import download_articles_from_urls
from newscache.constants import *
from newscache.validator import validate_request_params
from newscache.enums import RequestType
from requests import codes
from jsonpickle import encode

app = Flask(__name__)

api_key = os.environ[API_KEY_ENV_VARIABLE_KEY]
news_api = NewsApiClient(api_key=api_key)

error_message_format = 'Error: {}'
error_key = 'Error:'


def requires_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get(API_KEY_HEADER_KEY) and request.headers.get(API_KEY_HEADER_KEY) == api_key:
            return f(*args, **kwargs)
        else:
            abort(codes.unauthorized)
    return decorated


@app.route('/test')
def test():
    return 'OK'


@app.errorhandler(codes.not_found)
def page_not_found(e):
    return 'NOT FOUND', codes.not_found

# Add 405 error handler


@app.route('/sources', methods=['POST'])
@requires_key
def get_sources():
    try:
        params = validate_request_params(request.get_json(), RequestType.SOURCES)
        print(params)
        response = news_api.get_sources(
            language=params[LANGUAGES_KEY],
            category=params[CATEGORY_KEY],
            country=params[COUNTRY_KEY]
        )
        response_body = response[SOURCES_KEY]
        response_code = codes.ok
    except (TypeError, ValueError) as e:
        print(error_message_format.format(str(e)))
        response_body = {
            error_key: str(e)
        }
        response_code = codes.bad_request
    except newsapi_exception.NewsAPIException as e:
        print(e)
        response_body = {
            error_key: e.get_message()
        }
        response_code = codes.bad_request
    except Exception as e:
        print(error_message_format.format(str(e)))
        response_body = {
            error_key: str(e)
        }
        response_code = codes.server_error

    return jsonify(response_body), response_code


@app.route('/headlines', methods=['POST'])
@requires_key
def get_headlines():
    try:
        params = validate_request_params(request.get_json(), RequestType.HEADLINES)
        print(params)
        response = news_api.get_top_headlines(
            q=params[QUERY_KEY],
            sources=params[SOURCES_KEY],
            language=params[LANGUAGES_KEY],
            country=params[COUNTRY_KEY],
            category=params[COUNTRY_KEY],
            page_size=params[PAGE_SIZE_KEY],
            page=params[PAGE_KEY]
        )
        response_body = response[ARTICLES_KEY]
        response_code = codes.ok
    except (TypeError, ValueError) as e:
        print(error_message_format.format(str(e)))
        response_body = {
            error_key: str(e)
        }
        response_code = codes.bad_request
    except newsapi_exception.NewsAPIException as e:
        print(e)
        response_body = {
            error_key: e.get_message()
        }
        response_code = codes.bad_request
    except Exception as e:
        print(error_message_format.format(str(e)))
        response_body = {
            error_key: str(e)
        }
        response_code = codes.server_error

    return jsonify(response_body), response_code


@app.route('/everything', methods=['POST'])
@requires_key
def get_all():
    try:
        params = validate_request_params(request.get_json(), RequestType.EVERYTHING)
        print(params)
        response = news_api.get_everything(
            q=params[QUERY_KEY],
            sources=params[SOURCES_KEY],
            domains=params[DOMAINS_KEY],
            from_param=params[FROM_KEY],
            to=params[TO_KEY],
            language=params[LANGUAGES_KEY],
            sort_by=params[SORT_BY_KEY],
            page_size=params[PAGE_SIZE_KEY],
            page=params[PAGE_KEY]
        )
        response_body = response[ARTICLES_KEY]
        response_code = codes.ok
    except (TypeError, ValueError) as e:
        print(error_message_format.format(str(e)))
        response_body = {
            error_key: str(e)
        }
        response_code = codes.bad_request
    except newsapi_exception.NewsAPIException as e:
        print(e)
        response_body = {
            error_key: e.get_message()
        }
        response_code = codes.bad_request
    except Exception as e:
        print(error_message_format.format(str(e)))
        response_body = {
            error_key: str(e)
        }
        response_code = codes.server_error

    return jsonify(response_body), response_code


@app.route('/download', methods=['POST'])
@requires_key
def download_articles():
    body = request.get_json()
    if ARTICLES_KEY not in body:
        return 'No "{}" key found in body'.format(ARTICLES_KEY), codes.bad_request
    if not isinstance(body[ARTICLES_KEY], list):
        return '"{}" key must contain a list of article urls'.format(ARTICLES_KEY), codes.bad_request
    if len(body[ARTICLES_KEY]) <= 0:
        return '"{}" length is 0. Please pass a list of articles'.format(ARTICLES_KEY), codes.bad_request
    articles = download_articles_from_urls(body[ARTICLES_KEY])
    print(encode(articles))
    return encode(articles), codes.ok


if __name__ == '__main__':
    app.run(debug=True)
