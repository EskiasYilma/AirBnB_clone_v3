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
from models.user import User
from flask import request, jsonify
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound
import os

methods = ["GET", "POST", "DELETE", "PUT"]


@app_views.route("/cities/<city_id>/places", methods=[methods[0]])
@app_views.route("/places/<place_id>", methods=[methods[0]],
                 strict_slashes=False)
def all_places(city_id=None, place_id=None):
    """
    Get all Places or a single Place with place_id or city_id
    """
    if city_id is not None:
        city = storage.get(City, city_id)
        if city:
            temp = []
            if os.getenv('HBNB_TYPE_STORAGE') == "db":
                for i in city.places:
                    temp.append(i.to_dict())
            else:
                for i in storage.all(Place).values():
                    if i.city_id == city_id:
                        temp.append(i.to_dict())
            if len(temp) != 0:
                return jsonify(temp)
    elif place_id is not None:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
    raise NotFound()


@app_views.route("/cities/<city_id>/places", methods=[methods[1]],
                 strict_slashes=False)
def new_place(city_id=None):
    """
    Adds new Place to storage
    """
    new_pl = None
    try:
        new_pl = request.get_json()
    except Exception:
        pass
    if new_pl is None or type(new_pl) is not dict:
        raise BadRequest(description="Not a JSON")
    if 'name' not in new_pl:
        raise BadRequest(description="Missing name")
    if 'user_id' not in new_pl:
        raise BadRequest(description="Missing user_id")
    city = storage.get(City, city_id)
    if city is None:
        raise NotFound()
    user = storage.get(User, new_pl.get("user_id"))
    if user is None:
        raise NotFound()
    new_pl["city_id"] = city_id
    place = Place(**new_pl)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=[methods[2]],
                 strict_slashes=False)
def delete_place(place_id=None):
    """
    Removes Place from storage by place_id
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route("/places/<place_id>", methods=[methods[3]],
                 strict_slashes=False)
def update_place(place_id=None):
    """
    Updates Place in storage by place_id
    """
    ignore_keys = ["id", "user_id", "city_id", "email",
                   "created_at", "updated_at"]
    upd_usr = None
    place = storage.get(Place, place_id)
    if place:
        try:
            upd_usr = request.get_json()
        except Exception:
            pass
        if upd_usr is None or type(upd_usr) is not dict:
            raise BadRequest(description="Not a JSON")
        for i, j in upd_usr.items():
            if i not in ignore_keys:
                setattr(place, i, j)
        place.save()
        return jsonify(place.to_dict()), 200
    raise NotFound()
