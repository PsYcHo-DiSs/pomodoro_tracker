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

# TODO:
# DeleteAllCategoriesResponse model