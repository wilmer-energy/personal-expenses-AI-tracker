import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True, future=True)


SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=Session)


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        default=None,
        nullable=True
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
