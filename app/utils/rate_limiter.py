import logging
from datetime import timedelta

from app.cache.redis import redis_cache


async def initialize_limit(key: str, limit: int=2):
    result = await redis_cache.set_key(
        key=key,
        value=limit,
        expire=timedelta(seconds=180)

    )
    logging.info(f"Rate Limit Initialized for: {str(result)}")


async def request_is_limited(key: str) -> bool:
    limit = await redis_cache.get_key(key)

    if limit is not None and int(limit) > 0:
        await redis_cache.incr_key_val(key, -1)
        return False

    if limit is None:
        logging.info(f"LIMIT NOT SET OR EXPIRED. LIMIT = { limit }")
        await initialize_limit(key=key)
        return False
    
    if int(limit) <= 0:
        logging.info(f"RATE LIMIT EXCEEDED { limit }")
        return True
