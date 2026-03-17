#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
RATE LIMITER UTILITY
=============================================================================
"""

import time
import asyncio
import threading
from collections import defaultdict
from typing import Dict, Tuple, Optional, List, Callable, Any
from functools import wraps
from loguru import logger

from utils.exceptions import RateLimitError


class RateLimiter:
    """
    Rate limiter untuk membatasi frekuensi request
    """
    
    def __init__(self, max_requests: int = 10, time_window: int = 60, name: str = "default"):
        """
        Args:
            max_requests: Jumlah maksimum request dalam time_window
            time_window: Window waktu dalam detik
            name: Nama rate limiter untuk logging
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.name = name
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.RLock()
        self.total_requests = 0
        self.blocked_requests = 0
    
    def is_allowed(self, key: str) -> Tuple[bool, Optional[int]]:
        """
        Cek apakah request diizinkan
        
        Returns:
            (diizinkan, waktu_tunggu_detik)
        """
        with self.lock:
            now = time.time()
            cutoff = now - self.time_window
            
            # Bersihkan request lama
            self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff]
            
            if len(self.requests[key]) >= self.max_requests:
                # Hitung waktu tunggu
                oldest = min(self.requests[key])
                wait_time = int(oldest + self.time_window - now)
                self.blocked_requests += 1
                return False, wait_time
            
            return True, None
    
    def add_request(self, key: str):
        """Catat request baru"""
        with self.lock:
            self.requests[key].append(time.time())
            self.total_requests += 1
    
    def check(self, key: str) -> bool:
        """
        Cek dan catat request (gabungan is_allowed + add_request)
        
        Raises:
            RateLimitError jika melebihi batas
        """
        allowed, wait_time = self.is_allowed(key)
        if not allowed:
            logger.warning(f"[{self.name}] Rate limit exceeded for {key}, wait {wait_time}s")
            raise RateLimitError(
                f"Terlalu banyak permintaan. Tunggu {wait_time} detik.",
                retry_after=wait_time,
                details={
                    "key": key,
                    "limiter": self.name,
                    "limit": self.max_requests,
                    "window": self.time_window
                }
            )
        self.add_request(key)
        return True
    
    async def acheck(self, key: str) -> bool:
        """Async version of check"""
        return self.check(key)
    
    def get_remaining(self, key: str) -> int:
        """Dapatkan sisa request yang diizinkan"""
        with self.lock:
            now = time.time()
            cutoff = now - self.time_window
            self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff]
            return max(0, self.max_requests - len(self.requests[key]))
    
    def reset(self, key: Optional[str] = None):
        """Reset rate limiter"""
        with self.lock:
            if key:
                self.requests.pop(key, None)
                logger.debug(f"[{self.name}] Rate limiter reset for {key}")
            else:
                self.requests.clear()
                logger.debug(f"[{self.name}] Rate limiter fully reset")
    
    def get_stats(self, key: Optional[str] = None) -> Dict:
        """Dapatkan statistik rate limiter"""
        with self.lock:
            if key:
                now = time.time()
                cutoff = now - self.time_window
                recent = [ts for ts in self.requests.get(key, []) if ts > cutoff]
                return {
                    'key': key,
                    'current': len(recent),
                    'max': self.max_requests,
                    'remaining': self.max_requests - len(recent),
                    'window': self.time_window
                }
            else:
                return {
                    'name': self.name,
                    'total_keys': len(self.requests),
                    'max_requests': self.max_requests,
                    'time_window': self.time_window,
                    'total_requests': self.total_requests,
                    'blocked_requests': self.blocked_requests,
                    'block_rate': (self.blocked_requests / max(1, self.total_requests)) * 100
                }


def rate_limit(max_requests: int = 10, time_window: int = 60, limiter_name: str = "default", key_func: Optional[Callable] = None):
    """
    Decorator untuk rate limiting
    
    Args:
        max_requests: Maksimum requests
        time_window: Window waktu dalam detik
        limiter_name: Nama rate limiter
        key_func: Function untuk mendapatkan key (default: user_id dari args)
    
    Contoh:
        @rate_limit(max_requests=5, time_window=30)
        async def handle_message(user_id, message):
            ...
    """
    limiter = RateLimiter(max_requests, time_window, limiter_name)
    
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Dapatkan key
            if key_func:
                key = str(key_func(*args, **kwargs))
            else:
                # Default: coba ambil user_id dari args atau kwargs
                key = None
                if args and len(args) > 0:
                    key = str(args[0])
                elif 'user_id' in kwargs:
                    key = str(kwargs['user_id'])
                elif 'user' in kwargs:
                    key = str(kwargs['user'])
                else:
                    key = 'default'
            
            # Check rate limit
            limiter.check(key)
            
            # Execute function
            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Dapatkan key
            if key_func:
                key = str(key_func(*args, **kwargs))
            else:
                key = 'default'
                if args and len(args) > 0:
                    key = str(args[0])
                elif 'user_id' in kwargs:
                    key = str(kwargs['user_id'])
            
            # Check rate limit
            limiter.check(key)
            
            # Execute function
            return func(*args, **kwargs)
        
        # Pilih wrapper berdasarkan tipe function
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


# Singleton instances
_rate_limiters: Dict[str, RateLimiter] = {}


def get_rate_limiter(name: str = "default", max_requests: int = 10, time_window: int = 60) -> RateLimiter:
    """Dapatkan atau buat instance RateLimiter"""
    if name not in _rate_limiters:
        _rate_limiters[name] = RateLimiter(max_requests, time_window, name)
    return _rate_limiters[name]


__all__ = ['RateLimiter', 'rate_limit', 'get_rate_limiter']
