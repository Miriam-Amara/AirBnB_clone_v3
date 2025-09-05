#!/usr/bin/env python3

"""

"""

from dotenv import load_dotenv
from flask import Flask, request, abort
from flask_bcrypt import Bcrypt # type: ignore
from flask_cors import CORS
from typing import Optional
from werkzeug.exceptions import HTTPException
import logging
import os

from logging_config import setup_logging
from models import storage
from api.v1.views import app_views


load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

app.register_blueprint(app_views)
bycrypt = Bcrypt(app)

CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

auth = None
if os.getenv("AUTH_TYPE") == "jwt_bearer":
    from api.v1.auth.jwt_bearer import JWTBearerAuth
    auth = JWTBearerAuth()

if os.getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

@app.before_request
def verify_auth():
    """ """
    if auth is None:
        return
    if not auth.require_auth(
        request.path,
        ["/api/v1/status/", "/api/v1/stats/",
         "/api/v1/login/", "/api/v1/register/"]
    ):
        return
    if not auth.authorization_header(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)


@app.teardown_appcontext
def close_db(exception: Optional[BaseException]) -> None:
    storage.close()

@app.errorhandler(400)
def bad_request(error: HTTPException):
    response = {"message": error.description}
    return response, 400

@app.errorhandler(401)
def unauthorized(error: HTTPException):
    return {"error": "Unauthorized"}, 401

@app.errorhandler(403)
def forbidden(error: HTTPException):
    return {"error": "Forbidden"}, 403

@app.errorhandler(404)
def not_found(error: HTTPException):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def server_error(error: HTTPException):
    response = {"message": error.description}
    return response, 500


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
