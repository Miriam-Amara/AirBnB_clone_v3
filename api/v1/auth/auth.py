#!/usr/env python3

"""

"""


from flask import Request
import logging

from models.user import User


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Auth:
    """
    
    """
    def require_auth(self, path: str | None, excluded_paths: list[str] | None) -> bool:
        """ """
        logger.debug(f"{path}")
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        
        if not path.endswith("/"):
            path += "/"
        logger.debug(f"{path}")
        if path in excluded_paths:
            return False
        return True
    
    def authorization_header(self, request: Request | None=None) -> str | None:
        """ """
        logger.debug(f"{request}")
        logger.debug(f"{type(request)}")
        if request is None:
            return
        auth_header = request.headers.get("Authorization", None)
        logger.debug(f"{auth_header}")
        if not auth_header:
            return
        return auth_header
    
    def current_user(self, request: Request | None=None) -> User | None:
        """ """
        pass
