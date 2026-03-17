#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SESSION STORE WITH REDIS
=============================================================================
Session management menggunakan Redis untuk state persistence
"""

import json
import pickle
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from cache.redis_client import redis_client
from utils.logger import logger


class SessionStore:
    """
    Session storage dengan Redis backend
    - Auto-expiry sessions
    - Serialization/deserialization
    - Distributed support
    """
    
    def __init__(self, prefix: str = "session:"):
        self.prefix = prefix
        self.default_ttl = 3600  # 1 hour
    
    def _make_key(self, session_id: str) -> str:
        """Create Redis key with prefix"""
        return f"{self.prefix}{session_id}"
    
    async def save(self, session_id: str, data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Save session data"""
        key = self._make_key(session_id)
        
        # Add metadata
        data['_last_accessed'] = datetime.now().isoformat()
        
        return await redis_client.set(key, data, ttl or self.default_ttl)
    
    async def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        key = self._make_key(session_id)
        data = await redis_client.get(key)
        
        if data:
            # Update last accessed
            await self.touch(session_id)
        
        return data
    
    async def delete(self, session_id: str) -> bool:
        """Delete session"""
        key = self._make_key(session_id)
        return await redis_client.delete(key)
    
    async def exists(self, session_id: str) -> bool:
        """Check if session exists"""
        key = self._make_key(session_id)
        return await redis_client.exists(key)
    
    async def touch(self, session_id: str, ttl: Optional[int] = None) -> bool:
        """Update session TTL"""
        key = self._make_key(session_id)
        
        # Update last accessed in data
        data = await self.get(session_id)
        if data:
            data['_last_accessed'] = datetime.now().isoformat()
            return await self.save(session_id, data, ttl)
        
        return False
    
    async def update(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update specific fields in session"""
        data = await self.get(session_id)
        if not data:
            return False
        
        data.update(updates)
        return await self.save(session_id, data)
    
    async def get_field(self, session_id: str, field: str, default: Any = None) -> Any:
        """Get specific field from session"""
        data = await self.get(session_id)
        if not data:
            return default
        
        return data.get(field, default)
    
    async def set_field(self, session_id: str, field: str, value: Any) -> bool:
        """Set specific field in session"""
        return await self.update(session_id, {field: value})
    
    async def clear_all(self) -> bool:
        """Clear all sessions (dangerous!)"""
        try:
            # Get all session keys
            import redis
            pattern = f"{self.prefix}*"
            
            if redis_client.client:
                keys = await redis_client.client.keys(pattern)
                if keys:
                    await redis_client.client.delete(*keys)
                    logger.warning(f"⚠️ Cleared {len(keys)} sessions")
            
            return True
        except Exception as e:
            logger.error(f"Failed to clear sessions: {e}")
            return False
    
    async def get_all_sessions(self) -> Dict[str, Dict]:
        """Get all active sessions (for admin)"""
        sessions = {}
        try:
            pattern = f"{self.prefix}*"
            if redis_client.client:
                keys = await redis_client.client.keys(pattern)
                for key in keys:
                    session_id = key.replace(self.prefix, "")
                    data = await self.get(session_id)
                    if data:
                        sessions[session_id] = data
        except Exception as e:
            logger.error(f"Failed to get all sessions: {e}")
        
        return sessions
    
    async def get_active_count(self) -> int:
        """Get number of active sessions"""
        try:
            pattern = f"{self.prefix}*"
            if redis_client.client:
                keys = await redis_client.client.keys(pattern)
                return len(keys)
        except Exception as e:
            logger.error(f"Failed to get active count: {e}")
        
        return 0


class UserSessionStore(SessionStore):
    """
    Session store khusus untuk user sessions
    """
    
    def __init__(self):
        super().__init__(prefix="user:")
    
    async def save_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        """Save user data"""
        return await self.save(str(user_id), data)
    
    async def get_user_data(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        return await self.get(str(user_id))
    
    async def delete_user_data(self, user_id: int) -> bool:
        """Delete user data"""
        return await self.delete(str(user_id))
    
    async def update_user_data(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user data"""
        return await self.update(str(user_id), updates)


class BotSessionStore(SessionStore):
    """
    Session store khusus untuk bot sessions
    """
    
    def __init__(self):
        super().__init__(prefix="bot:")
    
    async def save_bot_state(self, bot_id: str, state: Dict[str, Any]) -> bool:
        """Save bot state"""
        return await self.save(bot_id, state)
    
    async def get_bot_state(self, bot_id: str) -> Optional[Dict]:
        """Get bot state"""
        return await self.get(bot_id)
    
    async def delete_bot_state(self, bot_id: str) -> bool:
        """Delete bot state"""
        return await self.delete(bot_id)


# ===== GLOBAL INSTANCES =====
user_session_store = UserSessionStore()
bot_session_store = BotSessionStore()


__all__ = [
    'SessionStore',
    'UserSessionStore',
    'BotSessionStore',
    'user_session_store',
    'bot_session_store'
]
