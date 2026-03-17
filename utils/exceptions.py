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
from typing import Optional, Dict, Any, List
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
        self.error_history: List[Dict] = []
    
    async def handle(self, error: Exception, context: Dict[str, Any] = None) -> str:
        """Handle exception"""
        self.error_count += 1
        self.last_error = error
        context = context or {}
        
        # Simpan ke history
        self.error_history.append({
            'error': str(error),
            'type': type(error).__name__,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        
        # Batasi history
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-100:]
        
        # Log error dengan loguru
        logger.opt(exception=error).error(f"Exception: {type(error).__name__}: {error}")
        
        if isinstance(error, GadisBaseException):
            return self._format_error_message(error)
        
        # Notify admin untuk critical errors
        if isinstance(error, (DatabaseError, AIError)):
            await self._notify_admin(error, context)
        
        return "😔 Maaf, terjadi error internal. Coba lagi ya."
    
    async def __call__(self, error: Exception, context: Dict[str, Any] = None) -> str:
        """Make instance callable like a function"""
        return await self.handle(error, context)
    
    def _format_error_message(self, error: GadisBaseException) -> str:
        """Format error message untuk user"""
        if isinstance(error, RateLimitError):
            return f"⏱️ {error.message}"
        elif isinstance(error, ValidationError):
            return f"❌ {error.message}"
        elif isinstance(error, RoleError):
            return f"🔒 {error.message}"
        else:
            return f"⚠️ {error.message}"
    
    async def _notify_admin(self, error: Exception, context: Dict):
        """Notify admin about critical errors"""
        if not settings.admin_id:
            return
        
        try:
            from telegram import Bot
            bot = Bot(token=settings.telegram_token)
            
            error_type = type(error).__name__
            error_msg = str(error)[:200]
            context_str = str(context)[:200]
            
            await bot.send_message(
                chat_id=settings.admin_id,
                text=f"🚨 *Critical Error*\n"
                     f"Type: `{error_type}`\n"
                     f"Message: `{error_msg}`\n"
                     f"Context: `{context_str}`",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")
    
    def get_stats(self) -> Dict:
        """Get error statistics"""
        return {
            'total_errors': self.error_count,
            'last_error': str(self.last_error) if self.last_error else None,
            'error_types': self._count_error_types(),
            'recent_errors': self.error_history[-5:] if self.error_history else []
        }
    
    def _count_error_types(self) -> Dict:
        """Count errors by type"""
        counts = {}
        for entry in self.error_history:
            error_type = entry['type']
            counts[error_type] = counts.get(error_type, 0) + 1
        return counts


# Global exception handler untuk Python (sync)
def sync_global_exception_handler(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical("🔥 Uncaught exception")


# Set global exception handler
sys.excepthook = sync_global_exception_handler


# Decorator for error handling
def handle_errors(func):
    """Decorator for error handling"""
    import asyncio
    import functools
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            handler = GlobalExceptionHandler()
            return await handler.handle(e, {'function': func.__name__})
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler = GlobalExceptionHandler()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(handler.handle(e, {'function': func.__name__}))
            finally:
                loop.close()
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


# Global instance
exception_handler = GlobalExceptionHandler()

# Untuk backward compatibility dengan kode lama
global_exception_handler_obj = exception_handler
global_exception_handler = exception_handler  # Ini penting!


__all__ = [
    'GadisBaseException',
    'DatabaseError',
    'AIError',
    'RateLimitError',
    'SessionError',
    'RoleError',
    'ValidationError',
    'exception_handler',
    'global_exception_handler_obj',
    'global_exception_handler',  # Tambahkan ini
    'handle_errors'
]
