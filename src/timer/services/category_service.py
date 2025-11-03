from src.timer.repositories import CategoryRepository
from src.timer.models import Category


class CategoryNotFoundError(Exception): pass


class CategoryValidationError(Exception): pass


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create_category(self, category_data: dict) -> Category | None:
        """сервис метод для создания категории"""
        name = category_data.get("name")

        if not name or not name.strip():
            raise CategoryValidationError("Category name is required")

        if len(name.strip()) < 2:
            raise CategoryValidationError("Category name must be at least 2 characters")

        return await self.repo.persist(category_data)

    async def get_category(self, category_id: int) -> Category:
        """сервис метод для возвращения категории по id"""
        category = await self.repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} not found")
        return category
