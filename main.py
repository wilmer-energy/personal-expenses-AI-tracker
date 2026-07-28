from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db import Base, engine
from routers.expense import router as expense_router
from routers.user import router as user_router

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]


def create_app() -> FastAPI:
    app = FastAPI(title="Personal Expenses Tracker")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(user_router)
    app.include_router(expense_router)

    @app.get("/")
    def hello_world():
        return "Hello world"

    return app


app = create_app()
