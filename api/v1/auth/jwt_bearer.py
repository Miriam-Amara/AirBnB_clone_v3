#!/usr/bin/env python3

"""

"""

from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Request
from typing import Any, cast
import jwt
import logging
import os

from api.v1.auth.auth import Auth
from api.v1.views.utils import get_obj
from models.user import User


load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class JWTBearerAuth(Auth):
    """
    """
    def get_bearer_token(
            self,
            authorization_header: str | None
        ) -> str | None:
        """
        Extracts and returns the JWT token from a Bearer Authorization header.
        """
        logger.debug(f"{authorization_header}")
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str): # type: ignore
            return
        if not authorization_header.startswith("Bearer "):
            return
        logger.debug(f"{authorization_header.split()[1]}")
        return authorization_header.split()[1]
    
    def decode_jwt_token(
            self,
            token: str | None
        ) -> dict[str, Any] | None:
        """Returns the decoded payload from a JWT token string."""
        if not token:
            return
        if not isinstance(token, str): # type: ignore
            return
        try:
            decoded_data: dict[str, Any] = jwt.decode( # type: ignore
                token, os.getenv("SECRET_KEY"), algorithms=["HS256"]
            )
            logger.debug(f"{decoded_data}")
            return decoded_data
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError as e:
            logger.debug(f"{e}")
            return
    
    def encode_jwt_token(self, user_id: str) -> tuple[str, str]:
        """
        
        """
        access_token_data: dict[str, Any] = {
            "sub": user_id,
            "exp": datetime.now() + timedelta(minutes=30)
        }
        refresh_token_data: dict[str, Any] = {
            "sub": user_id,
            "exp": datetime.now() + timedelta(days=7)
        }

        access_token: str = jwt.encode( # type: ignore
            access_token_data, os.getenv("SECRET_KEY"), algorithm="HS256"
        )
        refresh_token: str = jwt.encode( # type: ignore
            refresh_token_data, os.getenv("SECRET_KEY"), algorithm="HS256"
        )
        return access_token, refresh_token 

    
    def current_user(self, request: Request | None=None) -> User | None:
        """
        Overloads Auth and retrieves the User instance for a request.
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return
        token = self.get_bearer_token(auth_header)
        if not token:
            return
        decoded_data = self.decode_jwt_token(token)
        if not decoded_data:
            return

        user_obj = cast(User, get_obj("User", decoded_data["sub"]))
        logger.debug(f"auth_header: {auth_header}")
        logger.debug(f"base64_auth_header: {token}")
        logger.debug(f"decoded_base64_auth: {decoded_data}")
        logger.debug(f"user_obj: {user_obj}")
        return user_obj
