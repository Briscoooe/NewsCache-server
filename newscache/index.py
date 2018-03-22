import os
from functools import wraps
from flask import Flask, abort, jsonify, request
app = Flask(__name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]

#api_key = os.environ['NEWS_API_KEY'] 

def requires_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get('news-api-key') and request.headers.get('news-api-key') == 'hello':
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated

@app.route('/test')
def test():
    return 'OK'

@app.route('/incomes', methods=['POST'])
@requires_key
def add_income():
    return '', 200