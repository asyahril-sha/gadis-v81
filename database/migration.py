#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
DATABASE MIGRATION WITH ALEMBIC
=============================================================================
Schema versioning and migrations untuk PostgreSQL
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from database.models import Base
from utils.logger import logger


class MigrationManager:
    """
    Manajemen migrasi database dengan Alembic
    - Version tracking
    - Auto-migration on startup
    - Seed data
    - Rollback support
    """
    
    def __init__(self):
        self.sync_engine = create_engine(
            settings.db.url.replace("+asyncpg", ""),  # Sync URL for Alembic
            pool_pre_ping=True
        )
        self.migrations_table = "alembic_version"
    
    async def create_tables(self):
        """Create all tables (for initial setup)"""
        try:
            # Use sync engine in thread pool
            def _create():
                Base.metadata.create_all(self.sync_engine)
                logger.info("✅ All tables created")
            
            await asyncio.to_thread(_create)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            return False
    
    async def drop_tables(self):
        """Drop all tables (dangerous!)"""
        confirm = input("⚠️ This will DELETE ALL DATA! Type 'yes' to confirm: ")
        if confirm != "yes":
            logger.info("Drop tables cancelled")
            return False
        
        def _drop():
            Base.metadata.drop_all(self.sync_engine)
            logger.info("✅ All tables dropped")
        
        await asyncio.to_thread(_drop)
        return True
    
    async def get_current_version(self) -> Optional[str]:
        """Get current database version"""
        def _get():
            with self.sync_engine.connect() as conn:
                result = conn.execute(
                    text("SELECT version_num FROM alembic_version")
                )
                row = result.fetchone()
                return row[0] if row else None
        
        return await asyncio.to_thread(_get)
    
    async def init_alembic(self):
        """Initialize Alembic"""
        alembic_ini = Path("alembic.ini")
        if not alembic_ini.exists():
            # Create alembic.ini
            ini_content = f"""
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = {settings.db.url.replace("+asyncpg", "")}

[post_write_hooks]
hooks = black
black.type = console
black.executable = black
black.options = -l 88

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
            alembic_ini.write_text(ini_content)
            
            # Create alembic directory
            alembic_dir = Path("alembic")
            alembic_dir.mkdir(exist_ok=True)
            (alembic_dir / "versions").mkdir(exist_ok=True)
            
            # Create env.py
            env_py = alembic_dir / "env.py"
            env_py.write_text("""
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.models import Base
from config import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""")
            
            logger.info("✅ Alembic initialized")
            return True
        return False


# ===== CONVENIENCE FUNCTIONS =====

async def run_migrations():
    """Run migrations on startup"""
    manager = MigrationManager()
    
    # Check if tables exist
    def _check_tables():
        with manager.sync_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'relationships'
                )
            """))
            return result.scalar()
    
    tables_exist = await asyncio.to_thread(_check_tables)
    
    if not tables_exist:
        logger.info("📊 Creating database tables...")
        await manager.create_tables()
        await manager.init_alembic()
        logger.info("✅ Database initialized")
    else:
        logger.info("✅ Database already exists, skipping creation")
    
    return True


__all__ = ['MigrationManager', 'run_migrations']
