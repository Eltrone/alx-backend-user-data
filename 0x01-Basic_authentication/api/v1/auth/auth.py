#!/usr/bin/env python3
"""
Ce module définit la classe Auth utilisée
pour gérer l'authentification dans l'API.
"""

from flask import request
from typing import List, TypeVar

User = TypeVar('User')  # Utilisé pour le type de retour de current_user


class Auth:
    """
    Classe Auth pour gérer les mécanismes d'authentification
    de base dans l'API.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Détermine si le chemin donné nécessite une authentification
        en vérifiant s'il est dans la liste des chemins exclus.
        Retourne True si le chemin n'est pas dans la liste des
        chemins exclus ou si certaines conditions sont vraies
        (voir ci-dessous).
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        # Normaliser le chemin pour la tolérance au slash
        path = path.strip('/') + '/'
        for pattern in excluded_paths:
            if pattern.endswith('/'):
                pattern = pattern.rstrip('/')
            if path.startswith(pattern + '/') or path == pattern + '/':
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Récupère l'en-tête d'autorisation de la requête,
        si elle existe.
        Retourne None pour le moment.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Identifie l'utilisateur courant à partir de la requête.
        Retourne None pour le moment.
        """
        return None
