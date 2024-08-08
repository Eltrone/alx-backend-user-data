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
        Détermine si chemin donné nécessite une authentification en vérifiant
        s'il est dans la liste des chemins exclus.

        Retourne True si le chemin n'est pas dans la liste
        des chemins exclus ou si
        certaines conditions sont vraies (voir ci-dessous).
        """
        if path is None:
            # Retourne True si aucun chemin n'est fourni
            return True
        if not excluded_paths:
            # Retourne True si la liste des chemins exclus est vide ou None
            return True

        # Normalise le chemin pour terminer par un slash pour la cohérence
        path = path if path.endswith('/') else path + '/'

        # Normalise les chemins exclus qu'ils se terminent tous par slash
        normalized_excluded_paths = [p if p.endswith(
            '/') else p + '/' for p in excluded_paths]

        # Vérifie si le chemin actuel commence par un chemin exclu
        is_excluded = any(
            path.startswith(excluded_path)
            for excluded_path in normalized_excluded_paths
        )
        return not is_excluded

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

    def authorization_header(self, request=None) -> str:
        """
        Récupère l'en-tête d'autorisation de la requête, si elle existe.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)
