from flask import Flask
import newscache.routes
import newscache.error_handlers
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.register_blueprint(newscache.routes.blueprint)
app.register_blueprint(newscache.error_handlers.blueprint)

if __name__ == '__main__':
    handler = RotatingFileHandler('newscache.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug=True)
