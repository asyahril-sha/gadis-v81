#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
AUTOMATED BACKUP SYSTEM
=============================================================================
Backup database otomatis ke local disk atau cloud storage
"""

import os
import shutil
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import json

from config import settings
from utils.logger import logger


class AutoBackup:
    """
    Sistem backup otomatis untuk database
    - Backup periodik (setiap jam)
    - Rotasi backup (hapus yang lama)
    - Backup ke local disk
    - Opsional backup ke S3
    """
    
    def __init__(self):
        self.backup_dir = settings.backup_dir
        self.backup_dir.mkdir(exist_ok=True)
        
        self.db_path = Path(settings.db_path)
        self.backup_interval = settings.backup_interval  # detik
        self.retention_days = settings.backup_retention_days
        
        self.backup_task = None
        self.is_running = False
        self.last_backup = None
        self.backup_history = []
        
        logger.info(f"💾 AutoBackup initialized: interval={self.backup_interval}s, retention={self.retention_days} days")
    
    async def start(self):
        """Start automatic backup"""
        self.is_running = True
        self.backup_task = asyncio.create_task(self._backup_loop())
        logger.info("🔄 Automatic backup started")
    
    async def stop(self):
        """Stop automatic backup"""
        self.is_running = False
        if self.backup_task:
            self.backup_task.cancel()
            try:
                await self.backup_task
            except asyncio.CancelledError:
                pass
        logger.info("🔄 Automatic backup stopped")
    
    async def _backup_loop(self):
        """Main backup loop"""
        while self.is_running:
            try:
                await self.create_backup()
                await self._cleanup_old_backups()
                await asyncio.sleep(self.backup_interval)
            except Exception as e:
                logger.error(f"Backup error: {e}")
                await asyncio.sleep(60)  # Tunggu 1 menit lalu coba lagi
    
    async def create_backup(self, manual: bool = False) -> Optional[Path]:
        """Create a new backup"""
        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            return None
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"gadis_backup_{timestamp}.db"
        backup_path = self.backup_dir / backup_filename
        
        # Create backup
        try:
            shutil.copy2(self.db_path, backup_path)
            
            # Create metadata file
            metadata = {
                'timestamp': timestamp,
                'filename': backup_filename,
                'size_bytes': backup_path.stat().st_size,
                'manual': manual,
                'database': str(self.db_path)
            }
            
            metadata_path = backup_path.with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.last_backup = datetime.now()
            self.backup_history.append({
                'timestamp': timestamp,
                'path': str(backup_path),
                'size': backup_path.stat().st_size,
                'manual': manual
            })
            
            # Keep only last 100 in history
            if len(self.backup_history) > 100:
                self.backup_history = self.backup_history[-100:]
            
            logger.info(f"✅ Backup created: {backup_filename} ({backup_path.stat().st_size} bytes)")
            
            # Upload to S3 jika dikonfigurasi
            if settings.backup_s3_bucket:
                await self._upload_to_s3(backup_path)
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    async def _cleanup_old_backups(self):
        """Delete backups older than retention days"""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        deleted = 0
        
        for backup_file in self.backup_dir.glob("gadis_backup_*.db"):
            # Check file age
            file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            if file_time < cutoff:
                try:
                    # Delete .db and .json
                    backup_file.unlink()
                    metadata_file = backup_file.with_suffix('.json')
                    if metadata_file.exists():
                        metadata_file.unlink()
                    deleted += 1
                except Exception as e:
                    logger.error(f"Failed to delete old backup {backup_file}: {e}")
        
        if deleted > 0:
            logger.info(f"🧹 Cleaned up {deleted} old backups")
    
    async def _upload_to_s3(self, backup_path: Path):
        """Upload backup to S3 (placeholder)"""
        logger.info(f"☁️ Uploading {backup_path.name} to S3 bucket {settings.backup_s3_bucket}")
        # TODO: Implement S3 upload jika diperlukan
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob("gadis_backup_*.db"), reverse=True):
            metadata_file = backup_file.with_suffix('.json')
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                backups.append(metadata)
            else:
                # Create basic metadata
                backups.append({
                    'timestamp': backup_file.stem.replace('gadis_backup_', ''),
                    'filename': backup_file.name,
                    'size_bytes': backup_file.stat().st_size,
                    'manual': False
                })
        
        return backups
    
    def get_latest_backup(self) -> Optional[Path]:
        """Get latest backup file"""
        backups = sorted(self.backup_dir.glob("gadis_backup_*.db"), reverse=True)
        return backups[0] if backups else None
    
    def get_stats(self) -> Dict:
        """Get backup statistics"""
        return {
            'last_backup': self.last_backup.isoformat() if self.last_backup else None,
            'total_backups': len(self.list_backups()),
            'backup_dir': str(self.backup_dir),
            'backup_interval': self.backup_interval,
            'retention_days': self.retention_days,
            'history': self.backup_history[-10:]  # Last 10 backups
        }


class BackupManager:
    """Manager untuk semua operasi backup"""
    
    def __init__(self):
        self.auto_backup = AutoBackup()
        self.backup_in_progress = False
    
    async def start_auto_backup(self):
        """Start automatic backup"""
        await self.auto_backup.start()
    
    async def stop_auto_backup(self):
        """Stop automatic backup"""
        await self.auto_backup.stop()
    
    async def create_manual_backup(self) -> Optional[Path]:
        """Create manual backup"""
        self.backup_in_progress = True
        try:
            return await self.auto_backup.create_backup(manual=True)
        finally:
            self.backup_in_progress = False
    
    def list_all_backups(self) -> List[Dict]:
        """List all backups"""
        return self.auto_backup.list_backups()
    
    def get_latest_backup(self) -> Optional[Path]:
        """Get latest backup"""
        return self.auto_backup.get_latest_backup()


# ===== SINGLETON =====
backup_manager = BackupManager()


__all__ = ['AutoBackup', 'backup_manager', 'BackupManager']
