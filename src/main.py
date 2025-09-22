from fastapi import FastAPI
from .timer.handlers import routers as timer_routers
from .analytics.handlers import routers as analytics_routers

app = FastAPI(title="Pomodoro Tracker")

all_routers = timer_routers + analytics_routers

for router in all_routers:
    app.include_router(router)
