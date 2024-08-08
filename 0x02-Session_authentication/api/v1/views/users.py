# !/usr/bin/env python3
""" Module of Users views
"""

from models.user import User
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    if user_id == "me":
        if not hasattr(request, 'current_user') or \
                request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    rj = None
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if not rj.get("email"):
        return jsonify({'error': "email missing"}), 400
    if not rj.get("password"):
        return jsonify({'error': "password missing"}), 400
    try:
        user = User()
        user.email = rj['email']
        user.password = rj['password']
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': "Can't create User: {}".format(e)}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    user.first_name = rj.get('first_name', user.first_name)
    user.last_name = rj.get('last_name', user.last_name)
    user.save()
    return jsonify(user.to_json()), 200
