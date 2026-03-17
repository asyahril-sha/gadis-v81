#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
REDIS CLIENT SEDERHANA
=============================================================================
Redis client sederhana (mock) - tidak perlu Redis sungguhan
"""

from typing import Optional, Any, Dict
from utils.logger import logger


class RedisClient:
    """Redis client sederhana (mock)"""
    
    def __init__(self):
        self._connected = False
        self._cache = {}
    
    async def initialize(self):
        """Initialize Redis (mock)"""
        self._connected = True
        logger.info("✅ Redis mock initialized (no actual Redis)")
    
    async def close(self):
        """Close Redis connection"""
        self._connected = False
        self._cache.clear()
        logger.info("✅ Redis mock closed")
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        return self._cache.get(key, default)
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        self._cache[key] = value
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return key in self._cache
    
    def is_connected(self) -> bool:
        """Check if connected"""
        return self._connected


# ===== FUNGSI YANG DIBUTUHKAN =====
async def init_redis():
    """Initialize Redis (dipanggil di main.py)"""
    await redis_client.initialize()


async def close_redis():
    """Close Redis connection"""
    await redis_client.close()


# ===== GLOBAL INSTANCE =====
redis_client = RedisClient()


__all__ = ['redis_client', 'init_redis', 'close_redis']
