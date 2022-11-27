from fastapi.exceptions import HTTPException
from fastapi import status
from pydantic import BaseModel, Field


class APIExceptionModel(BaseModel):
    detail: str = Field(..., description="Подробное описание ошибки")


class APIException(HTTPException):
    model: BaseModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = APIExceptionModel(detail=self.detail)

    def schema(self):
        return {
            'model': self.model.__class__,
            'content': {
                'application/json': {
                    'example': {'detail': self.detail}
                }
            },
        }


# Users
NOT_AUTHENTICATED = APIException(status.HTTP_401_UNAUTHORIZED, "Not authenticated. Invalid authorization data or "
                                                               "token may be expired")
TOKEN_EXPIRED = APIException(status.HTTP_401_UNAUTHORIZED,
                             "Your token may be expired. Try to sign-in using username and password")
INVALID_AUTH_CRED = APIException(status.HTTP_401_UNAUTHORIZED, "Invalid authentication credentials")
USER_ALREADY_EXISTS = APIException(status.HTTP_409_CONFLICT,
                                   "User with such credentials already exists")

# Messages
NOT_MESSAGE_AUTHOR = APIException(status.HTTP_403_FORBIDDEN,
                                  "Not enough rights to delete others messages")
MESSAGE_NOT_FOUND = APIException(status.HTTP_404_NOT_FOUND, "Message with such id not found")
