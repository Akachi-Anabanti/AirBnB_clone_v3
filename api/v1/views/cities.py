#!/usr/bin/python3
"""State View"""

from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states/<string:state_id>/cities",
                 strict_slashes=False)
def get_all_cities(state_id):
    """retrives all cities"""

    state = storage.get(State,state_id)
    if not state:
        abort(404)

    city_list = state.cities
    all_cities = [city.to_dict() for city in city_list]
    return jsonify(all_cities)


@app_views.route("/cities/<string:city_id>", strict_slashes=False)
def get_city(city_id):
    """Retrieves a city"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route("/states/<string:state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """creates a city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in payload.keys():
        return jsonify({"error": "Missing name"}), 400
    payload["state_id"] = state_id
    city = City(**payload)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Updates the info about a city"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]

    for key, value in payload.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
