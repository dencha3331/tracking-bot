from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base

if TYPE_CHECKING:
    from db.models import User


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sum: Mapped[int]
    days: Mapped[int]
    payload: Mapped[str] = mapped_column(unique=True)
    success: Mapped[bool] = mapped_column(default=False)

    user_telegramid: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_telegramid")
    )

    user: Mapped["User"] = relationship(back_populates="transactions")
