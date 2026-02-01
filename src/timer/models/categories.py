from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from .base import Base
# from .tasks import Task


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[Optional[str]]
    name: Mapped[str] = mapped_column(Text)

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"
