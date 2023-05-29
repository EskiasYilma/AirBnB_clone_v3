#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """
    Close storage
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    Error 404 - Not Found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)
