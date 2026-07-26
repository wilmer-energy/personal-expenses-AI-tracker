from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from entities.expense import ExpenseCategory


class CreateExpense(BaseModel):
    note: str | None = None
    amount: Decimal
    made_at: datetime
    category: ExpenseCategory