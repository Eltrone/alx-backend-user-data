#!/usr/bin/env python3
"""
Basic Flask app for user authentication service.
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """Return a welcome message."""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user via the POST method."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
