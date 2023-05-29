#!/usr/bin/python3
"""
Handles all default RESTFul API actions for User objects
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import request, jsonify
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound
import os

methods = ["GET", "POST", "DELETE", "PUT"]


@app_views.route("/users", methods=[methods[0]],
                 strict_slashes=False)
@app_views.route("/users/<user_id>", methods=[methods[0]],
                 strict_slashes=False)
def all_users(user_id=None):
    """
    Get all Users or a single User with user_id
    """
    if user_id is not None:
        user = storage.get(User, user_id)
        if user:
            return jsonify(user.to_dict())
        return NotFound()
    temp = []
    for i in storage.all(User).values():
        temp.append(i.to_dict())
    if temp:
        return jsonify(temp)
    raise NotFound()


@app_views.route("/users", methods=[methods[1]],
                 strict_slashes=False)
def new_user(user_id=None):
    """
    Adds new User to storage
    """
    new_usr = None
    try:
        new_usr = request.get_json()
    except Exception:
        pass
    if new_usr is None or type(new_usr) is not dict:
        raise BadRequest(description="Not a JSON")
    if 'email' not in new_usr:
        raise BadRequest(description="Missing email")
    if 'password' not in new_usr:
        raise BadRequest(description="Missing password")
    user = User(**new_usr)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=[methods[2]],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    Removes User from storage by user_id
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route("/users/<user_id>", methods=[methods[3]],
                 strict_slashes=False)
def update_user(user_id=None):
    """
    Updates User in storage by user_id
    """
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    upd_usr = None
    user = storage.get(User, user_id)
    if user:
        try:
            upd_usr = request.get_json()
        except Exception:
            pass
        if upd_usr is None or type(upd_usr) is not dict:
            raise BadRequest(description="Not a JSON")
        for i, j in upd_usr.items():
            if i not in ignore_keys:
                setattr(user, i, j)
        user.save()
        return jsonify(user.to_dict()), 200
    raise NotFound()
