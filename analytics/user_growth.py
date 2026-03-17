#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
USER ANALYTICS
=============================================================================
Statistik penggunaan untuk single user
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class UserAnalytics:
    """Analytics untuk single user"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        
        # Session tracking
        self.sessions = []
        self.current_session_start = None
        self.total_time_online = timedelta()
        
        # Message stats
        self.messages_sent = 0
        self.messages_received = 0
        self.messages_by_hour = defaultdict(int)
        self.messages_by_day = defaultdict(int)
        
        # Command stats
        self.commands_used = defaultdict(int)
        self.favorite_commands = []
        
        # Role stats
        self.roles_used = defaultdict(int)
        self.current_role = None
    
    def start_session(self):
        """Start a new session"""
        self.current_session_start = datetime.now()
    
    def end_session(self):
        """End current session"""
        if self.current_session_start:
            session_duration = datetime.now() - self.current_session_start
            self.sessions.append({
                'start': self.current_session_start,
                'end': datetime.now(),
                'duration': session_duration
            })
            self.total_time_online += session_duration
            self.current_session_start = None
    
    def record_message(self, direction: str = 'sent'):
        """Record a message"""
        now = datetime.now()
        
        if direction == 'sent':
            self.messages_sent += 1
        else:
            self.messages_received += 1
        
        self.messages_by_hour[now.hour] += 1
        self.messages_by_day[now.weekday()] += 1
        self.last_seen = now
    
    def record_command(self, command: str):
        """Record command usage"""
        self.commands_used[command] += 1
        self.favorite_commands = [
            cmd for cmd, count in 
            sorted(self.commands_used.items(), key=lambda x: x[1], reverse=True)
        ][:5]
    
    def record_role(self, role: str):
        """Record role usage"""
        self.roles_used[role] += 1
        self.current_role = role
    
    def get_daily_stats(self) -> Dict:
        """Get daily statistics"""
        today = datetime.now().date()
        sessions_today = [
            s for s in self.sessions 
            if s['start'].date() == today
        ]
        
        return {
            'date': today.isoformat(),
            'messages_sent': self.messages_sent,
            'messages_received': self.messages_received,
            'sessions_count': len(sessions_today),
            'time_online': sum((s['duration'] for s in sessions_today), timedelta()),
            'commands_used': dict(self.commands_used),
            'current_role': self.current_role
        }
    
    def get_weekly_stats(self) -> Dict:
        """Get weekly statistics"""
        week_ago = datetime.now() - timedelta(days=7)
        recent_sessions = [s for s in self.sessions if s['start'] > week_ago]
        
        return {
            'period': '7 days',
            'total_messages': self.messages_sent + self.messages_received,
            'avg_messages_per_day': (self.messages_sent + self.messages_received) / 7,
            'total_sessions': len(recent_sessions),
            'total_time_online': sum((s['duration'] for s in recent_sessions), timedelta()),
            'peak_hour': max(self.messages_by_hour.items(), key=lambda x: x[1])[0] if self.messages_by_hour else None,
            'favorite_commands': self.favorite_commands[:3],
            'favorite_roles': [
                role for role, count in 
                sorted(self.roles_used.items(), key=lambda x: x[1], reverse=True)
            ][:3]
        }
    
    def get_summary(self) -> Dict:
        """Get complete user summary"""
        total_messages = self.messages_sent + self.messages_received
        avg_session_duration = self.total_time_online / len(self.sessions) if self.sessions else timedelta()
        
        return {
            'user_id': self.user_id,
            'first_seen': self.first_seen.isoformat(),
            'last_seen': self.last_seen.isoformat(),
            'total_messages': total_messages,
            'messages_sent': self.messages_sent,
            'messages_received': self.messages_received,
            'total_sessions': len(self.sessions),
            'total_time_online': str(self.total_time_online).split('.')[0],
            'avg_session_duration': str(avg_session_duration).split('.')[0],
            'messages_per_hour': dict(self.messages_by_hour),
            'favorite_commands': self.favorite_commands,
            'roles_used': dict(self.roles_used)
        }


__all__ = ['UserAnalytics']
