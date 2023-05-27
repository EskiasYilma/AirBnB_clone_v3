#!/usr/bin/python3
"""
API page
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """
    get api status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    get stats from all models
    """
    models_dict = {"Amenity": Amenity, "City": City,
                   "Place": Place, "Review": Review,
                   "State": State, "User": User}
    for i, j in models_dict.items():
        models_dict[i] = storage.count(j)
    return jsonify(models_dict)
