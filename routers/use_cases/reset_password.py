import re
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import hash_password
from routers.dtos.reset_password import ResetPasswordDto
from routers.repositories.password_reset_code import PasswordResetCodeRepository
from routers.repositories.user import UserRepository


def execute(dto: ResetPasswordDto, db: Session):

    if len(dto.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters.",
        )

    if not re.search(r"[A-Za-z]", dto.password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain letters.",
        )

    if not re.search(r"\d", dto.password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain numbers.",
        )

    user_repository = UserRepository(db)

    user = user_repository.get_by_email(dto.email)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    repository = PasswordResetCodeRepository(db)

    reset_code = repository.get_valid_code(
        user.id,
        dto.code,
    )

    if reset_code is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code.",
        )

    if reset_code.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Verification code expired.",
        )

    user_repository.update_password(
        user,
        hash_password(dto.password),
    )

    reset_code.used = True

    repository.update(reset_code)

    return {
        "message": "Password updated successfully."
    }