from .base import Base
from .tasks import Task
from .categories import Category

# Явно перечисляем все модели для Alembic
__all__ = ["Base", "Task", "Category"]