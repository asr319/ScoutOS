import asyncio
from metrics_utils import get_storage_usage, get_active_users_count
from metrics import ACTIVE_USERS_TOTAL, STORAGE_USED_BYTES, STORAGE_TOTAL_BYTES


async def update_metrics_periodically():
    while True:
        active_users = await get_active_users_count()
        ACTIVE_USERS_TOTAL.set(active_users)

        used_bytes, total_bytes = await get_storage_usage("/")
        STORAGE_USED_BYTES.set(used_bytes)
        STORAGE_TOTAL_BYTES.set(total_bytes)

        await asyncio.sleep(60)


async def start_background_tasks():
    asyncio.create_task(update_metrics_periodically())
