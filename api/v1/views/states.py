#!/usr/bin/python3
"""
Handles all default RESTFul API actions for State objects
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, jsonify
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


methods = ["GET", "POST", "DELETE", "PUT"]


@app_views.route("/states/", methods=[methods[0]])
@app_views.route("/states/<state_id>", methods=[methods[0]])
def all_states(state_id=None):
    """
    Get all States or a single State with state_id
    """
    states = storage.all(State).values()
    if state_id is not None:
        temp = []
        for i in states:
            if i.id == state_id:
                temp.append(i)
        if len(temp) != 0:
            return jsonify(temp[0].to_dict())
        raise NotFound()
    all_states_dict = []
    for i in states:
        all_states_dict.append(i.to_dict())
    return jsonify(all_states_dict)


@app_views.route("/states/", methods=[methods[1]])
def new_state():
    """
    Adds new State to storage
    """
    new_st = None
    try:
        new_st = request.get_json()
    except Exception:
        pass
    if new_st is None or type(new_st) is not dict:
        raise BadRequest(description="Not a JSON")
    if 'name' not in new_st:
        raise BadRequest(description="Missing name")
    state = State(**new_st)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=[methods[2]])
def delete_state(state_id=None):
    """
    Removes State from storage by state_id
    """
    states = storage.all(State).values()
    # if state_id is not None:
    temp = []
    for i in states:
        if i.id == state_id:
            temp.append(i)
    if len(temp) != 0:
        storage.delete(temp[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()
    # raise NotFound()


@app_views.route("/states/<state_id>", methods=[methods[3]])
def update_state(state_id=None):
    """
    Updates State in storage by state_id
    """
    states = storage.all(State).values()
    ignore_keys = ["id", "created_at", "updated_at"]
    upd_st = None
    # if state_id is not None:
    temp = []
    for i in states:
        if i.id == state_id:
            try:
                upd_st = request.get_json()
            except Exception:
                pass
            if upd_st is None or type(upd_st) is not dict:
                raise BadRequest(description="Not a JSON")
            temp.append(i)
    if len(temp) != 0:
        existing_st = temp[0]
        for i, j in upd_st.items():
            if i not in ignore_keys:
                setattr(existing_st, i, j)
        existing_st.save()
        return jsonify(existing_st.to_dict()), 200
    raise NotFound()
    # raise NotFound()
