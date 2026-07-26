from sqlalchemy.orm import Session

from routers.repositories.expense import ExpenseRepository


def execute(
    expense_id: int,
    user_id: int,
    db: Session,
) -> bool:
    repository = ExpenseRepository(db)

    return repository.delete(
        expense_id=expense_id,
        user_id=user_id,
    )