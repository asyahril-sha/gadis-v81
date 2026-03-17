#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
DISTRIBUTED LOCKS
=============================================================================
Redis-based distributed locking (di-sederhanakan untuk single-user)
"""

import threading
import asyncio
from typing import Optional
from datetime import datetime, timedelta


class DistributedLock:
    """
    Distributed lock menggunakan Redis
    DISEDERHANAKAN UNTUK SINGLE-USER - pakai threading.Lock
    """
    
    def __init__(self, lock_name: str, timeout: int = 30):
        self.lock_name = lock_name
        self.timeout = timeout
        self._lock = threading.Lock()
        self._async_lock = asyncio.Lock()
        self.owner = None
        self.acquired_at = None
    
    def acquire(self, blocking: bool = True) -> bool:
        """Acquire lock (threading version)"""
        if blocking:
            acquired = self._lock.acquire()
        else:
            acquired = self._lock.acquire(blocking=False)
        
        if acquired:
            self.owner = threading.current_thread().name
            self.acquired_at = datetime.now()
        
        return acquired
    
    def release(self):
        """Release lock"""
        if self._lock.locked():
            self._lock.release()
            self.owner = None
            self.acquired_at = None
    
    async def acquire_async(self) -> bool:
        """Acquire lock (async version)"""
        await self._async_lock.acquire()
        self.owner = f"async-{id(asyncio.current_task())}"
        self.acquired_at = datetime.now()
        return True
    
    async def release_async(self):
        """Release lock (async version)"""
        if self._async_lock.locked():
            self._async_lock.release()
            self.owner = None
            self.acquired_at = None
    
    def is_locked(self) -> bool:
        """Check if lock is held"""
        return self._lock.locked() or self._async_lock.locked()
    
    def get_owner(self) -> Optional[str]:
        """Get current lock owner"""
        return self.owner
    
    def get_age(self) -> Optional[float]:
        """Get lock age in seconds"""
        if self.acquired_at:
            return (datetime.now() - self.acquired_at).total_seconds()
        return None
    
    def __enter__(self):
        """Context manager support"""
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support"""
        self.release()


class LockManager:
    """Manager untuk distributed locks"""
    
    def __init__(self):
        self.locks = {}
    
    def get_lock(self, lock_name: str, timeout: int = 30) -> DistributedLock:
        """Get or create lock"""
        if lock_name not in self.locks:
            self.locks[lock_name] = DistributedLock(lock_name, timeout)
        return self.locks[lock_name]
    
    def release_all(self):
        """Release all locks"""
        for lock in self.locks.values():
            if lock.is_locked():
                lock.release()


# ===== SINGLETON =====
lock_manager = LockManager()


__all__ = ['DistributedLock', 'lock_manager', 'LockManager']
