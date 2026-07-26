from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.expense import Expense as ExpenseModel


class ExpenseRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, expense_data: dict[str, Any]) -> ExpenseModel:
        expense = ExpenseModel(**expense_data)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_by_user(self, user_id: int) -> list[ExpenseModel]:
        query = (
            select(ExpenseModel)
            .where(
                ExpenseModel.user_id == user_id,
                ExpenseModel.deleted_at.is_(None),
            )
            .order_by(ExpenseModel.made_at.desc())
        )

        return list(self.db.scalars(query).all())

    def update(
        self,
        expense_id: int,
        user_id: int,
        expense_data: dict[str, Any],
    ) -> ExpenseModel | None:

        expense = self.db.scalar(
            select(ExpenseModel).where(
                ExpenseModel.id == expense_id,
                ExpenseModel.user_id == user_id,
                ExpenseModel.deleted_at.is_(None),
            )
        )

        if expense is None:
            return None

        for key, value in expense_data.items():
            setattr(expense, key, value)

        self.db.commit()
        self.db.refresh(expense)

        return expense

    def delete(self, expense_id: int, user_id: int) -> bool:
        expense = self.db.scalar(
            select(ExpenseModel).where(
                ExpenseModel.id == expense_id,
                ExpenseModel.user_id == user_id,
                ExpenseModel.deleted_at.is_(None),
            )
        )

        if expense is None:
            return False

        expense.deleted_at = datetime.now(timezone.utc)

        self.db.commit()

        return True

    
    def get_by_id(self, expense_id: int, user_id: int) -> ExpenseModel | None:
        query = (
            select(ExpenseModel)
            .where(
                ExpenseModel.id == expense_id,
                ExpenseModel.user_id == user_id,
                ExpenseModel.deleted_at.is_(None),
            )
        )

        return self.db.scalar(query)