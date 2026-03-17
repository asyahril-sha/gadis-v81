#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
EXCEPTION HANDLERS
=============================================================================
Global exception handling untuk bot
"""

import traceback
from typing import Optional, Dict, Any
from datetime import datetime

from utils.logger import logger
from config import settings


class GadisBaseException(Exception):
    """Base exception class"""
    def __init__(self, message: str, code: int = 500, details: Optional[Dict] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(message)


class DatabaseError(GadisBaseException):
    """Database related errors"""
    pass


class AIError(GadisBaseException):
    """AI API related errors"""
    pass


class RateLimitError(GadisBaseException):
    """Rate limiting errors"""
    def __init__(self, message: str, retry_after: int, details: Optional[Dict] = None):
        details = details or {}
        details['retry_after'] = retry_after
        super().__init__(message, 429, details)


class SessionError(GadisBaseException):
    """Session related errors"""
    pass


class RoleError(GadisBaseException):
    """Role related errors"""
    pass


class ValidationError(GadisBaseException):
    """Input validation errors"""
    pass


class GlobalExceptionHandler:
    """Global exception handler"""
    
    def __init__(self):
        self.error_count = 0
        self.last_error = None
    
    async def handle(self, error: Exception, context: Dict[str, Any] = None) -> str:
        """Handle exception"""
        self.error_count += 1
        self.last_error = error
        
        logger.error(f"Exception: {type(error).__name__}: {error}")
        logger.debug(traceback.format_exc())
        
        if isinstance(error, GadisBaseException):
            return f"⚠️ {error.message}"
        
        return "😔 Maaf, terjadi error. Coba lagi ya."
    
    async def _notify_admin(self, error: Exception, context: Dict):
        """Notify admin about critical errors"""
        if not settings.admin_id:
            return
        
        try:
            from telegram import Bot
            bot = Bot(token=settings.telegram_token)
            
            await bot.send_message(
                chat_id=settings.admin_id,
                text=f"🚨 Error: {type(error).__name__}\n{str(error)[:200]}"
            )
        except:
            pass
    
    def get_stats(self) -> Dict:
        """Get error statistics"""
        return {
            'total_errors': self.error_count,
            'last_error': str(self.last_error) if self.last_error else None
        }


# Decorator for error handling
def handle_errors(func):
    """Decorator for error handling"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            handler = GlobalExceptionHandler()
            return await handler.handle(e, {'function': func.__name__})
    return wrapper


# Global instance
global_exception_handler = GlobalExceptionHandler()


__all__ = [
    'GadisBaseException',
    'DatabaseError',
    'AIError',
    'RateLimitError',
    'SessionError',
    'RoleError',
    'ValidationError',
    'global_exception_handler',
    'handle_errors'
]
