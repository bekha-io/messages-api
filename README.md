# MessageAPI

REST API сервис, предоставляющий минималистичный интерфейс для взаимодействия с сообщениями: просмотр, публикация и
удаление. Имеется система доступа, основанная на аутентификации и авторизации пользователей (регистрация, вход). Все
взаимодействие с интерфейсом сообщений происходит с использованием HTTPBearer аутентификации (JWT Bearer).

<b>Сервис был написан в качестве решения тестового задания для вакансии Python бэкэнд-разработчика в zypl.ai</b>

URL для тестирования сервиса: http://134.209.177.216:8000/

### Тестовое задание

```text
Backend sample test

Create a simple API for a web application on Python. The API should allow
the user to register, log in, post a text message, view all previous messages
and delete a message selectively. All actions with messages should be only
allowed to logged users (JWT). Fill the automatic FastAPI documentation
with details as much as you can. Encrypt passwords!

Use following libraries:
● SQLite
● FastAPI
● pydantic

If possible, deploy the API on server/cloud for public access.

```

### Конфигурация

Создайте модуль `config.py` в корневой директории проекта со следующим содержанием:

```python
class Database:
    DB_NAME = "путь/к/базе/sqlite"


class Auth:
    JWT_SECRET = "секретный-ключ-для-шифрования-JWT-токенов"
    ACCESS_EXPIRES_IN = 15 * 60  # Срок действия access токена в секундах
    REFRESH_EXPIRES_IN = 60 * 60 * 24  # Срок действия access токена в секундах
```

### Документация

Документация доступна по адресам:
http://134.209.177.216:8000/docs (SwaggerUI)
http://134.209.177.216:8000/redoc (Redocly, рекомендуется)