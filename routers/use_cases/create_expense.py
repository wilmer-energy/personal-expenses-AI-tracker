from sqlalchemy.orm import Session

from routers.dtos.create_expense import CreateExpense
from routers.repositories.expense import ExpenseRepository


def execute(dto: CreateExpense, db: Session):
    repository = ExpenseRepository(db)

    expense = repository.create(dto.model_dump())

    return expense