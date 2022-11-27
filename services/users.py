import datetime
import typing
import jwt
from uuid import UUID

import config
from services.abstract import AbstractService
from models.user import CreateUserRequest, User, TokenPair, SignInRequest
from db.sqlite import Database
from utils import check_password


class UserService(AbstractService):
    def get_by_pk(self, pk: UUID) -> typing.Optional[User]:
        with Database() as db:
            r = db.fetch("SELECT * FROM users WHERE uuid =?", (pk.__str__(),))
            if r:
                return User(**r)

    def delete_by_pk(self, pk: UUID):
        with Database() as db:
            db.execute("DELETE FROM users WHERE uuid=?", (pk.__str__()))
            return

    @staticmethod
    def get_user_by_username(username: str) -> typing.Optional[User]:
        with Database() as db:
            r = db.fetch(
                "SELECT * FROM users WHERE username=?", (username,)
            )
            if r:
                return User(**r)

    def create_user(self, data: CreateUserRequest) -> typing.Optional[User]:
        """Creates user if not there is no matching username, otherwise returns None"""
        u = self.get_user_by_username(data.username)
        if not u:
            with Database() as db:
                db.execute(
                    "INSERT INTO users (uuid, username, hashed_password, "
                    "access_token, refresh_token, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (data.uuid.__str__(), data.username, data.password_confirm,
                     self.__get_new_access_token(data.uuid), self.__get_new_refresh_token(data.uuid),
                     data.created_at))
                r = db.fetch("SELECT * FROM users WHERE username=?", (data.username, ))
                if r:
                    return User(**r)

    def is_authenticated(self, data: SignInRequest) -> bool:
        """Checks username/password match and verifies user. Returns True if credentials are correct, False otherwise"""
        user = self.get_user_by_username(data.username)
        if user:
            return True if check_password(data.password, user.hashed_password) else False
        return False

    def new_token_pair(self, user_uuid: UUID) -> TokenPair:
        """Updates matching user's token pair (access_token, refresh_token)"""
        user = self.get_by_pk(user_uuid)
        if user:
            pair = TokenPair(
                access_token=self.__get_new_access_token(user_uuid),
                refresh_token=self.__get_new_refresh_token(user_uuid)
            )
            with Database() as db:
                db.execute(
                    "UPDATE users SET access_token=? , refresh_token=? WHERE uuid=?",
                    (pair.access_token, pair.refresh_token, user_uuid.__str__())
                )
            return pair

    def new_token_pair_via_refresh_token(self, refresh_token: str) -> typing.Optional[TokenPair]:
        with Database() as db:
            r = db.fetch(
                "SELECT * FROM users WHERE refresh_token=?", (refresh_token,),
            )
            if r:
                u = User(**r)
                return self.new_token_pair(u.uuid)

    @staticmethod
    def __get_new_access_token(user_uuid: UUID) -> str:
        return jwt.encode(
            {'exp': datetime.datetime.now() + datetime.timedelta(seconds=config.Auth.ACCESS_EXPIRES_IN),
             'sub': user_uuid.__str__(),
             },
            config.Auth.JWT_SECRET
        )

    @staticmethod
    def __get_new_refresh_token(user_uuid: UUID) -> str:
        return jwt.encode(
            {'exp': datetime.datetime.now() + datetime.timedelta(seconds=config.Auth.REFRESH_EXPIRES_IN),
             'sub': user_uuid.__str__(),
             },
            config.Auth.JWT_SECRET
        )
