from fastapi import FastAPI

from core.db import Base, engine
from routers.user import router as user_router
from routers.expense import router as expense_router


def create_app() -> FastAPI:
    app = FastAPI(title="Personal Expenses Tracker")

    Base.metadata.create_all(bind=engine)

    app.include_router(user_router)
    app.include_router(expense_router)

    @app.get("/")
    def hello_world():
        return "Hello world"

    return app


app = create_app()
