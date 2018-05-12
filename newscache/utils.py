from newscache.constants import API_KEY_HEADER_KEY


def api_key_is_match(api_key, headers):
    return headers.get(API_KEY_HEADER_KEY) and headers.get(API_KEY_HEADER_KEY) == api_key
