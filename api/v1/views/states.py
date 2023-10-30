#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieve the list of all State objects.
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieve a specific State."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Delete a State Object. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})



@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a new State object. """
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object by state_id. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
