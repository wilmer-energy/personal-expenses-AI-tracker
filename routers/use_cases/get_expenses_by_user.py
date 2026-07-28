from datetime import date

from sqlalchemy.orm import Session

from routers.dtos.expense_response import ExpenseResponse
from routers.repositories.expense import ExpenseRepository


def execute(
    user_id: int,
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[ExpenseResponse]:

    repository = ExpenseRepository(db)

    expenses = repository.get_by_user(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    return [
        ExpenseResponse.model_validate(expense)
        for expense in expenses
    ]
