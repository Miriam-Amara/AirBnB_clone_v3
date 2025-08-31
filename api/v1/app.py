#!/usr/bin/env python3

"""

"""

from dotenv import load_dotenv
from flask import Flask
from typing import Optional
from werkzeug.exceptions import HTTPException
import os

from models import storage
from api.v1.views import app_views


load_dotenv()

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db(exception: Optional[BaseException]) -> None:
    storage.close()

@app.errorhandler(404)
def not_found(error: HTTPException):
    if error.description:
        return {"error": error.description}, 404
    return {"error": "Not found"}, 404

@app.errorhandler(400)
def bad_request(error: HTTPException):
    response = {"message": error.description}
    return response, 400

@app.errorhandler(500)
def server_error(error: HTTPException):
    response = {"message": error.description}
    return response, 500


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
