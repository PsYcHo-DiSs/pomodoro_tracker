from typing import AsyncGenerator
import redis.asyncio as redis
from src.timer.config import get_settings

settings = get_settings()

async def get_redis_session() -> AsyncGenerator[redis.Redis, None]:
    """Получение асинхронной Redis сессии"""
    print(f"Connecting to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")  # Для отладки

    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
        socket_connect_timeout=2
    )
    try:
        # Проверим подключение
        await client.ping()
        print("✅ Redis connected successfully")
        yield client
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        yield None  # Возвращаем None, чтобы приложение не падало
    finally:
        if client:
            await client.aclose()