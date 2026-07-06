from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from library_api.models import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),
    )
