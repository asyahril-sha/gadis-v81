#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
DATA COLLECTOR
=============================================================================
Mengumpulkan data dari berbagai komponen bot secara periodik
"""

import asyncio
import psutil
from datetime import datetime
from typing import Dict, Optional

from monitoring.metrics import MetricsCollector
from utils.logger import logger
from config import settings


class DataCollector:
    """Collector untuk data dari berbagai sumber"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.collection_task = None
        self.is_running = False
        
        # System metrics
        self.system_metrics = {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_usage': 0,
            'network_io': {'sent': 0, 'recv': 0}
        }
    
    async def start_collection(self, interval: int = 60):
        """Start periodic data collection"""
        self.is_running = True
        self.collection_task = asyncio.create_task(self._collection_loop(interval))
        logger.info(f"📊 Data collection started (interval: {interval}s)")
    
    async def stop_collection(self):
        """Stop data collection"""
        self.is_running = False
        if self.collection_task:
            self.collection_task.cancel()
            try:
                await self.collection_task
            except asyncio.CancelledError:
                pass
        logger.info("📊 Data collection stopped")
    
    async def _collection_loop(self, interval: int):
        """Main collection loop"""
        while self.is_running:
            try:
                await self.collect_all()
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Collection error: {e}")
                await asyncio.sleep(interval)
    
    async def collect_all(self) -> Dict:
        """Collect all metrics"""
        # Collect bot metrics
        bot_metrics = self.metrics.collect()
        
        # Collect system metrics
        system_metrics = await self._collect_system_metrics()
        
        # Collect database metrics
        db_metrics = await self._collect_database_metrics()
        
        # Collect cache metrics
        cache_metrics = await self._collect_cache_metrics()
        
        combined = {
            'timestamp': datetime.now().isoformat(),
            'bot': bot_metrics,
            'system': system_metrics,
            'database': db_metrics,
            'cache': cache_metrics
        }
        
        return combined
    
    async def _collect_system_metrics(self) -> Dict:
        """Collect system metrics"""
        try:
            import psutil
            self.system_metrics = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_used_mb': psutil.virtual_memory().used / (1024 * 1024),
                'disk_usage': psutil.disk_usage('/').percent,
                'network_io': {
                    'sent_mb': psutil.net_io_counters().bytes_sent / (1024 * 1024),
                    'recv_mb': psutil.net_io_counters().bytes_recv / (1024 * 1024)
                }
            }
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
        
        return self.system_metrics
    
    async def _collect_database_metrics(self) -> Dict:
        """Collect database metrics"""
        # TODO: Implement database metrics collection
        return {
            'connection_pool_size': 0,
            'active_connections': 0,
            'total_queries': 0,
            'slow_queries': 0
        }
    
    async def _collect_cache_metrics(self) -> Dict:
        """Collect cache metrics"""
        # TODO: Implement cache metrics collection
        return {
            'hit_rate': 0,
            'miss_rate': 0,
            'memory_used': 0
        }
    
    def get_latest(self) -> Dict:
        """Get latest collected metrics"""
        return self.metrics.metrics.get_metrics_summary()
    
    def get_system_metrics(self) -> Dict:
        """Get latest system metrics"""
        return self.system_metrics


__all__ = ['DataCollector']
