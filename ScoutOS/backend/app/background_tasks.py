import asyncio
import json
from .metrics_utils import get_storage_usage, get_active_users_count
from .metrics import ACTIVE_USERS_TOTAL, STORAGE_USED_BYTES, STORAGE_TOTAL_BYTES
from .websocket_manager import manager


async def update_metrics_periodically():
    while True:
        active_users = await get_active_users_count()
        ACTIVE_USERS_TOTAL.set(active_users)

        used_bytes, total_bytes = await get_storage_usage("/")
        STORAGE_USED_BYTES.set(used_bytes)
        STORAGE_TOTAL_BYTES.set(total_bytes)

        metrics_data = {
            "active_users": active_users,
            "storage_used_bytes": used_bytes,
            "storage_total_bytes": total_bytes,
        }
        await manager.broadcast(json.dumps({"type": "metrics", "data": metrics_data}))

        await asyncio.sleep(60)


async def start_background_tasks():
    asyncio.create_task(update_metrics_periodically())
