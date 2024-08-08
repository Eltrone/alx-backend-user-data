#!/usr/bin/env python3
# Gestion des routes pour l'API
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Configuration de l'authentification
auth = None
if os.getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif os.getenv("AUTH_TYPE") == "auth":
    auth = Auth()
elif os.getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()

# Vérification avant chaque requête


@app.before_request
def check_request():
    if auth and auth.require_auth(request.path, ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/', '/api/v1/auth_session/login/']):
        if auth.authorization_header(request) is None:
            abort(401)
        if not auth.current_user(request):
            abort(403)

# Gestionnaires d'erreurs


@app.errorhandler(404)
def handle_404(error) -> str:
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def handle_401(error) -> str:
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_403(error):
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(host=getenv("API_HOST", "0.0.0.0"),
            port=getenv("API_PORT", "5000"))
