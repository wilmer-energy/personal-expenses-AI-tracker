from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.db import get_db
from core.jwt import CurrentUser, get_current_user
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
CurrentUserDependency = Annotated[
    CurrentUser,
    Depends(get_current_user),
]


@router.post("")
def create_expense(
    current_user: CurrentUserDependency,
    dto: CreateExpense,
    db: DbSession
):
    return create_expense_use_case(current_user.id, dto, db)


@router.get("/")
def get_expenses_by_user(
    current_user: CurrentUserDependency,
    db: DbSession,
    start_date: Annotated[
        date | None,
        Query(description="Start date (YYYY-MM-DD)")
    ] = None,
    end_date: Annotated[
        date | None,
        Query(description="End date (YYYY-MM-DD)")
    ] = None,
):
    return get_expenses_by_user_use_case(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        db=db,
    )


@router.put("/{id}")
def update_expense(
        id: int,
        current_user: CurrentUserDependency,
        dto: UpdateExpense, db: DbSession
):
    return update_expense_use_case(id, current_user.id, dto, db)


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: CurrentUserDependency,
    db: DbSession
):
    return delete_expense_use_case(
        expense_id=expense_id,
        user_id=current_user.id,
        db=db,
    )
