from fastapi import FastAPI
from core.db import Base, engine

def create_app() -> FastAPI:
    app = FastAPI(title="Personal Expenses Tracker")

    Base.metadata.create_all(bind=engine)

    @app.get("/")
    def hello_world():
        return "Hello world"

    return app


app = create_app()
