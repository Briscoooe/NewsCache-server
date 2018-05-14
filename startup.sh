#!/bin/sh

source $(pipenv --venv)/bin/activate
gunicorn -w 4 newscache.app:app
