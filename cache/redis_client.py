#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
REDIS CLIENT FOR CACHING
=============================================================================
Redis connection pool untuk caching dan rate limiting
"""

import json
import pickle
from typing import Optional, Any, Dict, List
from datetime import timedelta

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from config import settings
from utils.logger import logger


class RedisClient:
    """
    Redis client dengan connection pooling
    - Async support
    - Auto reconnect
    - Serialization/deserialization
    """
    
    def __init__(self):
        self.client = None
        self._connected = False
    
    async def initialize(self):
        """Initialize Redis connection"""
        if self._connected:
            return
        
        if not REDIS_AVAILABLE:
            logger.warning("Redis not available, using fallback")
            return
        
        try:
            # Create connection pool
            self.client = await redis.from_url(
                settings.redis.url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=10,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            
            # Test connection
            await self.client.ping()
            self._connected = True
            logger.info(f"✅ Redis connected: {settings.redis.host}:{settings.redis.port}")
            
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.client = None
    
    async def close(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            self._connected = False
            logger.info("✅ Redis connection closed")
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from Redis"""
        if not self.client:
            return default
        
        try:
            value = await self.client.get(key)
            if value is None:
                return default
            
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except:
                return value
                
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return default
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in Redis with optional TTL"""
        if not self.client:
            return False
        
        try:
            # Serialize to JSON if dict/list
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if ttl:
                await self.client.setex(key, ttl, value)
            else:
                await self.client.set(key, value)
            
            return True
            
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.client:
            return False
        
        try:
            result = await self.client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.client:
            return False
        
        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    async def incr(self, key: str) -> Optional[int]:
        """Increment counter"""
        if not self.client:
            return None
        
        try:
            return await self.client.incr(key)
        except Exception as e:
            logger.error(f"Redis incr error: {e}")
            return None
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on key"""
        if not self.client:
            return False
        
        try:
            return await self.client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Redis expire error: {e}")
            return False
    
    async def ttl(self, key: str) -> Optional[int]:
        """Get TTL for key"""
        if not self.client:
            return None
        
        try:
            return await self.client.ttl(key)
        except Exception as e:
            logger.error(f"Redis ttl error: {e}")
            return None
    
    async def hset(self, key: str, field: str, value: Any) -> bool:
        """Set hash field"""
        if not self.client:
            return False
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            await self.client.hset(key, field, value)
            return True
        except Exception as e:
            logger.error(f"Redis hset error: {e}")
            return False
    
    async def hget(self, key: str, field: str, default: Any = None) -> Any:
        """Get hash field"""
        if not self.client:
            return default
        
        try:
            value = await self.client.hget(key, field)
            if value is None:
                return default
            
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except:
                return value
                
        except Exception as e:
            logger.error(f"Redis hget error: {e}")
            return default
    
    async def hgetall(self, key: str) -> Dict:
        """Get all hash fields"""
        if not self.client:
            return {}
        
        try:
            result = await self.client.hgetall(key)
            # Try to deserialize values
            deserialized = {}
            for k, v in result.items():
                try:
                    deserialized[k] = json.loads(v)
                except:
                    deserialized[k] = v
            return deserialized
        except Exception as e:
            logger.error(f"Redis hgetall error: {e}")
            return {}
    
    async def sadd(self, key: str, *values) -> int:
        """Add to set"""
        if not self.client:
            return 0
        
        try:
            return await self.client.sadd(key, *values)
        except Exception as e:
            logger.error(f"Redis sadd error: {e}")
            return 0
    
    async def smembers(self, key: str) -> set:
        """Get all set members"""
        if not self.client:
            return set()
        
        try:
            return await self.client.smembers(key)
        except Exception as e:
            logger.error(f"Redis smembers error: {e}")
            return set()
    
    async def srem(self, key: str, *values) -> int:
        """Remove from set"""
        if not self.client:
            return 0
        
        try:
            return await self.client.srem(key, *values)
        except Exception as e:
            logger.error(f"Redis srem error: {e}")
            return 0
    
    async def lpush(self, key: str, *values) -> int:
        """Push to list"""
        if not self.client:
            return 0
        
        try:
            # Serialize values
            serialized = [json.dumps(v) if isinstance(v, (dict, list)) else str(v) for v in values]
            return await self.client.lpush(key, *serialized)
        except Exception as e:
            logger.error(f"Redis lpush error: {e}")
            return 0
    
    async def lrange(self, key: str, start: int, end: int) -> List:
        """Get list range"""
        if not self.client:
            return []
        
        try:
            values = await self.client.lrange(key, start, end)
            # Deserialize
            result = []
            for v in values:
                try:
                    result.append(json.loads(v))
                except:
                    result.append(v)
            return result
        except Exception as e:
            logger.error(f"Redis lrange error: {e}")
            return []
    
    async def flush_all(self) -> bool:
        """Flush all keys (dangerous!)"""
        if not self.client:
            return False
        
        try:
            await self.client.flushall()
            logger.warning("⚠️ Redis flushed all keys")
            return True
        except Exception as e:
            logger.error(f"Redis flush error: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self._connected and self.client is not None


# ===== GLOBAL INSTANCE =====
redis_client = RedisClient()


__all__ = ['redis_client', 'RedisClient']
