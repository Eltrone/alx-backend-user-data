#!/usr/bin/env python3
"""
Ce module définit la classe Auth utilisée
pour gérer l'authentification dans l'API.
"""

from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """
    Classe Auth pour gérer les mécanismes d'authentification
    de base dans l'API.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Détermine si chemin donné nécessite une authentification en vérifiant
        s'il est dans la liste des chemins exclus.

        Retourne True si le chemin n'est pas dans la liste
        des chemins exclus ou si
        certaines conditions sont vraies (voir ci-dessous).
        """
        if path is None: 
            return True
        if not excluded_paths:
            return True

        path = path if path.endswith('/') else path + '/'

        normalized_excluded_paths = [p if p.endswith(
            '/') else p + '/' for p in excluded_paths]

        is_excluded = any(
            path.startswith(excluded_path)
            for excluded_path in normalized_excluded_paths
        )
        return not is_excluded

    def current_user(self, request=None) -> User:
        """
        Identifie l'utilisateur courant à partir de la requête.
        Retourne None pour le moment.
        """
        return None

    def authorization_header(self, request=None) -> str:
        """
        Récupère l'en-tête d'autorisation de la requête, si elle existe.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)
