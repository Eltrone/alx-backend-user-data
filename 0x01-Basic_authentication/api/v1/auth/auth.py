# api/v1/auth/auth.py
from flask import request
from typing import List, TypeVar

User = TypeVar('User')  # Utilisé pour le type de retour de current_user


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Vérifie si le chemin requiert une authentification. """
        return False  # Toujours False pour l'instant

    def authorization_header(self, request=None) -> str:
        """ Récupère l'entête d'autorisation de la requête. """
        return None  # Toujours None pour l'instant

    def current_user(self, request=None) -> User:
        """ Récupère l'utilisateur courant de la requête. """
        return None  # Toujours None pour l'instant
