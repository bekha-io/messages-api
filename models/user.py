import datetime
from uuid import UUID, uuid4
import regex

from models.base import *
from utils import get_hashed_password


class User(Model):
    """A base user model to be used in code and read/saved from/into database"""
    uuid: UUID = Field(default_factory=uuid4)
    username: str
    hashed_password: str
    access_token: str
    refresh_token: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class CreateUserRequest(Model):
    """A model of create user request. It demands only username and password as inputs"""
    username: str = Field(..., description="Имя пользователя. Может содержать только цифры, буквы "
                                           "и спецсимволы '-' и '.', если они не расположены в начале и конце",
                          max_length=24)
    password: str = Field(..., description="Пароль", max_length=24)
    password_confirm: str = Field(..., description="Подтверждение пароля", max_length=24)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = uuid4()
        self.created_at = datetime.datetime.now()

    @validator('username')
    def validate_username(cls, v):
        if regex.fullmatch(r"^(?=.*[A-Za-z0-9]$)[A-Za-z][A-Za-z\d.-]{0,19}$", v) is None:
            raise ValueError('Please, try to use another username')
        return v

    @validator('password_confirm')
    def validate_password(cls, v, values, **kwargs):
        # Check whether passwords match
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')

        # Strong password check
        if regex.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", v) is None:
            raise ValueError(
                'Password should be strength. Minimum eight characters, at least one letter and one number')
        v = get_hashed_password(values['password'])
        return v


class UserResponse(Model):
    """A simple output User model to return and hide some specific sensitive fields"""
    uuid: UUID = Field(..., description="UUID пользователя")
    username: str = Field(..., description="Имя пользователя")
    created_at: datetime.datetime = Field(..., description="Дата и время регистрации пользователя в формате "
                                                           "RFC 3339 (ISO 8601)")


class TokenPair(Model):
    access_token: str = Field(..., description="Сгенерированный многоразовый, но короткоживущий JWT access_token "
                                               "для использования в "
                                               "последующих запросах до истечения срока его действия. "
                                               "Срок жизни - 15 минут")
    refresh_token: str = Field(..., description="Сгенерированный одноразовый, но долгоживущий JWT refresh_token "
                                                "для обновления сессии. Срок жизни - 24 часа")


class SignInRequest(Model):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(..., description="Пароль")


class RefreshTokenRequest(Model):
    refresh_token: str = Field(..., description="Токен, выданный ранее в рамках действующей сессии. "
                                                "Используется для выпуска новой пары токенов (access, refresh)")
