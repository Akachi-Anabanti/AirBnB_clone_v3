#!/usr/bin/python3
"""User View"""

from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users", strict_slashes=False)
def get_all_users():
    """retrives all users"""

    user_objs = storage.all(User)

    all_users = [user.to_dict() for user in user_objs.values()]
    return jsonify(all_users)


@app_views.route("/users/<string:user_id>", strict_slashes=False)
def get_user(user_id):
    """Retrieves a user"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """creates a user"""
    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if "email" not in payload.keys():
        return jsonify({"error": "Missing email"}), 400
    if "password" not in payload.keys():
        return jsonify({"error": "Missing password"}), 400
    user = User(**payload)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Updates the info about a user"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    try:
        payload = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]

    for key, value in payload.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
