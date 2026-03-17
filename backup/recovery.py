#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
RECOVERY SYSTEM
=============================================================================
Restore database dari backup dan recovery procedures
"""

import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

from config import settings
from utils.logger import logger
from backup.automated import backup_manager


class RecoveryManager:
    """
    Manajemen recovery database dari backup
    - Restore ke latest backup
    - Restore ke backup specific
    - Verify sebelum restore
    - Rollback jika gagal
    """
    
    def __init__(self):
        self.db_path = Path(settings.db_path)
        self.backup_dir = settings.backup_dir
        self.recovery_history = []
    
    def list_available_backups(self) -> List[Dict]:
        """List semua backup yang tersedia"""
        return backup_manager.list_all_backups()
    
    def verify_backup(self, backup_path: Path) -> bool:
        """Verifikasi integritas backup file"""
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        # Check file size
        if backup_path.stat().st_size == 0:
            logger.error(f"Backup file is empty: {backup_path}")
            return False
        
        # Try to read SQLite header
        try:
            with open(backup_path, 'rb') as f:
                header = f.read(16)
                if not header.startswith(b'SQLite format 3\x00'):
                    logger.error(f"Invalid SQLite file: {backup_path}")
                    return False
        except Exception as e:
            logger.error(f"Failed to read backup file: {e}")
            return False
        
        return True
    
    async def restore_latest(self, create_backup_first: bool = True) -> bool:
        """Restore from latest backup"""
        latest = backup_manager.get_latest_backup()
        if not latest:
            logger.error("No backup found")
            return False
        
        return await self.restore_from_file(latest, create_backup_first)
    
    async def restore_from_file(self, backup_path: Path, create_backup_first: bool = True) -> bool:
        """Restore database from backup file"""
        backup_path = Path(backup_path)
        
        # Verify backup
        if not self.verify_backup(backup_path):
            return False
        
        # Create backup of current database before restore
        if create_backup_first and self.db_path.exists():
            pre_restore_backup = self.backup_dir / f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            try:
                shutil.copy2(self.db_path, pre_restore_backup)
                logger.info(f"✅ Created pre-restore backup: {pre_restore_backup}")
            except Exception as e:
                logger.error(f"Failed to create pre-restore backup: {e}")
                return False
        
        try:
            # Stop auto backup during restore
            await backup_manager.stop_auto_backup()
            
            # Close current database connections
            from database.connection import close_db
            await close_db()
            
            # Perform restore
            shutil.copy2(backup_path, self.db_path)
            
            # Verify restored database
            from database.connection import init_db
            await init_db()
            
            # Record recovery
            self.recovery_history.append({
                'timestamp': datetime.now().isoformat(),
                'backup': str(backup_path),
                'status': 'success'
            })
            
            logger.info(f"✅ Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            
            # Try to rollback
            if 'pre_restore_backup' in locals() and pre_restore_backup.exists():
                try:
                    shutil.copy2(pre_restore_backup, self.db_path)
                    logger.info("✅ Rolled back to pre-restore state")
                except Exception as rollback_error:
                    logger.error(f"Rollback failed: {rollback_error}")
            
            self.recovery_history.append({
                'timestamp': datetime.now().isoformat(),
                'backup': str(backup_path),
                'status': 'failed',
                'error': str(e)
            })
            
            return False
            
        finally:
            # Restart auto backup
            await backup_manager.start_auto_backup()
    
    async def restore_to_point_in_time(self, timestamp: str) -> bool:
        """Restore to specific point in time based on backup timestamp"""
        backups = self.list_available_backups()
        
        # Find backup closest to timestamp
        target_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        closest_backup = None
        closest_diff = None
        
        for backup in backups:
            backup_time = datetime.strptime(backup['timestamp'], "%Y%m%d_%H%M%S")
            diff = abs((backup_time - target_time).total_seconds())
            
            if closest_diff is None or diff < closest_diff:
                closest_diff = diff
                closest_backup = backup
        
        if not closest_backup:
            logger.error(f"No backup found near {timestamp}")
            return False
        
        backup_path = self.backup_dir / closest_backup['filename']
        return await self.restore_from_file(backup_path)
    
    def get_recovery_history(self) -> List[Dict]:
        """Get recovery operation history"""
        return self.recovery_history
    
    def get_recovery_instructions(self) -> str:
        """Get manual recovery instructions"""
        return """
🔧 **INSTRUKSI RECOVERY MANUAL**

1. Stop bot
2. Backup database saat ini (jika perlu)
3. Copy file backup ke lokasi database
4. Start bot kembali

Command:
   cp backups/gadis_backup_20250101_120000.db gadis_v81.db
   python main.py

Atau gunakan command:
   /recover latest
   /recover <timestamp>
"""


# ===== SINGLETON =====
recovery_manager = RecoveryManager()


__all__ = ['recovery_manager', 'RecoveryManager']
