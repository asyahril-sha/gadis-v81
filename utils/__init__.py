#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
UTILITIES PACKAGE
=============================================================================
"""

from utils.logger import setup_logging, logger
from utils.exceptions import (
    GadisBaseException,
    DatabaseError,
    AIError,
    RateLimitError,
    SessionError,
    RoleError,
    ValidationError,
    global_exception_handler_obj,
    handle_errors
)
from utils.rate_limiter import RateLimiter, rate_limit, get_rate_limiter

__all__ = [
    # Logger
    'setup_logging',
    'logger',
    
    # Exceptions
    'GadisBaseException',
    'DatabaseError',
    'AIError',
    'RateLimitError',
    'SessionError',
    'RoleError',
    'ValidationError',
    'global_exception_handler_obj',
    'handle_errors',
    
    # Rate Limiter
    'RateLimiter',
    'rate_limit',
    'get_rate_limiter'
]
