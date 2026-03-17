#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ALERTING SYSTEM
=============================================================================
Notifikasi jika ada masalah atau anomali pada bot
"""

import asyncio
from enum import Enum
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta

from utils.logger import logger
from config import settings


class AlertLevel(Enum):
    """Level alert"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Alert:
    """Model untuk alert"""
    
    def __init__(self, 
                 title: str,
                 message: str,
                 level: AlertLevel = AlertLevel.INFO,
                 source: str = None,
                 metadata: Dict = None):
        
        self.id = f"alert_{datetime.now().timestamp()}"
        self.title = title
        self.message = message
        self.level = level
        self.source = source
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.acknowledged = False
        self.resolved = False
        self.resolved_at = None


class AlertManager:
    """Manager untuk alert dan notifikasi"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self.handlers: Dict[AlertLevel, List[Callable]] = {
            AlertLevel.INFO: [],
            AlertLevel.WARNING: [],
            AlertLevel.ERROR: [],
            AlertLevel.CRITICAL: []
        }
        
        # Thresholds
        self.thresholds = {
            'error_rate': 10,  # errors per hour
            'response_time': 5.0,  # seconds
            'cpu_usage': 80,  # percent
            'memory_usage': 80,  # percent
            'arousal_drop': 0.5,  # sudden drop
        }
        
        # Stats
        self.error_count = 0
        self.last_alert_time = None
    
    def register_handler(self, level: AlertLevel, handler: Callable):
        """Register handler for alert level"""
        self.handlers[level].append(handler)
    
    async def send_alert(self, alert: Alert):
        """Send alert to all registered handlers"""
        self.alerts.append(alert)
        self.last_alert_time = datetime.now()
        
        if alert.level in [AlertLevel.ERROR, AlertLevel.CRITICAL]:
            self.error_count += 1
        
        # Call handlers
        for handler in self.handlers[alert.level]:
            try:
                await handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")
        
        # Log alert
        log_func = logger.error if alert.level in [AlertLevel.ERROR, AlertLevel.CRITICAL] else logger.warning
        log_func(f"🔔 ALERT [{alert.level.value.upper()}]: {alert.title} - {alert.message}")
        
        # Send to Telegram admin
        await self._send_telegram(alert)
    
    async def _send_telegram(self, alert: Alert):
        """Send alert to Telegram admin"""
        if not settings.admin_id:
            return
        
        try:
            from telegram import Bot
            bot = Bot(token=settings.telegram_token)
            
            emoji = {
                AlertLevel.INFO: "ℹ️",
                AlertLevel.WARNING: "⚠️",
                AlertLevel.ERROR: "❌",
                AlertLevel.CRITICAL: "🚨"
            }.get(alert.level, "🔔")
            
            text = (
                f"{emoji} *Alert: {alert.title}*\n\n"
                f"{alert.message}\n\n"
                f"Level: {alert.level.value.upper()}\n"
                f"Time: {alert.created_at.strftime('%H:%M:%S')}"
            )
            
            await bot.send_message(
                chat_id=settings.admin_id,
                text=text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
    
    async def check_metrics(self, metrics: Dict):
        """Check metrics against thresholds and send alerts"""
        bot_metrics = metrics.get('bot', {})
        system_metrics = metrics.get('system', {})
        
        # Check error rate
        if bot_metrics.get('total_errors', 0) > self.thresholds['error_rate']:
            await self.send_alert(Alert(
                title="High Error Rate",
                message=f"Error rate: {bot_metrics['total_errors']}/hour",
                level=AlertLevel.ERROR,
                source="metrics_check",
                metadata={'errors': bot_metrics['total_errors']}
            ))
        
        # Check CPU usage
        if system_metrics.get('cpu_percent', 0) > self.thresholds['cpu_usage']:
            await self.send_alert(Alert(
                title="High CPU Usage",
                message=f"CPU: {system_metrics['cpu_percent']}%",
                level=AlertLevel.WARNING,
                source="system",
                metadata={'cpu': system_metrics['cpu_percent']}
            ))
        
        # Check memory usage
        if system_metrics.get('memory_percent', 0) > self.thresholds['memory_usage']:
            await self.send_alert(Alert(
                title="High Memory Usage",
                message=f"Memory: {system_metrics['memory_percent']}%",
                level=AlertLevel.WARNING,
                source="system",
                metadata={'memory': system_metrics['memory_percent']}
            ))
        
        # Check response time
        if bot_metrics.get('avg_response_time_ms', 0) > self.thresholds['response_time'] * 1000:
            await self.send_alert(Alert(
                title="Slow Response Time",
                message=f"Response time: {bot_metrics['avg_response_time_ms']}ms",
                level=AlertLevel.WARNING,
                source="bot",
                metadata={'response_time': bot_metrics['avg_response_time_ms']}
            ))
    
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return True
        return False
    
    def resolve_alert(self, alert_id: str):
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all unresolved alerts"""
        return [a for a in self.alerts if not a.resolved]
    
    def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        """Get alerts by level"""
        return [a for a in self.alerts if a.level == level]
    
    def get_recent_alerts(self, minutes: int = 60) -> List[Alert]:
        """Get alerts from last N minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [a for a in self.alerts if a.created_at > cutoff]


__all__ = ['AlertLevel', 'Alert', 'AlertManager']
