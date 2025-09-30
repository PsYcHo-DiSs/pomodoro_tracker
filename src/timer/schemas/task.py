from pydantic import BaseModel, Field, model_validator


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int = Field(exclude=True)

    @model_validator(mode="after")
    def is_not_none_check(self, value):
        if self.name is None or self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        return self


