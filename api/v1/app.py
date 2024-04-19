#!/usr/bin/python3
"""Flask app"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_notfound(e):
    """not found error"""
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def teardown_app(exc):
    """Closes the app context"""
    storage.close()


if __name__ == "__main__":
    app.run(host=os.environ.get("HBNB_API_HOST", '0.0.0.0'),
            port=os.environ.get("HBNB_API_PORT", 5000),
            threaded=True)
