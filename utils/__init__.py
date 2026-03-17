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
    global_exception_handler,
    handle_errors
)

__all__ = [
    'setup_logging',
    'logger',
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
