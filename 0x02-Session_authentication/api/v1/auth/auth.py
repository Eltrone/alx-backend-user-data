#!/usr/bin/env python3
"""gérer l'authentification de l'API"""
from typing import List, TypeVar
from flask import request
from os import getenv


class Auth():
    """Classe Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Fonction require_auth"""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Fonction authorization_header"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Fonction current_user"""
        return None

    def session_cookie(self, request=None):
        """Fonction session_cookie"""
        if request:
            session_name = getenv("SESSION_NAME")
            return request.cookies.get(session_name, None)
