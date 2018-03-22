#!/bin/sh
export FLASK_APP=./newscache/index.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0