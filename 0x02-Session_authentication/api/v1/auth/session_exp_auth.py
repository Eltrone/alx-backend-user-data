#!/usr/bin/env python3
"""
Module des routes pour l'API
"""

from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    def __init__(self):
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary['user_id']
        created_at = session_dictionary['created_at']
        expiration_date = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_date:
            return None
        return session_dictionary['user_id']
