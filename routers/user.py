from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.container import Container
from core.db import get_db
from routers.dtos.create_user import CreateUser
from routers.dtos.forgot_password import ForgotPasswordDto
from routers.dtos.login import LoginDto
from routers.dtos.reset_password import ResetPasswordDto
from routers.use_cases.create_user import execute
from routers.use_cases.forgot_password import execute as forgot_password_use_case
from routers.use_cases.get_user_by_id import execute as get_user_by_id_use_case
from routers.use_cases.get_users import execute as get_users_use_case
from routers.use_cases.login import execute as login_use_case
from routers.use_cases.reset_password import execute as reset_password_use_case

router = APIRouter(prefix="/user")

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/login")
def login(dto: LoginDto, db: DbSession):
    return login_use_case(dto, db)


@router.post("")
def create_user(dto: CreateUser, db: DbSession):
    return execute(dto, db)


@router.get("/{id}")
def get_user_by_id(id: int, db: DbSession):
    return get_user_by_id_use_case(id, db)


@router.get("/")
def get_users(db: DbSession):
    return get_users_use_case(db)



@router.post("/reset-password")
def reset_password(
    dto: ResetPasswordDto,
    db: DbSession,
):
    return reset_password_use_case(dto, db)



@router.post("/forgot-password")
def forgot_password(
    dto: ForgotPasswordDto,
    db: DbSession,
):
    return forgot_password_use_case(
        dto,
        db,
        Container.email_provider,
    )
