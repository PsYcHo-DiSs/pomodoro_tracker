import time
import asyncio
from typing import Union
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class Person(BaseModel):
    name: str | None
    age: int


@app.get(
    "/person",
    description="Get Hello World",
    response_model=Person)
def get_person():
    return {"name": "Artem",
            "age": 34}


async def get_users():
    await asyncio.sleep(3)
    return 1


async def get_wiki():
    await asyncio.sleep(3)
    return 2


@app.post("/person",
          response_model=Person)
async def create_person(person: Person):
    users, wiki = await asyncio.gather(get_users(), get_wiki())
    return person
