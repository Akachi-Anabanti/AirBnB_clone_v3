#!/usr/bin/python3
"""State View"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    """retrives all states"""

    state_objs = storage.all(State)

    all_states = [state.to_dict() for state in state_objs.values()]
    return jsonify(all_states)


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def get_state(state_id):
    """Retrieves a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """creates a state"""
    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in payload.keys():
        return jsonify({"error": "Missing name"}), 400
    state = State(**payload)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Updates the info about a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]

    for key, value in payload.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
