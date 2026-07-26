from fastapi import HTTPException
from sqlalchemy.orm import Session

from routers.dtos.update_expense import UpdateExpense
from routers.repositories.expense import ExpenseRepository


def execute(
    expense_id: int,
    user_id: int,
    dto: UpdateExpense,
    db: Session,
):
    repository = ExpenseRepository(db)

    expense = repository.get_by_id(expense_id, user_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    expense_data = dto.model_dump()

    return repository.update(
        expense_id=expense_id,
        user_id=expense.user_id,
        expense_data=expense_data,
    )
