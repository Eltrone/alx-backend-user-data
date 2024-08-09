#!/usr/bin/env python3
"""
Module des routes pour l'API
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth_type = os.getenv("AUTH_TYPE")
if auth_type == "session_exp_auth":
    auth = SessionExpAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
elif auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "auth":
    auth = Auth()
else:
    auth = None


@app.before_request
def before_request_func():
    """ Fonction exécutée avant chaque requête """
    if auth is None:
        return
    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/',
                                            '/api/v1/auth_session/login/']):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if not auth.current_user(request):
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Gestionnaire pour les erreurs 404 """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Fonction pour les erreurs d'autorisation """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Fonction pour les erreurs d'accès interdit """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
