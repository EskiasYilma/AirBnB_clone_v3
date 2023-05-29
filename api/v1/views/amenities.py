#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Amenity objects
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import request, jsonify
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


methods = ["GET", "POST", "DELETE", "PUT"]


@app_views.route("/amenities/", methods=[methods[0]])
@app_views.route("/amenities", methods=[methods[0]])
@app_views.route("/amenities/<amenity_id>", methods=[methods[0]])
def all_amenities(amenity_id=None):
    """
    Get all Amenitys or a single Amenity with amenity_id
    """
    amenities = storage.all(Amenity).values()
    if amenity_id is not None:
        temp = []
        for i in amenities:
            if i.id == amenity_id:
                temp.append(i)
        if len(temp) != 0:
            return jsonify(temp[0].to_dict())
        raise NotFound()
    all_amenities_dict = []
    for i in amenities:
        all_amenities_dict.append(i.to_dict())
    return jsonify(all_amenities_dict)


@app_views.route("/amenities/", methods=[methods[1]])
def new_amenity():
    """
    Adds new Amenity to storage
    """
    new_am = None
    try:
        new_am = request.get_json()
    except Exception:
        pass
    if new_am is None or type(new_am) is not dict:
        raise BadRequest(description="Not a JSON")
    if 'name' not in new_am:
        raise BadRequest(description="Missing name")
    amenity = Amenity(**new_am)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=[methods[2]])
def delete_amenity(amenity_id=None):
    """
    Removes Amenity from storage by amenity_id
    """
    amenities = storage.all(Amenity).values()
    # if amenity_id is not None:
    temp = []
    for i in amenities:
        if i.id == amenity_id:
            temp.append(i)
    if len(temp) != 0:
        storage.delete(temp[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()
    # raise NotFound()


@app_views.route("/amenities/<amenity_id>", methods=[methods[3]])
def update_amenity(amenity_id=None):
    """
    Updates Amenity in storage by amenity_id
    """
    amenities = storage.all(Amenity).values()
    ignore_keys = ["id", "created_at", "updated_at"]
    upd_am = None
    # if amenity_id is not None:
    temp = []
    for i in amenities:
        if i.id == amenity_id:
            try:
                upd_am = request.get_json()
            except Exception:
                pass
            if upd_am is None or type(upd_am) is not dict:
                raise BadRequest(description="Not a JSON")
            temp.append(i)
    if len(temp) != 0:
        existing_st = temp[0]
        for i, j in upd_am.items():
            if i not in ignore_keys:
                setattr(existing_st, i, j)
        existing_st.save()
        return jsonify(existing_st.to_dict()), 200
    raise NotFound()
    # raise NotFound()
