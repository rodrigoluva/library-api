from datetime import date, datetime
from typing import Optional
from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from library_api.models import Base


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    bio: Mapped[Optional[str]] = mapped_column(Text, default=None)
    birthdate: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),
    )
