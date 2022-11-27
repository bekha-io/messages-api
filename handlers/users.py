from fastapi import APIRouter, Depends

from models.user import CreateUserRequest, UserResponse, TokenPair, SignInRequest, RefreshTokenRequest
from services.user import UserService
from handlers.exceptions import *

router = APIRouter(prefix='/users')


@router.post('/sign-up', response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             summary="Sign-up",
             responses={
                 status.HTTP_409_CONFLICT: USER_ALREADY_EXISTS.schema()
             },
             response_model_exclude={'hashed_password', 'access_token', 'refresh_token'})
def sign_up(data: CreateUserRequest, user_s: UserService = Depends()):
    """Регистрация нового пользователя в системе.
    В качестве параметров выступают уникальный имя пользователя (username), пароль и подтверждение пароля.
    В случае, если имя пользователя занято, возвращает ответ со статусом 409 (Conflict).
    В случае успешной регистрации возвращает объект пользователя (200)"""
    u = user_s.create_user(data)
    if not u:
        raise USER_ALREADY_EXISTS
    return UserResponse.parse_obj(u)


@router.post('/sign-in', response_model=TokenPair, status_code=status.HTTP_200_OK,
             summary="Sign-in",
             responses={
                 status.HTTP_401_UNAUTHORIZED: INVALID_AUTH_CRED.schema(),
             })
def sign_in(data: SignInRequest, user_s: UserService = Depends()):
    """Вход пользователя по имени пользователя и паролю. Если аутентификация успешна, возвращает
    данные авторизации в виде access_token и refresh_token (200). В ином случае возвращает ошибку"""
    if user_s.is_authenticated(data):
        u = user_s.get_user_by_username(data.username)
        return user_s.new_token_pair(u.uuid)
    else:
        raise INVALID_AUTH_CRED


@router.post('/refresh-token', response_model=TokenPair, status_code=status.HTTP_200_OK,
             summary="Refresh token",
             responses={
                 status.HTTP_401_UNAUTHORIZED: TOKEN_EXPIRED.schema()})
def refresh_token(data: RefreshTokenRequest, user_s: UserService = Depends()):
    """Возвращает новую пару access и refresh токенов, если тело запроса содержит действующий refresh токен (200).
    В ином случае, если срок действия refresh_token истек, необходимо осуществить вход с помощью имени пользователя
    и пароля (401)"""
    pair = user_s.new_token_pair_via_refresh_token(data.refresh_token)
    if pair:
        return pair
    raise TOKEN_EXPIRED
