from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from entities.expense import ExpenseCategory


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    note: str | None
    amount: Decimal
    made_at: datetime
    category: ExpenseCategory