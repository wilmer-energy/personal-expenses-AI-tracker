from sqlalchemy.orm import Session

from routers.dtos.create_expense import CreateExpense
from routers.repositories.expense import ExpenseRepository


def execute(user_id:int, dto: CreateExpense, db: Session):
    repository = ExpenseRepository(db)
    data = dto.model_dump()
    data["user_id"] = user_id
    expense = repository.create(data)

    return expense