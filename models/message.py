import datetime
import typing
from uuid import UUID

from models.base import *


class Message(Model):
    id: int = Field(..., description="Уникальный идентификатор сообщения в системе")
    user_uuid: UUID = Field(..., description="UUID пользователя, опубликовавшего сообщение")
    text: str = Field(..., description="Содержимое сообщения")
    published_at: datetime.datetime = Field(..., description="Дата и время публикации сообщения в формате "
                                                             "RFC 3339 (ISO 8601)")
    deleted_at: typing.Optional[datetime.datetime] = Field(..., description="Дата и время удаления сообщения в формате "
                                                                            "RFC 3339 (ISO 8601)")


class CreateMessageRequest(Model):
    text: str = Field(..., description="Текст-содержимое сообщения для опубликования. Не более 256 символов",
                      max_length=256)


class MessageResponse(Model):
    id: int = Field(..., description="Уникальный идентификатор сообщения в системе")
    user_uuid: UUID = Field(..., description="UUID пользователя, опубликовавшего сообщение")
    text: str = Field(..., description="Содержимое сообщения")
    published_at: datetime.datetime = Field(...,
                                            description="Дата и время публикации сообщения в формате RFC 3339 (ISO 8601)")


class MessagesListResponse(Model):
    count: typing.Optional[int] = Field(..., description="Количество сообщений в массиве messages")
    messages: typing.List[MessageResponse] = Field(..., description="Массив сообщений")