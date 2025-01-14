from typing import TYPE_CHECKING
import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base

if TYPE_CHECKING:
    from db.models import Transaction


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_telegramid: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    is_chanel_user: Mapped[bool] = mapped_column(default=False, nullable=True)
    first_contact_date: Mapped[datetime.date] = mapped_column(
        default=datetime.datetime.now(),
        server_default=func.now(),
    )
    start_subscribe: Mapped[datetime.datetime] = mapped_column(nullable=True)
    end_subscribe: Mapped[datetime.datetime] = mapped_column(nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
