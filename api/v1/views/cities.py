#!/usr/bin/python3
"""
Handles all default RESTFul API actions for State objects
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from flask import request, jsonify
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound
import os

methods = ["GET", "POST", "DELETE", "PUT"]


@app_views.route("/states/<state_id>/cities", methods=[methods[0]])
def all_cities(state_id=None):
    """
    Get all Cities with state_id
    """
    states = storage.get(State, state_id)
    if states:
        temp = []
        for i in states.cities:
            temp.append(i.to_dict())
        if len(temp) != 0:
            return jsonify(temp)
    raise NotFound()


@app_views.route("/cities/<city_id>", methods=[methods[0]])
def one_city(city_id=None):
    """
    Get a single City with city_id
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    raise NotFound()


@app_views.route("/states/<state_id>/cities", methods=[methods[1]])
def new_city(state_id=None):
    """
    Adds new City to storage
    """
    new_ct = None
    try:
        new_ct = request.get_json()
    except Exception:
        pass
    if new_ct is None or type(new_ct) is not dict:
        raise BadRequest(description="Not a JSON")
    if 'name' not in new_ct:
        raise BadRequest(description="Missing name")
    states = storage.get(State, state_id)
    if not states:
        raise NotFound()
    new_ct['state_id'] = state_id
    city = City(**new_ct)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=[methods[2]])
def delete_city(city_id=None):
    """
    Removes City from storage by city_id
    """
    city = storage.get(City, city_id)
    if city:
        # if os.getenv('HBNB_TYPE_STORAGE') != "db":
        for i in storage.all(Place).values():
            if i.city_id == city_id:
                for j in storage.all(Review).values():
                    if j.place_id == i.id:
                        storage.delete(j)
                storage.delete(i)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route("/cities/<city_id>", methods=[methods[3]])
def update_city(city_id=None):
    """
    Updates City in storage by city_id
    """
    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    upd_ct = None
    city = storage.get(City, city_id)
    if city is None:
        raise NotFound()
    try:
        upd_ct = request.get_json()
    except Exception:
        pass
    if upd_ct is None or type(upd_ct) is not dict:
        raise BadRequest(description="Not a JSON")
    for i, j in upd_ct.items():
        if i not in ignore_keys:
            setattr(city, i, j)
    city.save()
    return jsonify(city.to_dict()), 200
