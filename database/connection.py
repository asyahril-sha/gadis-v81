#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
POSTGRESQL CONNECTION POOL
=============================================================================
Async connection pool dengan SQLAlchemy + asyncpg
"""

import asyncio
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy import text

from config import settings
from utils.logger import logger


class DatabaseManager:
    """
    Manajemen koneksi database PostgreSQL
    - Connection pooling
    - Async sessions
    - Health checks
    - Query logging
    """
    
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.async_session_maker: Optional[async_sessionmaker] = None
        self._connection_lock = asyncio.Lock()
        self._stats = {
            "connections_created": 0,
            "connections_closed": 0,
            "queries_executed": 0,
            "errors": 0
        }
    
    async def initialize(self):
        """Initialize database connection pool"""
        async with self._connection_lock:
            if self.engine is not None:
                return
            
            # Database URL from settings
            database_url = settings.db.url
            
            # Connection pool configuration
            pool_config = {
                "pool_size": settings.db.pool_size,
                "max_overflow": settings.db.max_overflow,
                "pool_pre_ping": True,  # Check connection health
                "pool_recycle": 3600,  # Recycle connections after 1 hour
                "echo": False,  # Set to True for SQL logging
            }
            
            # Create engine
            self.engine = create_async_engine(
                database_url,
                **pool_config
            )
            
            # Create session maker
            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Test connection
            try:
                async with self.engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                logger.info("✅ Database connection successful")
            except Exception as e:
                logger.error(f"❌ Database connection failed: {e}")
                raise
            
            self._stats["connections_created"] += 1
            logger.info(f"✅ Database pool initialized: size={settings.db.pool_size}, overflow={settings.db.max_overflow}")
    
    async def close(self):
        """Close all database connections"""
        async with self._connection_lock:
            if self.engine:
                await self.engine.dispose()
                self.engine = None
                self.async_session_maker = None
                self._stats["connections_closed"] += 1
                logger.info("✅ Database connections closed")
    
    @asynccontextmanager
    async def session(self):
        """
        Get database session with context manager
        Auto-commit on success, rollback on error
        """
        if not self.async_session_maker:
            await self.initialize()
        
        session = self.async_session_maker()
        try:
            yield session
            await session.commit()
            self._stats["queries_executed"] += 1
        except Exception as e:
            await session.rollback()
            self._stats["errors"] += 1
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            async with self.session() as session:
                result = await session.execute(text("SELECT 1"))
                if result.scalar() == 1:
                    return {
                        "status": "healthy",
                        "connections": self._stats["connections_created"],
                        "queries": self._stats["queries_executed"],
                        "errors": self._stats["errors"]
                    }
                return {"status": "unhealthy", "error": "Query failed"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self._stats.copy()


# ===== GLOBAL INSTANCE =====
db_manager = DatabaseManager()


# ===== CONVENIENCE FUNCTIONS =====

async def init_db():
    """Initialize database"""
    await db_manager.initialize()


async def close_db():
    """Close database connections"""
    await db_manager.close()


@asynccontextmanager
async def get_session():
    """Get database session"""
    async with db_manager.session() as session:
        yield session


async def execute_query(query, params=None):
    """Execute raw query and return results"""
    async with get_session() as session:
        result = await session.execute(text(query), params or {})
        return result.mappings().all()


async def execute_insert(query, params=None):
    """Execute insert and return lastrowid"""
    async with get_session() as session:
        result = await session.execute(text(query), params or {})
        await session.flush()
        return result.lastrowid


async def execute_update(query, params=None):
    """Execute update/delete and return rowcount"""
    async with get_session() as session:
        result = await session.execute(text(query), params or {})
        return result.rowcount


__all__ = [
    'db_manager', 'init_db', 'close_db', 'get_session',
    'execute_query', 'execute_insert', 'execute_update'
]
