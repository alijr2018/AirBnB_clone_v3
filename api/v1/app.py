#!/usr/bin/python3
"""Flask Application."""
from os import environ
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(error):
    """Close Storage."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
