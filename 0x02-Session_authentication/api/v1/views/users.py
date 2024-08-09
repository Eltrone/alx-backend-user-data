#!/usr/bin/env python3
""" Module de gestion des utilisateurs """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users() -> str:
    users = [user.to_json() for user in User.all()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str = None) -> str:
    if user_id == "me" and not request.current_user:
        abort(404)
    user = User.get(user_id) or abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    User.get(user_id) or abort(404)
    User.remove()
    return jsonify({}), 200

# Créer un utilisateur


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    try:
        data = request.get_json() or abort(400, 'Wrong format')
        if not all(data.get(k) for k in ['email', 'password']):
            abort(400, 'Missing email or password')
        user = User(**data)
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Mettre à jour un utilisateur


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    user = User.get(user_id) or abort(404)
    data = request.get_json() or abort(400, 'Wrong format')
    for field in ['first_name', 'last_name']:
        if data.get(field):
            setattr(user, field, data[field])
    user.save()
    return jsonify(user.to_json()), 200
