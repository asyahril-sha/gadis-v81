#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
PROMETHEUS METRICS
=============================================================================
Koleksi metrik bot untuk monitoring dengan Prometheus
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

# Coba import prometheus
try:
    from prometheus_client import Counter, Gauge, Histogram, generate_latest, REGISTRY
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

from utils.logger import logger


class BotMetrics:
    """Koleksi metrik bot"""
    
    def __init__(self):
        self.start_time = time.time()
        
        # Counters
        self.message_count = 0
        self.command_count = 0
        self.climax_count = 0
        self.together_climax_count = 0
        self.error_count = 0
        
        # Gauges
        self.active_sessions = 0
        self.current_arousal = 0.0
        self.current_level = 1
        self.memory_usage = 0
        self.cpu_usage = 0
        
        # Histograms
        self.response_times = []
        self.session_durations = []
        
        # Per-role stats
        self.role_stats = defaultdict(lambda: {
            'messages': 0,
            'climax': 0,
            'time_spent': 0
        })
        
        # Per-position stats (V81)
        self.position_stats = defaultdict(lambda: {
            'times_used': 0,
            'climax_count': 0,
            'success_rate': 0.0
        })
        
        # Prometheus metrics
        if PROMETHEUS_AVAILABLE:
            self._init_prometheus()
    
    def _init_prometheus(self):
        """Initialize Prometheus metrics"""
        try:
            self.prom_message_counter = Counter(
                'bot_messages_total',
                'Total messages processed',
                ['role']
            )
            self.prom_climax_counter = Counter(
                'bot_climax_total',
                'Total climaxes',
                ['type']
            )
            self.prom_active_users = Gauge(
                'bot_active_users',
                'Number of active users'
            )
            self.prom_response_time = Histogram(
                'bot_response_time_seconds',
                'Response time in seconds'
            )
            self.prom_error_counter = Counter(
                'bot_errors_total',
                'Total errors',
                ['type']
            )
            logger.info("✅ Prometheus metrics initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Prometheus: {e}")
    
    def record_message(self, role: str = None):
        """Record a message"""
        self.message_count += 1
        
        if role:
            self.role_stats[role]['messages'] += 1
        
        if PROMETHEUS_AVAILABLE and hasattr(self, 'prom_message_counter'):
            self.prom_message_counter.labels(role=role or 'unknown').inc()
    
    def record_command(self):
        """Record a command usage"""
        self.command_count += 1
    
    def record_climax(self, climax_type: str = 'bot', role: str = None, position: str = None):
        """Record a climax"""
        self.climax_count += 1
        
        if climax_type == 'together':
            self.together_climax_count += 1
        
        if role:
            self.role_stats[role]['climax'] += 1
        
        if position:
            self.position_stats[position]['times_used'] += 1
            self.position_stats[position]['climax_count'] += 1
        
        if PROMETHEUS_AVAILABLE and hasattr(self, 'prom_climax_counter'):
            self.prom_climax_counter.labels(type=climax_type).inc()
    
    def record_response_time(self, response_time: float):
        """Record response time"""
        self.response_times.append(response_time)
        
        # Keep only last 1000
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        if PROMETHEUS_AVAILABLE and hasattr(self, 'prom_response_time'):
            self.prom_response_time.observe(response_time)
    
    def record_error(self, error_type: str = 'unknown'):
        """Record an error"""
        self.error_count += 1
        
        if PROMETHEUS_AVAILABLE and hasattr(self, 'prom_error_counter'):
            self.prom_error_counter.labels(type=error_type).inc()
    
    def update_session_count(self, count: int):
        """Update active session count"""
        self.active_sessions = count
        
        if PROMETHEUS_AVAILABLE and hasattr(self, 'prom_active_users'):
            self.prom_active_users.set(count)
    
    def update_arousal(self, arousal: float):
        """Update current arousal"""
        self.current_arousal = arousal
    
    def update_level(self, level: int):
        """Update current level"""
        self.current_level = level
    
    def get_uptime(self) -> float:
        """Get uptime in seconds"""
        return time.time() - self.start_time
    
    def get_average_response_time(self) -> float:
        """Get average response time"""
        if not self.response_times:
            return 0
        return sum(self.response_times) / len(self.response_times)
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of all metrics"""
        return {
            'uptime_seconds': self.get_uptime(),
            'uptime_hours': self.get_uptime() / 3600,
            'total_messages': self.message_count,
            'total_commands': self.command_count,
            'total_climax': self.climax_count,
            'together_climax': self.together_climax_count,
            'total_errors': self.error_count,
            'active_sessions': self.active_sessions,
            'current_arousal': round(self.current_arousal, 2),
            'current_level': self.current_level,
            'avg_response_time_ms': round(self.get_average_response_time() * 1000, 2),
            'role_stats': dict(self.role_stats),
            'position_stats': dict(self.position_stats)
        }
    
    def get_prometheus_metrics(self) -> Optional[bytes]:
        """Get Prometheus metrics in text format"""
        if PROMETHEUS_AVAILABLE:
            return generate_latest(REGISTRY)
        return None


class MetricsCollector:
    """Collector untuk metrik bot"""
    
    def __init__(self):
        self.metrics = BotMetrics()
        self.collection_interval = 60  # seconds
        self.last_collection = datetime.now()
        self.metrics_history = []
    
    def collect(self) -> Dict:
        """Collect current metrics"""
        now = datetime.now()
        
        if (now - self.last_collection).total_seconds() < self.collection_interval:
            return self.metrics.get_metrics_summary()
        
        summary = self.metrics.get_metrics_summary()
        summary['timestamp'] = now.isoformat()
        
        self.metrics_history.append(summary)
        self.last_collection = now
        
        # Keep last 1000 collections
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
        
        return summary
    
    def get_history(self, hours: int = 24) -> List[Dict]:
        """Get metrics history for last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [m for m in self.metrics_history 
                if datetime.fromisoformat(m['timestamp']) > cutoff]
    
    def get_daily_report(self) -> Dict:
        """Get daily report"""
        today = datetime.now().date()
        today_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m['timestamp']).date() == today
        ]
        
        if not today_metrics:
            return {}
        
        latest = today_metrics[-1]
        first = today_metrics[0]
        
        return {
            'date': today.isoformat(),
            'total_messages': latest['total_messages'] - first['total_messages'],
            'total_climax': latest['total_climax'] - first['total_climax'],
            'total_errors': latest['total_errors'] - first['total_errors'],
            'peak_arousal': max(m['current_arousal'] for m in today_metrics),
            'avg_response_time': sum(m['avg_response_time_ms'] for m in today_metrics) / len(today_metrics)
        }


__all__ = ['BotMetrics', 'MetricsCollector']
