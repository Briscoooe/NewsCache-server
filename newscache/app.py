from flask import Flask
import newscache.routes
import newscache.http_error_handlers

app = Flask(__name__)
app.register_blueprint(newscache.routes.blueprint)
app.register_blueprint(newscache.http_error_handlers.blueprint)

if __name__ == '__main__':
    app.run(debug=True)
