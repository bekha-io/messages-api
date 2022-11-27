import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import config
from services.users import UserService
from handlers.exceptions import NOT_AUTHENTICATED


bearer = HTTPBearer(description="Используйте JWT access_token для аутентификации")


def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer), auth_s: UserService = Depends(UserService)):
    """Serves as a middleware function for messages related routes.
    Validates bearer jwt-token and returns matching context User object"""
    try:
        payload = jwt.decode(token.credentials, config.Auth.JWT_SECRET, algorithms=["HS256"])
        user_uuid = payload.get('sub')
        if user_uuid is None:
            raise NOT_AUTHENTICATED
        user = auth_s.get_by_pk(user_uuid)
        if not user:
            raise NOT_AUTHENTICATED
        if user.access_token != token.credentials:
            raise NOT_AUTHENTICATED
        return user
    except jwt.PyJWTError:
        raise NOT_AUTHENTICATED
