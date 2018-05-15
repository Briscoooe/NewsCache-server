import os
from flask import jsonify, request, Blueprint
from newsapi import NewsApiClient
from newscache.newspaper_client import download_articles_from_urls
from newscache.constants import *
from newscache.validator import validate_request_params
from newscache.enums import RequestType
from newscache.utils import api_key_is_match
from newscache.decorators import requires_key, handle_exception, log_request
from requests import codes
blueprint = Blueprint('routes', __name__)

api_key = os.environ[API_KEY_ENV_VARIABLE_KEY]
news_api = NewsApiClient(api_key=api_key)


@blueprint.route('/verify', methods=['POST'])
@log_request
def verify_key_matches():
    if api_key_is_match(api_key, request.headers):
        return 'OK', codes.ok
    else:
        return jsonify({'Error': 'News API key is not present or does not match'}), codes.unauthorized


@blueprint.route('/sources', methods=['POST'])
@requires_key(api_key)
@handle_exception
@log_request
def get_sources():
    params = validate_request_params(request.get_json(), RequestType.SOURCES)
    response = news_api.get_sources(
        language=params[LANGUAGES_KEY],
        category=params[CATEGORY_KEY],
        country=params[COUNTRY_KEY]
    )
    response_body = response[SOURCES_KEY]
    response_code = codes.ok

    return jsonify(response_body), response_code


@blueprint.route('/headlines', methods=['POST'])
@requires_key(api_key)
@handle_exception
@log_request
def get_headlines():
    params = validate_request_params(request.get_json(), RequestType.HEADLINES)
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

    return jsonify(response_body), response_code


@blueprint.route('/everything', methods=['POST'])
@requires_key(api_key)
@handle_exception
@log_request
def get_all():
    params = validate_request_params(request.get_json(), RequestType.EVERYTHING)
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

    return jsonify(response_body), response_code


@blueprint.route('/download', methods=['POST'])
@requires_key(api_key)
@log_request
def download_articles():
    body = request.get_json()
    if ARTICLES_KEY not in body:
        return 'No "{}" key found in body'.format(ARTICLES_KEY), codes.bad_request
    if not isinstance(body[ARTICLES_KEY], list):
        return '"{}" key must contain a list of article urls'.format(ARTICLES_KEY), codes.bad_request
    if len(body[ARTICLES_KEY]) <= 0:
        return '"{}" length is 0. Please pass a list of articles'.format(ARTICLES_KEY), codes.bad_request
    articles = download_articles_from_urls(body[ARTICLES_KEY])
    return jsonify({'articles': articles}), codes.ok

