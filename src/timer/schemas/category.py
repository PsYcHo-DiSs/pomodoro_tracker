from pydantic import BaseModel, ConfigDict, Field


class Category(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdate(BaseModel):
    name: str = Field(
        None,
        description="Название категории. Обязательное поле."
    )

    model_config = ConfigDict(from_attributes=True)


class DeleteAllCategoriesResponse(BaseModel):
    message: str
    deleted_count: int


class BatchDeleteCategoriesRequest(BaseModel):
    category_ids: list[int] = Field(..., min_length=1, description="Список ID категорий для удаления")


class BatchDeleteCategoriesResponse(BaseModel):
    message: str
    deleted_count: int
    requested_count: int
