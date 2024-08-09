#!/usr/bin/env python3
""" Module des vues pour les utilisateurs
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Renvoie :
      - Liste de tous les objets User représentés en JSON
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Paramètre de chemin :
      - ID de l'utilisateur
    Renvoie :
      - Objet User représenté en JSON
      - 404 si l'ID de l'utilisateur n'existe pas
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    if request.current_user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Paramètre de chemin :
      - ID de l'utilisateur
    Renvoie :
      - JSON vide si l'utilisateur a été correctement supprimé
      - 404 si l'ID de l'utilisateur n'existe pas
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    Corps JSON :
      - email
      - mot de passe
      - nom (optionnel)
      - prénom (optionnel)
    Renvoie :
      - Objet User représenté en JSON
      - 400 si la création du nouvel utilisateur échoue
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Format incorrect"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email manquant"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "mot de passe manquant"
    if error_msg is None:
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Impossible de créer l'utilisateur : {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Paramètre de chemin :
      - ID de l'utilisateur
    Corps JSON :
      - nom (optionnel)
      - prénom (optionnel)
    Renvoie :
      - Objet User représenté en JSON
      - 404 si l'ID de l'utilisateur n'existe pas
      - 400 si la mise à jour de l'utilisateur échoue
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Format incorrect"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
