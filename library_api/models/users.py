from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from library_api.models import Base


if TYPE_CHECKING:
    from library_api.models import BorrowRecord


class UserRole(str, Enum):
    ADMIN = 'admin'
    LIBRARIAN = 'librarian'
    MEMBER = 'member'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    role: Mapped[UserRole] = mapped_column(String(12))
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),
    )

    borrow_records: Mapped[List['BorrowRecord']] = relationship(
        back_populates='user',
    )
