from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db import get_db
from routers.dtos.create_user import CreateUser
from routers.use_cases.create_user import execute
from routers.use_cases.get_user_by_id import execute as get_user_by_id_use_case
from routers.use_cases.get_users import execute as get_users_use_case

router = APIRouter(prefix="/user")

DbSession = Annotated[Session, Depends(get_db)]

@router.post("")
def create_user(dto: CreateUser, db: DbSession):
    return execute(dto, db)


@router.get("/{id}")
def get_user_by_id(id: int, db: DbSession):
    return get_user_by_id_use_case(id, db)


@router.get("/")
def get_users(db: DbSession):
    return get_users_use_case(db)
