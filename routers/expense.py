from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db import get_db
from routers.dtos.create_expense import CreateExpense
from routers.dtos.update_expense import UpdateExpense
from routers.use_cases.create_expense import execute as create_expense_use_case
from routers.use_cases.delete_expense import execute as delete_expense_use_case
from routers.use_cases.get_expenses_by_user import (
    execute as get_expenses_by_user_use_case,
)
from routers.use_cases.update_expense import execute as update_expense_use_case

router = APIRouter(prefix="/expenses", tags=["Expenses"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("")
def create_expense(dto: CreateExpense, db: DbSession):
    return create_expense_use_case(dto, db)


@router.get("/user/{user_id}")
def get_expenses_by_user(user_id: int, db: DbSession):
    return get_expenses_by_user_use_case(user_id, db)


@router.put("/{id}")
def update_expense(id: int, dto: UpdateExpense, db: DbSession):
    return update_expense_use_case(id, dto, db)


@router.delete("/{expense_id}/user/{user_id}")
def delete_expense(expense_id: int, user_id: int, db: DbSession):
    return delete_expense_use_case(
        expense_id=expense_id,
        user_id=user_id,
        db=db,
    )
