#!/usr/bin/env python3
""" Module providing BasicAuth for user authentication."""

import base64
import binascii
from typing import TypeVar, Tuple
from models.user import User
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """Implementation of basic authentication methods."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 encoded part from the Authorization header."""
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the Base64 encoded part of the Authorization header."""
        if base64_authorization_header and isinstance(base64_authorization_header, str):
            try:
                encode = base64_authorization_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extracts user email and password from the decoded Base64 string."""
        if (decoded_base64_authorization_header and isinstance(decoded_base64_authorization_header, str) and
                ":" in decoded_base64_authorization_header):
            user_email, user_pwd = decoded_base64_authorization_header.split(":", 1)
            return user_email, user_pwd
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Fetches the User object using email and password."""
        if user_email is None or not isinstance(user_email, str) or user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if users:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overrides Auth to retrieve user based on basic auth credentials."""
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, password)
        return None
