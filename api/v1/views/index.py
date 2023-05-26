#!/usr/bin/python3
"""
API page
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def app_views():
    """
    Simply returns the state of the api.
    """
    return jsonify({"status": "OK"})
