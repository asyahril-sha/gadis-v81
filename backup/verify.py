#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
BACKUP VERIFICATION
=============================================================================
Verifikasi integritas backup file
"""

import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from utils.logger import logger
from config import settings


class BackupVerifier:
    """
    Verifikasi integritas backup database
    - Cek checksum
    - Cek struktur database
    - Cek konsistensi data
    - Generate laporan verifikasi
    """
    
    def __init__(self):
        self.verification_history = []
    
    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def verify_file_integrity(self, backup_path: Path) -> Tuple[bool, str]:
        """Verify file integrity (size, header)"""
        if not backup_path.exists():
            return False, "File not found"
        
        # Check file size
        if backup_path.stat().st_size == 0:
            return False, "File is empty"
        
        # Check SQLite header
        try:
            with open(backup_path, 'rb') as f:
                header = f.read(16)
                if not header.startswith(b'SQLite format 3\x00'):
                    return False, "Invalid SQLite header"
        except Exception as e:
            return False, f"Cannot read file: {e}"
        
        return True, "File integrity OK"
    
    def verify_database_structure(self, backup_path: Path) -> Tuple[bool, List[str]]:
        """Verify database structure (tables, indexes)"""
        errors = []
        
        try:
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            
            # Check required tables
            required_tables = [
                'relationships',
                'conversations',
                'memories',
                'preferences',
                'sessions',
                'hts_fwb_relationships',
                'climax_history',
                'ranking',
                'sex_positions',
                'sensitive_areas',
                'public_locations'
            ]
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            for table in required_tables:
                if table not in existing_tables:
                    errors.append(f"Missing table: {table}")
            
            # Check if any data exists
            if existing_tables:
                for table in existing_tables[:3]:  # Check first few tables
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        logger.debug(f"Table {table}: {count} rows")
                    except:
                        pass
            
            conn.close()
            
        except Exception as e:
            errors.append(f"Database error: {e}")
        
        return len(errors) == 0, errors
    
    def verify_data_consistency(self, backup_path: Path) -> Tuple[bool, List[str]]:
        """Verify data consistency (foreign keys, referential integrity)"""
        errors = []
        
        try:
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            
            # Enable foreign keys and check
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("PRAGMA foreign_key_check")
            fk_violations = cursor.fetchall()
            
            if fk_violations:
                for violation in fk_violations:
                    errors.append(f"Foreign key violation: {violation}")
            
            conn.close()
            
        except Exception as e:
            errors.append(f"Consistency check error: {e}")
        
        return len(errors) == 0, errors
    
    def verify_backup(self, backup_path: Path, detailed: bool = False) -> Dict:
        """Complete backup verification"""
        logger.info(f"🔍 Verifying backup: {backup_path}")
        
        result = {
            'backup_path': str(backup_path),
            'timestamp': datetime.now().isoformat(),
            'file_size': backup_path.stat().st_size if backup_path.exists() else 0,
            'checksum': self.calculate_checksum(backup_path) if backup_path.exists() else None,
            'integrity': {'passed': False, 'errors': []},
            'structure': {'passed': False, 'errors': []},
            'consistency': {'passed': False, 'errors': []},
            'overall_passed': False
        }
        
        # File integrity
        integrity_passed, integrity_msg = self.verify_file_integrity(backup_path)
        result['integrity']['passed'] = integrity_passed
        if not integrity_passed:
            result['integrity']['errors'].append(integrity_msg)
        
        if detailed and integrity_passed:
            # Database structure
            structure_passed, structure_errors = self.verify_database_structure(backup_path)
            result['structure']['passed'] = structure_passed
            result['structure']['errors'] = structure_errors
            
            # Data consistency
            consistency_passed, consistency_errors = self.verify_data_consistency(backup_path)
            result['consistency']['passed'] = consistency_passed
            result['consistency']['errors'] = consistency_errors
            
            # Overall
            result['overall_passed'] = (
                integrity_passed and
                structure_passed and
                consistency_passed
            )
        else:
            result['overall_passed'] = integrity_passed
        
        # Log result
        if result['overall_passed']:
            logger.info(f"✅ Backup verification PASSED: {backup_path}")
        else:
            logger.warning(f"⚠️ Backup verification FAILED: {backup_path}")
        
        # Save to history
        self.verification_history.append({
            'timestamp': result['timestamp'],
            'backup': str(backup_path),
            'passed': result['overall_passed']
        })
        
        return result
    
    def verify_all_backups(self, backup_dir: Path = None) -> List[Dict]:
        """Verify all backups in directory"""
        if backup_dir is None:
            backup_dir = settings.backup_dir
        
        results = []
        for backup_file in backup_dir.glob("gadis_backup_*.db"):
            result = self.verify_backup(backup_file, detailed=False)
            results.append(result)
        
        return results
    
    def get_verification_report(self, backup_path: Path = None) -> str:
        """Get human-readable verification report"""
        if backup_path:
            result = self.verify_backup(backup_path, detailed=True)
            backups = [result]
        else:
            backups = self.verify_all_backups()
        
        report = []
        report.append("=" * 60)
        report.append("BACKUP VERIFICATION REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        passed = sum(1 for b in backups if b['overall_passed'])
        total = len(backups)
        
        report.append(f"Total Backups: {total}")
        report.append(f"Passed: {passed}")
        report.append(f"Failed: {total - passed}")
        report.append("")
        
        for backup in backups:
            status = "✅ PASSED" if backup['overall_passed'] else "❌ FAILED"
            report.append(f"{status} - {Path(backup['backup_path']).name}")
            report.append(f"  Size: {backup['file_size']:,} bytes")
            report.append(f"  Checksum: {backup['checksum'][:16]}...")
            
            if not backup['overall_passed']:
                if backup['integrity']['errors']:
                    report.append(f"  Integrity: {backup['integrity']['errors'][0]}")
                if backup['structure']['errors']:
                    report.append(f"  Structure: {backup['structure']['errors'][0]}")
                if backup['consistency']['errors']:
                    report.append(f"  Consistency: {backup['consistency']['errors'][0]}")
            
            report.append("")
        
        return "\n".join(report)
    
    def clean_corrupted_backups(self, backup_dir: Path = None) -> int:
        """Delete corrupted backups"""
        if backup_dir is None:
            backup_dir = settings.backup_dir
        
        deleted = 0
        for backup_file in backup_dir.glob("gadis_backup_*.db"):
            result = self.verify_backup(backup_file, detailed=False)
            if not result['overall_passed']:
                try:
                    backup_file.unlink()
                    metadata_file = backup_file.with_suffix('.json')
                    if metadata_file.exists():
                        metadata_file.unlink()
                    deleted += 1
                    logger.info(f"🗑️ Deleted corrupted backup: {backup_file.name}")
                except Exception as e:
                    logger.error(f"Failed to delete {backup_file}: {e}")
        
        if deleted > 0:
            logger.info(f"🧹 Cleaned up {deleted} corrupted backups")
        
        return deleted


# ===== SINGLETON =====
backup_verifier = BackupVerifier()


__all__ = ['backup_verifier', 'BackupVerifier']
