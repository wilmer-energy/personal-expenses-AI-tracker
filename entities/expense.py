from core.db import Base
from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
import enum
from sqlalchemy import Enum as SQLEnum
from datetime import datetime

if TYPE_CHECKING:
    from .user import User


class ExpenseCategory(str, enum.Enum):
    FIXED = "fixed"
    VARIABLE = "variable"
    SAVINGS_INVESTMENTS = "savings_investments"


class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    note: Mapped[str] = mapped_column(String(100), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    made_at: Mapped[datetime] = mapped_column(nullable=False)
    category: Mapped[ExpenseCategory] = mapped_column(
        SQLEnum(ExpenseCategory, name="category_enum"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    user: Mapped[Optional["User"]] = relationship(
        back_populates="expenses")
