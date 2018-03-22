import os
from functools import wraps
from flask import Flask, abort, jsonify, request
from newsapi import NewsApiClient


app = Flask(__name__)
api_key = os.environ['NEWS_API_KEY'] 
api_key_header_name = 'X-Api-Key'
newsapi = NewsApiClient(api_key=api_key)

def requires_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get(api_key_header_name) and request.headers.get(api_key_header_name) == api_key: 
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated

@app.route('/sources/', methods=['POST'])
@requires_key
def get_sources():
    sources = newsapi.get_sources()
    return jsonify(sources), 200

if __name__ == '__main__':
    app.run(debug=True)
