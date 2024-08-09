#!/usr/bin/env python3
"""Module gérant l'authentification par session."""

from api.v1.auth.auth import Auth
from typing import TypeVar
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Gestion des sessions utilisateurs."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Crée une session pour ID user donné et renvoie ID de session."""
        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retourne ID user associé à ID de session donné, s'il existe."""
        if not session_id or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Récupère l'utilisateur actuel à partir de la session courante."""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user
