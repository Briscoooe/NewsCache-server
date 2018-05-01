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


@app.route('/test')
def test():
    return 'OK'

@app.route('/sources', methods=['POST'])
@requires_key
def get_sources():
    response = newsapi.get_sources()
    response_code = 200
    response_body = ''
    if (response['status'] == 'ok'):
        response_body = response['sources']
    else:
        response_body = response
        response_code = 400 
    return jsonify(response_body), response_code


supported_categories = ['business', 'entertainment', 'health', 'science', 'sports', 'technology']

def format_body_parameters(body):
    if ('sources' in body):
        body['sources'] =  ', '.join([str(source) for source in body['sources']])
    if ('category' in body and body['category'] not in supported_categories):
        body['category'] = ''
    
@app.route('/headlines', methods=['POST'])
@requires_key
def get_headlines():
    body = request.get_json()
    response = newsapi.get_top_headlines(q=body['q'],
        sources=body['sources'],
        #country=body['country'],
        language=body['language'],
        #category=body['category']
    )
    response_code = 200
    response_body = ''
    if (response['status'] == 'ok'):
        response_body = response['articles']
    else:
        response_body = response
        response_code = 400 
    return jsonify(response_body), response_code


@app.route('/download', methods=['POST'])
@requires_key
def download_articles():
    body = request.get_json()
    return jsonify(body['urls'])

@app.route('/all', methods=['POST'])
@requires_key
def get_all():
    body = request.get_json()
    format_body_parameters(body)
    response = newsapi.get_everything(q=body['q'], 
            sources=body['sources'], 
            page=body['page'],
            page_size=body['page_size'])
    response_code = 200
    response_body = ''
    if (response['status'] == 'ok'):
        response_body = response['articles']
    else:
        response_body = response
        response_code = 400 
    return jsonify(response_body), response_code

if __name__ == '__main__':
    app.run(debug=True)
