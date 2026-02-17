from pydantic import BaseModel, Field, model_validator, ConfigDict


class TaskCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    pomodoro_count: int = Field(..., gt=0, le=100)
    category_id: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)
    pomodoro_count: int | None = Field(None, gt=0, le=100)
    category_id: int | None = Field(None, gt=0)


class TaskResponse(BaseModel):
    id: int
    name: str
    pomodoro_count: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)


# ----- ДЛЯ КЕША (отдельная схема!) -----
class TaskCacheSchema(BaseModel):
    """Схема ТОЛЬКО для кеша - минимальные поля"""
    id: int
    name: str
    pomodoro_count: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)

    # Можно добавить вспомогательные методы
    def to_redis(self) -> str:
        """Подготовка для сохранения в Redis"""
        return self.model_dump_json()

    @classmethod
    def from_redis(cls, data: str) -> 'TaskCacheSchema':
        """Восстановление из Redis"""
        return cls.model_validate_json(data)


class DeleteAllTasksResponse(BaseModel):
    message: str
    deleted_count: int


class BatchDeleteTasksRequest(BaseModel):
    tasks_ids: list[int] = Field(..., min_length=1, description="Список ID задач для удаления")


class BatchDeleteTasksResponse(BaseModel):
    message: str
    deleted_count: int
    requested_count: int
