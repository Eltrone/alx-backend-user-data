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
    Classe Auth pour gérer mécanismes d'authentification de base dans l'API.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Détermine si le chemin donné nécessite une authentification.
        Retourne toujours False pour le moment.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Récupère l'en-tête d'autorisation de la requête, si elle existe.
        Retourne None pour le moment.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Identifie l'utilisateur courant à partir de la requête.
        Retourne None pour le moment.
        """
        return None
