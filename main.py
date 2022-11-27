from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from db.sqlite import Database
import handlers.users
import handlers.messages

app = FastAPI()
app.include_router(handlers.users.router, tags=["users"])
app.include_router(handlers.messages.router, tags=["messages"])
app.mount("/static", StaticFiles(directory="static"), name="static")


def my_schema():
    openapi_schema = get_openapi(
        title="Messages API",
        version="1.0b",
        description="REST API сервис, позволяющий авторизированным пользователям создавать и делиться сообщениями. "
                    "Сервис был написан в качестве решения тестового задания "
                    "для вакансии Python бэкэнд-разработчика в zypl.ai",
        contact={"email": "iskandarzoda@outlook.com", "name": "Bekhruz Iskandarzoda"},
        routes=app.routes,
    )
    return openapi_schema


app.openapi_schema = my_schema()

# Creating non-existing tables first
with Database() as db:
    db.migrate()
