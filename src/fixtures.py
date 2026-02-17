from src.timer.schemas import TaskCreate, Category

tasks = [
    TaskCreate(id=1, name="Task 1", pomodoro_count=10, category_id=1),
    TaskCreate(id=2, name="Task 2", pomodoro_count=5, category_id=2),
    TaskCreate(id=3, name="Task 3", pomodoro_count=3, category_id=3),
    TaskCreate(id=4, name="Task 4", pomodoro_count=8, category_id=4),
]

categories = [
    Category(id=1, name="Category 1"),
    Category(id=2, name="Category 2"),
    Category(id=3, name="Category 3"),
    Category(id=4, name="Category 4"),
]
