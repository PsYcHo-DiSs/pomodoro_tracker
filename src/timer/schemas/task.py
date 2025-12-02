from pydantic import BaseModel, Field, model_validator, ConfigDict


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def is_not_none_check(self, value):
        if self.name is None or self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        return self


class TaskUpdate(BaseModel):
    name: str | None = Field(
        None,
        description="Название задачи. Опциональное поле."
    )
    pomodoro_count: int | None = Field(
        None,
        description="Количество помодоро. Опциональное поле."
    )
    category_id: int | None = Field(
        None,
        description="ID категории. Опциональное поле."
    )


class DeleteAllTasksResponse(BaseModel):
    message: str
    deleted_count: int

