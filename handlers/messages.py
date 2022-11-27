from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from handlers.jwt import *
from handlers.exceptions import *
from models.user import User
from models.message import *
from services.messages import MessageService

router = APIRouter(prefix='/messages', responses={
    status.HTTP_401_UNAUTHORIZED: NOT_AUTHENTICATED.schema(),
})
templates = Jinja2Templates(directory="templates")


@router.get("", response_model=MessagesListResponse, summary="Get all user's messages",
            response_model_exclude_none=True)
def get_user_messages(user: User = Depends(get_current_user), message_s: MessageService = Depends(MessageService)):
    """Возвращает все сообщения, опубликованные контекстным пользователем и
    отсортированные по дате публикации в убывающем порядке (200)"""
    return message_s.get_user_messages(user.uuid)


@router.get('/view/{message_id}', response_class=HTMLResponse,
            summary="View message page",
            openapi_extra={
                "parameters": [
                    {
                        "in": "query",
                        "name": "message_id",
                        "schema": {
                            "type": "integer"
                        },
                        "description": "ID сообщения"
                    }
                ]
            },
            responses={
                status.HTTP_404_NOT_FOUND: {'class': HTMLResponse}
            })
def view_message_by_id(message_id: int, request: Request, user: User = Depends(get_current_user),
                       message_s: MessageService = Depends(MessageService),
                       user_s: UserService = Depends(UserService)):
    """Html-представление сообщения изначально не запрашивало аутентификацию. <b>Согласно условиям теста, все действия
    с сообщениями должны быть разрешены только для вошедших в систему пользователей</b>. Так как просмотр сообщения
    также является действием по отношению к сообщению, было принято решение запрашивать Bearer аутентификацию
    для просмотра страницы с сообщением, в том числе"""
    message = message_s.get_by_pk(message_id)
    if message:
        user = user_s.get_by_pk(message.user_uuid)
        if user:
            return templates.TemplateResponse(
                "message.html", {'message': message, 'request': request, 'author': user}
            )
    return templates.TemplateResponse(
        'message_404.html', {'request': request})


@router.get("/{message_id}", response_model=MessageResponse, response_model_exclude_none=True,
            summary="Get message",
            status_code=status.HTTP_200_OK,
            openapi_extra={
                "parameters": [
                    {
                        "in": "query",
                        "name": "message_id",
                        "schema": {
                            "type": "integer"
                        },
                        "description": "ID сообщения"
                    }
                ]
            },
            responses={status.HTTP_404_NOT_FOUND: MESSAGE_NOT_FOUND.schema()})
def get_message_by_id(message_id: int, message_s: MessageService = Depends(MessageService)):
    """Возвращает сообщение по его ID (200). Если сообщение с таким ID не найдено, возвращает ошибку (404).
    <b>Пользователь может просматривать чужие сообщения, т.е. сообщения, авторами которых он не является</b>"""
    message = message_s.get_by_pk(message_id)
    if message:
        return message
    raise MESSAGE_NOT_FOUND


@router.post("", response_model=MessageResponse, response_model_exclude_none=True,
             summary="Post new message")
def post_message(data: CreateMessageRequest, user: User = Depends(get_current_user),
                 message_s: MessageService = Depends(MessageService)):
    """Роут предназначен для опубликования сообщения (200).
    Возвращает опубликованное сообщение, если не возникло ошибок"""
    message = message_s.post_message(user.uuid, data.text)
    if message:
        return message


@router.delete('/{message_id}', response_model=Message, summary="Delete message",
               status_code=status.HTTP_200_OK,
               openapi_extra={
                   "parameters": [
                       {
                           "in": "query",
                           "name": "message_id",
                           "schema": {
                               "type": "integer"
                           },
                           "description": "ID сообщения"
                       }
                   ]
               },
               responses={
                   status.HTTP_403_FORBIDDEN: NOT_MESSAGE_AUTHOR.schema(),
                   status.HTTP_404_NOT_FOUND: MESSAGE_NOT_FOUND.schema()
               })
def delete_message_by_id(message_id: int, user: User = Depends(get_current_user),
                         message_s: MessageService = Depends(MessageService),
                         user_s: UserService = Depends(UserService)):
    """Удаляет сообщение и возвращает удаленное сообщение, если не возникло ошибок.
    Удаление сообщения доступно только его владельцу (200).
    В случае, если пользователь не является автором сообщения, возвращает ошибку (403).
    Если сообщение не найдено, также возвращает ошибку (404)"""
    message = message_s.get_by_pk(message_id)
    if message:
        if user.uuid == message.user_uuid:
            message_s.delete_by_pk(pk=message.id)
            message.deleted_at = datetime.datetime.now()
            return message
        raise NOT_MESSAGE_AUTHOR

    raise MESSAGE_NOT_FOUND
