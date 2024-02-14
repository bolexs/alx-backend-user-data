#!/usr/bin/env python3
"""BasicAuth Module"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return the Base64 part of the Authorization header"""
        if authorization_header is None or \
                type(authorization_header) is not str or \
                not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Return the decoded value of a Base64 string"""
        if base64_authorization_header is None or \
                type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header.encode('utf-8')).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Return the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) is not str or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on his email and password"""
        if user_email is None or user_pwd is None or \
                type(user_email) is not str or type(user_pwd) is not str:
            return None
        try:
            return User().search({'email': user_email})
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(auth_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_email, user_pwd)
