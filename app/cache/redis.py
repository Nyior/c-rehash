from typing import Any, Optional
import logging

import aioredis


class RedisCache:
    """
    Holds a pool of connections to the redis server.
    The goal is to abstract connection logic and reuse connections from a pool.
    """

    pool: Optional[aioredis.Redis] = None

    async def start(self):
        """
        Creates the pool of connections.
        """
        self.pool = aioredis.from_url(
            "redis://localhost:6379/0?encoding=utf-8", max_connections=100
        )

    async def set_key(
        self, key: str, value: Any, expire: Optional[int] = None
    ) -> None:
        """
        Sets the value for a key in the cache.

        Args:
            key (str): key
            value (str): value to save
            expire (int, optional): expire time (in seconds). Defaults to None.
        """
        # Execute SET command
        result = await self.pool.execute_command("set", key, value)

        # If expire is set, execute an additional command
        if expire is not None:
            _ = await self.pool.execute_command("expire", key, expire)

        return result

    async def get_key(self, key: str) -> Optional[str]:
        """
        Gets the value for a key.

        Args:
            key (str): key

        Returns:
            str: value. Defaults to None if the key does not exist.
        """
        return await self.pool.execute_command("get", key)

    async def close(self) -> None:
        """Closes pool of connections"""
        await self.pool.close()


# We'll initialize the redis_cache variable, which should be re-used across the
# codebase (think singleton pattern)
redis_cache = RedisCache()