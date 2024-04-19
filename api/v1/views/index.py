#!/usr/bin/python3
"""Index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.review import Review
from models.user import User
from models.place import Place
from models.amenity import Amenity


@app_views.route("/status")
def status():
    """Displays status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def obj_stats():
    """Get the number of each object"""
    obj = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User),
            "places": storage.count(Place)
            }
    return jsonify(obj)
