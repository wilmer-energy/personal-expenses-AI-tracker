from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.password_reset_code import PasswordResetCode


class PasswordResetCodeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_valid_code(
        self,
        user_id: int,
        code: str,
    ) -> PasswordResetCode | None:

        query = (
            select(PasswordResetCode)
            .where(
                PasswordResetCode.user_id == user_id,
                PasswordResetCode.code == code,
                PasswordResetCode.used.is_(False),
                PasswordResetCode.deleted_at.is_(None),
            )
        )

        return self.db.scalar(query)

    def update(self, entity: PasswordResetCode):
        self.db.commit()
        self.db.refresh(entity)

    def create(self, entity: PasswordResetCode):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

    def delete_active_codes(self, user_id: int):
        query = select(PasswordResetCode).where(
            PasswordResetCode.user_id == user_id,
            PasswordResetCode.deleted_at.is_(None),
        )

        codes = self.db.scalars(query).all()

        for code in codes:
            code.deleted_at = datetime.now(timezone.utc)

        self.db.commit()
