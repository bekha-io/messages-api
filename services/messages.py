import datetime
import typing
from uuid import UUID

from services.abstract import AbstractService
from models.message import Message, MessageResponse, MessagesListResponse
from db.sqlite import Database


class MessageService(AbstractService):
    def get_by_pk(self, pk: int) -> typing.Optional[Message]:
        with Database() as db:
            r = db.fetch(
                "SELECT * FROM messages WHERE id=?", (pk,)
            )
            if r:
                m = Message(**r)
                if not m.deleted_at:
                    return m

    def delete_by_pk(self, pk: typing.Any) -> typing.Any:
        with Database() as db:
            tx = db.execute(
                "UPDATE messages SET deleted_at=? WHERE id=?", (datetime.datetime.now(), pk)
            )
            if tx.rowcount != 0:
                r = db.fetch(
                    "SELECT * FROM messages WHERE id=? LIMIT 1", (pk,)
                )
                return Message(**r)

    @staticmethod
    def post_message(user_uuid: UUID, text: str):
        with Database() as db:
            tx = db.execute(
                "INSERT INTO messages (user_uuid, text, published_at) VALUES (?, ?, ?)",
                (user_uuid.__str__(), text, datetime.datetime.now())
            )
            if tx.rowcount != 0:
                r = db.fetch(
                    "SELECT * FROM messages WHERE user_uuid=? ORDER BY published_at DESC LIMIT 1", (
                        user_uuid.__str__(),)
                )
                return MessageResponse(**r)

    @staticmethod
    def get_user_messages(user_uuid: UUID) -> MessagesListResponse:
        with Database() as db:
            r = db.fetch(
                "SELECT * FROM messages WHERE user_uuid=? ORDER BY published_at DESC ", (user_uuid.__str__(),),
                many=True
            )
            return MessagesListResponse(messages=[MessageResponse(**m) for m in r], count=len(r))
