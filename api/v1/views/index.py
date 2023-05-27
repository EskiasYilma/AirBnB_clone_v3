#!/usr/bin/python3
"""
API page
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def get_status():
    """
    get api status
    """
    return jsonify({"status": "OK"})
