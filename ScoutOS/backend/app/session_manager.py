import aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
SESSION_PREFIX = "session:"

redis = None


async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis


async def create_session(
    user_id: str,
    session_id: str,
    expire_seconds: int = 3600,
):
    r = await get_redis()
    key = f"{SESSION_PREFIX}{session_id}"
    await r.set(key, user_id, ex=expire_seconds)


async def get_user_by_session(session_id: str):
    r = await get_redis()
    key = f"{SESSION_PREFIX}{session_id}"
    return await r.get(key)


async def delete_session(session_id: str):
    r = await get_redis()
    key = f"{SESSION_PREFIX}{session_id}"
    await r.delete(key)


async def get_active_users_count():
    r = await get_redis()
    keys = await r.keys(f"{SESSION_PREFIX}*")
    return len(keys)
