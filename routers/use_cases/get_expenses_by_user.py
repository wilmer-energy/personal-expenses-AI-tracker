from sqlalchemy.orm import Session

from routers.dtos.expense_response import ExpenseResponse
from routers.repositories.expense import ExpenseRepository


def execute(user_id: int, db: Session) -> list[ExpenseResponse]:
    repository = ExpenseRepository(db)

    expenses = repository.get_by_user(user_id)

    return [
        ExpenseResponse.model_validate(expense)
        for expense in expenses
    ]