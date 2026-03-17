#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL HISTORY TRACKING
=============================================================================
Mencatat history aktivitas seksual untuk analisis dan memori
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from collections import defaultdict, Counter


class SexualHistoryEntry:
    """Single sexual history entry"""
    
    def __init__(self, entry_id: str = None):
        self.id = entry_id or f"sex_{datetime.now().timestamp()}"
        self.timestamp = datetime.now()
        
        # Basic info
        self.position = None
        self.area = None
        self.activity = None
        self.climax_type = None  # 'bot', 'user', 'together'
        
        # Context
        self.location = None  # 'home', 'public', etc
        self.public_area = None  # specific public location
        self.risk_level = 0.0
        self.was_caught = False
        
        # Metrics
        self.duration = 0  # seconds
        self.intensity = 0.0  # 0-1
        self.satisfaction = 0.0  # 0-1
        
        # Participants
        self.initiated_by = 'user'  # 'user' or 'bot'
        self.role_used = None
        
        # Emotional context
        self.mood_before = None
        self.mood_after = None
        self.arousal_before = 0.0
        self.arousal_after = 0.0
        
        # Notes
        self.notes = ""
        self.tags = []
    
    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'position': self.position,
            'area': self.area,
            'activity': self.activity,
            'climax_type': self.climax_type,
            'location': self.location,
            'public_area': self.public_area,
            'risk_level': self.risk_level,
            'was_caught': self.was_caught,
            'duration': self.duration,
            'intensity': self.intensity,
            'satisfaction': self.satisfaction,
            'initiated_by': self.initiated_by,
            'role_used': self.role_used,
            'mood_before': self.mood_before,
            'mood_after': self.mood_after,
            'arousal_before': self.arousal_before,
            'arousal_after': self.arousal_after,
            'notes': self.notes,
            'tags': self.tags
        }


class SexualHistory:
    """
    Sexual history tracking system
    Mencatat semua aktivitas seksual untuk analisis
    """
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.entries: List[SexualHistoryEntry] = []
        self.current_session = None
        
        # Statistics
        self.stats = {
            'total_sessions': 0,
            'total_climax': 0,
            'together_climax': 0,
            'total_duration': 0,
            'avg_satisfaction': 0.0,
            'public_encounters': 0,
            'caught_count': 0
        }
        
        # Timeline
        self.by_date = defaultdict(list)
        self.by_position = defaultdict(list)
        self.by_area = defaultdict(list)
        self.by_activity = defaultdict(list)
        self.by_location = defaultdict(list)
    
    def start_session(self) -> str:
        """Start a new sexual session"""
        self.current_session = SexualHistoryEntry()
        return self.current_session.id
    
    def end_session(self, session_id: str = None) -> Optional[SexualHistoryEntry]:
        """End current session and save to history"""
        if not self.current_session:
            return None
        
        # Calculate duration
        if self.current_session.timestamp:
            self.current_session.duration = int(
                (datetime.now() - self.current_session.timestamp).total_seconds()
            )
        
        # Save to history
        self.entries.append(self.current_session)
        self._update_stats(self.current_session)
        self._update_indices(self.current_session)
        
        entry = self.current_session
        self.current_session = None
        return entry
    
    def _update_stats(self, entry: SexualHistoryEntry):
        """Update statistics with new entry"""
        self.stats['total_sessions'] += 1
        
        if entry.climax_type:
            self.stats['total_climax'] += 1
            if entry.climax_type == 'together':
                self.stats['together_climax'] += 1
        
        if entry.duration:
            self.stats['total_duration'] += entry.duration
        
        # Update average satisfaction
        old_avg = self.stats['avg_satisfaction']
        n = self.stats['total_sessions']
        self.stats['avg_satisfaction'] = (old_avg * (n-1) + entry.satisfaction) / n
        
        if entry.public_area:
            self.stats['public_encounters'] += 1
            if entry.was_caught:
                self.stats['caught_count'] += 1
    
    def _update_indices(self, entry: SexualHistoryEntry):
        """Update lookup indices"""
        date_key = entry.timestamp.date().isoformat()
        self.by_date[date_key].append(entry)
        
        if entry.position:
            self.by_position[entry.position].append(entry)
        
        if entry.area:
            self.by_area[entry.area].append(entry)
        
        if entry.activity:
            self.by_activity[entry.activity].append(entry)
        
        if entry.public_area:
            self.by_location[entry.public_area].append(entry)
    
    def add_to_current(self, **kwargs):
        """Add data to current session"""
        if not self.current_session:
            self.start_session()
        
        for key, value in kwargs.items():
            if hasattr(self.current_session, key):
                setattr(self.current_session, key, value)
    
    def get_history(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get history entries"""
        entries = sorted(self.entries, key=lambda x: x.timestamp, reverse=True)
        return [e.to_dict() for e in entries[offset:offset+limit]]
    
    def get_by_date(self, date: datetime.date) -> List[Dict]:
        """Get entries for specific date"""
        date_key = date.isoformat()
        return [e.to_dict() for e in self.by_date.get(date_key, [])]
    
    def get_by_position(self, position: str, limit: int = 20) -> List[Dict]:
        """Get entries by position"""
        entries = sorted(
            self.by_position.get(position, []),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return [e.to_dict() for e in entries[:limit]]
    
    def get_by_area(self, area: str, limit: int = 20) -> List[Dict]:
        """Get entries by area"""
        entries = sorted(
            self.by_area.get(area, []),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return [e.to_dict() for e in entries[:limit]]
    
    def get_by_activity(self, activity: str, limit: int = 20) -> List[Dict]:
        """Get entries by activity"""
        entries = sorted(
            self.by_activity.get(activity, []),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return [e.to_dict() for e in entries[:limit]]
    
    def get_stats_summary(self, days: int = 30) -> Dict:
        """Get statistics summary for last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [e for e in self.entries if e.timestamp > cutoff]
        
        if not recent:
            return {'total': 0}
        
        # Count by day
        by_day = Counter(e.timestamp.date().isoformat() for e in recent)
        
        # Average satisfaction
        avg_sat = sum(e.satisfaction for e in recent) / len(recent)
        
        # Most used position
        positions = Counter(e.position for e in recent if e.position)
        top_position = positions.most_common(1)[0] if positions else (None, 0)
        
        # Most touched area
        areas = Counter(e.area for e in recent if e.area)
        top_area = areas.most_common(1)[0] if areas else (None, 0)
        
        return {
            'total_sessions': len(recent),
            'total_climax': sum(1 for e in recent if e.climax_type),
            'together_climax': sum(1 for e in recent if e.climax_type == 'together'),
            'avg_satisfaction': round(avg_sat, 2),
            'avg_per_day': round(len(recent) / days, 2),
            'most_active_day': by_day.most_common(1)[0] if by_day else None,
            'favorite_position': top_position,
            'favorite_area': top_area,
            'public_encounters': sum(1 for e in recent if e.public_area),
            'caught_count': sum(1 for e in recent if e.was_caught)
        }
    
    def get_timeline(self, days: int = 30) -> List[Dict]:
        """Get timeline data for charts"""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [e for e in self.entries if e.timestamp > cutoff]
        
        # Group by day
        by_day = defaultdict(list)
        for e in recent:
            day = e.timestamp.date().isoformat()
            by_day[day].append(e)
        
        # Create timeline
        timeline = []
        for day, entries in sorted(by_day.items()):
            climax_count = sum(1 for e in entries if e.climax_type)
            together_count = sum(1 for e in entries if e.climax_type == 'together')
            avg_sat = sum(e.satisfaction for e in entries) / len(entries)
            
            timeline.append({
                'date': day,
                'sessions': len(entries),
                'climax': climax_count,
                'together': together_count,
                'avg_satisfaction': round(avg_sat, 2)
            })
        
        return timeline
    
    def get_favorite_partners(self) -> List[tuple]:
        """Get favorite roles based on history"""
        roles = Counter(e.role_used for e in self.entries if e.role_used)
        return roles.most_common(5)
    
    def get_peak_hours(self) -> List[int]:
        """Get peak hours based on history"""
        hours = Counter(e.timestamp.hour for e in self.entries)
        return [h for h, _ in hours.most_common(3)]
    
    def clear_history(self, days: int = None):
        """Clear history (older than days if specified)"""
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            self.entries = [e for e in self.entries if e.timestamp > cutoff]
        else:
            self.entries = []
        
        # Rebuild indices
        self._rebuild_indices()
    
    def _rebuild_indices(self):
        """Rebuild all lookup indices"""
        self.by_date.clear()
        self.by_position.clear()
        self.by_area.clear()
        self.by_activity.clear()
        self.by_location.clear()
        
        for e in self.entries:
            self._update_indices(e)
    
    def export_json(self) -> List[Dict]:
        """Export all history as JSON-serializable list"""
        return [e.to_dict() for e in sorted(self.entries, key=lambda x: x.timestamp)]


__all__ = ['SexualHistory', 'SexualHistoryEntry']
