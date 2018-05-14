#!/bin/sh

source $(pipenv --venv)/bin/activate
gunicorn newscache.app:app
