from datetime import datetime, timedelta, timezone
from random import randint

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.providers.email.email_provider import EmailProvider
from entities.password_reset_code import PasswordResetCode
from routers.dtos.forgot_password import ForgotPasswordDto
from routers.repositories.password_reset_code import (
    PasswordResetCodeRepository,
)
from routers.repositories.user import UserRepository


def execute(
    dto: ForgotPasswordDto,
    db: Session,
    email_provider: EmailProvider,
):
    user_repository = UserRepository(db)

    user = user_repository.get_by_email(dto.email)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    repository = PasswordResetCodeRepository(db)

    repository.delete_active_codes(user.id)

    code = randint(100000, 999999)

    entity = PasswordResetCode(
        code=str(code),
        expires_at=datetime.now(timezone.utc)
        + timedelta(minutes=10),
        user_id=user.id,
    )

    repository.create(entity)

    email_provider.send_verification_code_email(
        code=code,
        email=user.email,
    )

    return {
        "message": "Verification code sent."
    }