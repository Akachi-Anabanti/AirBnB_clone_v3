#!/usr/bin/python3
"""Amenity View"""

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route("/amenities", strict_slashes=False)
def get_all_amenities():
    """retrives all amenities"""

    amenity_objs = storage.all(Amenity)

    all_amenities = [amenity.to_dict() for amenity in amenity_objs.values()]
    return jsonify(all_amenities)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """creates a amenity"""
    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in payload.keys():
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**payload)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates the info about a amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]

    for key, value in payload.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
