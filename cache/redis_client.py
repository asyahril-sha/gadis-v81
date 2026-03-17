#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
REDIS CLIENT
=============================================================================
"""

import asyncio
from typing import Optional, Any
from utils.logger import logger


# Mock Redis untuk development
class MockRedis:
    def __init__(self):
        self._data = {}
    
    async def get(self, key):
        return self._data.get(key)
    
    async def set(self, key, value, ex=None):
        self._data[key] = value
        return True
    
    async def delete(self, key):
        if key in self._data:
            del self._data[key]
            return 1
        return 0
    
    async def close(self):
        self._data.clear()


_redis_client: Optional[MockRedis] = None


# ===== ASYNC VERSIONS =====

async def init_redis():
    """Initialize Redis asynchronously"""
    global _redis_client
    _redis_client = MockRedis()
    logger.info("✅ Redis mock initialized (async)")
    return _redis_client


async def get_redis():
    """Get Redis client asynchronously"""
    return _redis_client


async def close_redis():
    """Close Redis asynchronously"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("✅ Redis mock closed (async)")


# ===== SYNC WRAPPERS =====

def init_redis_sync():
    """Initialize Redis synchronously"""
    import asyncio
    return asyncio.run(init_redis())


def close_redis_sync():
    """Close Redis synchronously"""
    import asyncio
    return asyncio.run(close_redis())


__all__ = [
    'init_redis',
    'get_redis',
    'close_redis',
    'init_redis_sync',  # ← Tambahkan ini
    'close_redis_sync'   # ← Tambahkan ini
]
