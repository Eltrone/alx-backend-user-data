#!/usr/bin/env python3
"""
Initialise et gère une API Flask avec diverses méthodes d'authentification.
"""

from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
if getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "auth":
    auth = Auth()
elif getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()
elif getenv("AUTH_TYPE") == "session_exp_auth":
    auth = SessionExpAuth()

@app.before_request
def before_request_func():
    """
    Vérifie l'authentification avant chaque requête.
    """
    if auth and auth.require_auth(
        request.path, 
        ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/', 
         '/api/v1/auth_session/login/']
    ):
        if not auth.authorization_header(request):
            abort(401)
        if not auth.current_user(request):
            abort(403)

@app.errorhandler(404)
def not_found(error):
    """ Retourne erreur 404 si la ressource n'est pas trouvée. """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    """ Retourne erreur 401 si l'utilisateur n'est pas authentifié. """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """ Retourne erreur 403 si l'accès est refusé. """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    app.run(host=getenv("API_HOST", "0.0.0.0"), port=getenv("API_PORT", "5000"))

