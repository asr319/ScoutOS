import os
from .session_manager import (
    get_active_users_count as session_active_users_count,
)


async def get_storage_usage(path: str):
    stat = os.statvfs(path)
    total_bytes = stat.f_frsize * stat.f_blocks
    used_bytes = total_bytes - (stat.f_frsize * stat.f_bfree)
    return used_bytes, total_bytes


async def get_active_users_count():
    return await session_active_users_count()
