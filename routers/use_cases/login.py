from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.jwt import create_access_token
from core.security import verify_password
from routers.dtos.login import LoginDto
from routers.repositories.user import UserRepository


def execute(dto: LoginDto, db: Session):
    repository = UserRepository(db)

    user = repository.get_by_email(dto.email.strip().lower())

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(dto.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        id=user.id,
        name=user.name,
        email=user.email,
    )

    return {
        "access_token": token,
        "token_type": "Bearer",
    }
