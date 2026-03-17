#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SQLITE CONNECTION (SANGAT SEDERHANA)
=============================================================================
Koneksi database SQLite tanpa settings.db.path
"""

import sqlite3
import aiosqlite
from pathlib import Path
from typing import Optional, Dict, List, Any
from contextlib import asynccontextmanager

from config import settings
from utils.logger import logger


class DatabaseManager:
    """Manajemen koneksi SQLite sederhana"""
    
    def __init__(self):
        # Langsung pakai string, bukan settings.db.path
        self.db_path = Path("gadis_v81.db")
        self.connection = None
        self._lock = None
        self._stats = {
            "queries": 0,
            "errors": 0
        }
    
    async def initialize(self):
        """Inisialisasi database"""
        import asyncio
        self._lock = asyncio.Lock()
        
        async with self._lock:
            try:
                # Buat koneksi
                self.connection = await aiosqlite.connect(self.db_path)
                self.connection.row_factory = sqlite3.Row
                
                # Enable foreign keys
                await self.connection.execute("PRAGMA foreign_keys = ON")
                
                # Buat tabel jika belum ada
                await self._create_tables()
                
                logger.info(f"✅ SQLite connected: {self.db_path}")
                
            except Exception as e:
                logger.error(f"❌ Database connection failed: {e}")
                raise
    
    async def _create_tables(self):
        """Buat tabel-tabel yang diperlukan"""
        
        # Tabel relationships
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                bot_name TEXT NOT NULL,
                bot_role TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                stage TEXT DEFAULT 'stranger',
                dominance TEXT DEFAULT 'normal',
                total_messages INTEGER DEFAULT 0,
                bot_climax INTEGER DEFAULT 0,
                user_climax INTEGER DEFAULT 0,
                together_climax INTEGER DEFAULT 0,
                hair_style TEXT,
                height INTEGER,
                weight INTEGER,
                breast_size TEXT,
                hijab BOOLEAN DEFAULT 0,
                most_sensitive_area TEXT,
                skin_color TEXT,
                face_shape TEXT,
                personality TEXT,
                current_clothing TEXT DEFAULT 'pakaian biasa',
                last_clothing_change TIMESTAMP,
                anger_level INTEGER DEFAULT 0,
                relationship_status TEXT DEFAULT 'pdkt',
                unique_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Tabel conversations
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                relationship_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                mood TEXT,
                arousal REAL,
                location TEXT,
                clothing TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (relationship_id) REFERENCES relationships(id) ON DELETE CASCADE
            )
        """)
        
        # Tabel preferences
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                user_id INTEGER PRIMARY KEY,
                romantic_score REAL DEFAULT 0,
                vulgar_score REAL DEFAULT 0,
                dominant_score REAL DEFAULT 0,
                submissive_score REAL DEFAULT 0,
                speed_score REAL DEFAULT 0,
                total_interactions INTEGER DEFAULT 0,
                favorite_areas TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.connection.commit()
        logger.info("✅ Database tables created")
    
    @asynccontextmanager
    async def cursor(self):
        """Dapatkan cursor database"""
        if not self.connection:
            await self.initialize()
        
        async with self._lock:
            try:
                yield self.connection
                self._stats["queries"] += 1
            except Exception as e:
                self._stats["errors"] += 1
                logger.error(f"Database error: {e}")
                raise
    
    async def execute(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute query and return results"""
        async with self.cursor() as conn:
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()
            
            # Convert to dict
            result = []
            for row in rows:
                result.append({key: row[key] for key in row.keys()})
            
            return result
    
    async def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute insert and return last row id"""
        async with self.cursor() as conn:
            cursor = await conn.execute(query, params)
            await conn.commit()
            return cursor.lastrowid
    
    async def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute update/delete and return rowcount"""
        async with self.cursor() as conn:
            cursor = await conn.execute(query, params)
            await conn.commit()
            return cursor.rowcount
    
    async def close(self):
        """Tutup koneksi database"""
        if self.connection:
            await self.connection.close()
            self.connection = None
            logger.info("✅ Database connection closed")
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        return self._stats.copy()


# ===== GLOBAL INSTANCE =====
db_manager = DatabaseManager()


# ===== CONVENIENCE FUNCTIONS =====
# PASTIKAN FUNGSI INI ADA!

async def init_db():
    """Initialize database"""
    await db_manager.initialize()
    return db_manager


async def close_db():
    """Close database connection"""
    await db_manager.close()


async def get_db():
    """Get database manager instance"""
    return db_manager


async def execute_query(query: str, params: tuple = ()) -> List[Dict]:
    """Execute query"""
    return await db_manager.execute(query, params)


async def execute_insert(query: str, params: tuple = ()) -> int:
    """Execute insert"""
    return await db_manager.execute_insert(query, params)


async def execute_update(query: str, params: tuple = ()) -> int:
    """Execute update"""
    return await db_manager.execute_update(query, params)


# ===== SYNCHRONOUS WRAPPERS (untuk main.py) =====
def init_db_sync():
    """Synchronous wrapper for init_db"""
    import asyncio
    return asyncio.run(init_db())


def close_db_sync():
    """Synchronous wrapper for close_db"""
    import asyncio
    return asyncio.run(close_db())


__all__ = [
    'db_manager',
    'init_db',
    'close_db',
    'get_db',
    'execute_query',
    'execute_insert',
    'execute_update',
    'init_db_sync',  # ← Tambahkan ini
    'close_db_sync'   # ← Tambahkan ini
]
