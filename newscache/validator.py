from newscache.constants import *
from newscache.enums import RequestType


def get_key_value(key, request_params):
    return request_params[key] if key in request_params else None


def validate_request_params(request_params, request_type):
    valid_params = {}
    valid_params[LANGUAGES_KEY] = get_key_value(LANGUAGES_KEY, request_params)
    if request_type == RequestType.SOURCES or request_type == RequestType.HEADLINES:
        valid_params[CATEGORY_KEY] = get_key_value(CATEGORY_KEY, request_params)
        valid_params[COUNTRY_KEY] = get_key_value(COUNTRY_KEY, request_params)

    if request_type == RequestType.HEADLINES or request_type == RequestType.EVERYTHING:
        valid_params[QUERY_KEY] = get_key_value(QUERY_KEY, request_params)
        valid_params[SOURCES_KEY] = get_key_value(SOURCES_KEY, request_params)
        valid_params[PAGE_SIZE_KEY] = get_key_value(PAGE_SIZE_KEY, request_params)
        valid_params[PAGE_KEY] = get_key_value(PAGE_KEY, request_params)

    if request_type == RequestType.HEADLINES:
        valid_params[DOMAINS_KEY] = get_key_value(DOMAINS_KEY, request_params)
        valid_params[FROM_KEY] = get_key_value(FROM_KEY, request_params)
        valid_params[TO_KEY] = get_key_value(TO_KEY, request_params)
        valid_params[SORT_BY_KEY] = get_key_value(SORT_BY_KEY, request_params)

    return valid_params
