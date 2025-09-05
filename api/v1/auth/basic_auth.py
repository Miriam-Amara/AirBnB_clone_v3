#!/usr/bin/env python3

"""

"""

from flask import Request
from typing import cast
import base64
import logging

from api.v1.auth.auth import Auth
from models.user import User


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BasicAuth(Auth):
    """ """

    def extract_base64_authorization_header(
            self,
            authorization_header: str | None
        ) -> str | None:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        logger.debug(f"{authorization_header}")
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str): # type: ignore
            return
        if not authorization_header.startswith("Basic "):
            return
        logger.debug(f"{authorization_header.split()[1]}")
        return authorization_header.split()[1]
    
    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str | None
        ) -> str | None:
        """Returns the decoded value of a Base64 string"""
        if not base64_authorization_header:
            return
        if not isinstance(base64_authorization_header, str): # type: ignore
            return
        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True
            )
        except Exception:
            return
        decoded_string = decoded_bytes.decode("utf-8")
        logger.debug(f"{decoded_string}")
        return decoded_bytes.decode("utf-8")
        
    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str | None
        ) -> tuple[str, str] | None:
        """Returns the user email and password from the Base64 decoded value"""
        if not decoded_base64_authorization_header:
            return
        if not isinstance(decoded_base64_authorization_header, str): # type: ignore
            return
        if ":" not in decoded_base64_authorization_header:
            return
        try:
            email, password = decoded_base64_authorization_header.split(":")[:2]
        except Exception as e:
            logger.error(f"{e}")
            return
        logger.debug(f"email: {email}")
        logger.debug(f"password: {password}")
        return (email, password)
    
    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
        ) -> User | None:
        """
        Returns the User instance based on his email and password.
        """
        if (not isinstance(user_email, str) # type: ignore
            or not isinstance(user_pwd, str) # type: ignore
        ):
            return
        
        user_obj = cast(User, User.search(user_email))
        if not user_obj:
            return
        if not user_obj.is_valid_password(user_pwd):
            return
        return user_obj
    
    def current_user(self, request: Request | None=None) -> User | None:
        """
        Overloads Auth and retrieves the User instance for a request.
        """
        logger.debug(f"In current user")
        auth_header = self.authorization_header(request)
        if not auth_header:
            return
        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        if not base64_auth_header:
            return
        decoded_base64_auth = self.decode_base64_authorization_header(base64_auth_header)
        if not decoded_base64_auth:
            return
        user_data = self.extract_user_credentials(decoded_base64_auth)
        if not user_data:
            return
        user_obj = self.user_object_from_credentials(user_data[0], user_data[1])

        logger.debug(f"auth_header: {auth_header}")
        logger.debug(f"base64_auth_header: {base64_auth_header}")
        logger.debug(f"decoded_base64_auth: {decoded_base64_auth}")
        logger.debug(f"user_data: {user_data}")
        logger.debug(f"user_obj: {user_obj}")
        return user_obj
