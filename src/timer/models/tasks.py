from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    pomodoro_count: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship("Category", back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, name='{self.name}', category_id={self.category_id})"
