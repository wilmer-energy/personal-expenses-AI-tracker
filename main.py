from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import ALLOWED_ORIGINS, ENVIRONMENT
from core.db import Base, engine
from routers.expense import router as expense_router
from routers.user import router as user_router


def create_app() -> FastAPI:
    is_prod = ENVIRONMENT == "production"
    app = FastAPI(title="Personal Expenses Tracker")

    app = FastAPI(
        title="Personal Expenses Tracker",
        docs_url=None if is_prod else "/docs",
        redoc_url=None if is_prod else "/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(user_router)
    app.include_router(expense_router)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
