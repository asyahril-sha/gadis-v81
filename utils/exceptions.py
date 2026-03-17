#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
EXCEPTION HANDLERS
=============================================================================
Global exception handling untuk bot
"""

import traceback
import sys
from typing import Optional, Dict, Any
from datetime import datetime
from loguru import logger

# Coba import settings, jika gagal buat dummy
try:
    from config import settings
except ImportError:
    class DummySettings:
        admin_id = None
        telegram_token = None
    settings = DummySettings()


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
        
        # Log error dengan loguru
        logger.opt(exception=error).error(f"Exception: {type(error).__name__}: {error}")
        
        if isinstance(error, GadisBaseException):
            return f"⚠️ {error.message}"
        
        # Notify admin untuk critical errors
        if isinstance(error, (DatabaseError, AIError)):
            await self._notify_admin(error, context or {})
        
        return "😔 Maaf, terjadi error. Coba lagi ya."
    
    async def _notify_admin(self, error: Exception, context: Dict):
        """Notify admin about critical errors"""
        if not settings.admin_id:
            return
        
        try:
            from telegram import Bot
            bot = Bot(token=settings.telegram_token)
            
            error_type = type(error).__name__
            error_msg = str(error)[:200]
            
            await bot.send_message(
                chat_id=settings.admin_id,
                text=f"🚨 *Critical Error*\n"
                     f"Type: `{error_type}`\n"
                     f"Message: `{error_msg}`\n"
                     f"Context: `{context}`",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")
    
    def get_stats(self) -> Dict:
        """Get error statistics"""
        return {
            'total_errors': self.error_count,
            'last_error': str(self.last_error) if self.last_error else None
        }


# Global exception handler untuk Python
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical("Uncaught exception")


# Set global exception handler
sys.excepthook = global_exception_handler


# Decorator for error handling
def handle_errors(func):
    """Decorator for error handling"""
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            handler = GlobalExceptionHandler()
            return await handler.handle(e, {'function': func.__name__})
    
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler = GlobalExceptionHandler()
            import asyncio
            loop = asyncio.new_event_loop()
            return loop.run_until_complete(handler.handle(e, {'function': func.__name__}))
    
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


# Global instance
global_exception_handler_obj = GlobalExceptionHandler()


__all__ = [
    'GadisBaseException',
    'DatabaseError',
    'AIError',
    'RateLimitError',
    'SessionError',
    'RoleError',
    'ValidationError',
    'global_exception_handler_obj',
    'handle_errors'
]
