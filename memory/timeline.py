#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MEMORY TIMELINE
=============================================================================
Visualisasi dan query timeline memori
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from collections import defaultdict, Counter

from utils.logger import logger


class MemoryTimeline:
    """
    Timeline untuk visualisasi dan query memori
    - Event ordering
    - Timeline visualization data
    - Timeline queries
    - Pattern analysis over time
    """
    
    def __init__(self, episodic_memory):
        self.episodic = episodic_memory
        self.timeline_cache = {}
        self.last_cache_update = None
        
        logger.info("📅 Memory Timeline initialized")
    
    def get_events_by_date(self, date: datetime) -> List[Dict]:
        """Get all events on specific date"""
        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)
        
        events = []
        for mem in self.episodic.memories:
            if start <= mem['timestamp'] < end:
                events.append(mem.copy())
        
        return sorted(events, key=lambda x: x['timestamp'])
    
    def get_events_by_week(self, year: int, week: int) -> List[Dict]:
        """Get all events in specific week"""
        first_day = datetime.fromisocalendar(year, week, 1)
        last_day = first_day + timedelta(days=7)
        
        events = []
        for mem in self.episodic.memories:
            if first_day <= mem['timestamp'] < last_day:
                events.append(mem.copy())
        
        return sorted(events, key=lambda x: x['timestamp'])
    
    def get_events_by_month(self, year: int, month: int) -> List[Dict]:
        """Get all events in specific month"""
        events = []
        for mem in self.episodic.memories:
            if mem['timestamp'].year == year and mem['timestamp'].month == month:
                events.append(mem.copy())
        
        return sorted(events, key=lambda x: x['timestamp'])
    
    def get_timeline_summary(self, days: int = 30) -> Dict:
        """Get summary of timeline for last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        
        # Filter recent memories
        recent = [m for m in self.episodic.memories if m['timestamp'] > cutoff]
        
        # Group by day
        by_day = defaultdict(list)
        for mem in recent:
            day = mem['timestamp'].date()
            by_day[day].append(mem)
        
        # Calculate stats per day
        daily_stats = {}
        for day, mems in sorted(by_day.items()):
            daily_stats[day.isoformat()] = {
                'total': len(mems),
                'important': sum(1 for m in mems if m['importance'] > 0.7),
                'emotions': Counter(m['emotion'] for m in mems),
                'avg_importance': sum(m['importance'] for m in mems) / len(mems)
            }
        
        # Overall stats
        total_events = len(recent)
        total_important = sum(1 for m in recent if m['importance'] > 0.7)
        
        # Emotional progression
        emotional_progression = []
        for mem in sorted(recent, key=lambda x: x['timestamp']):
            emotional_progression.append({
                'date': mem['timestamp'].isoformat(),
                'emotion': mem['emotion'],
                'importance': mem['importance']
            })
        
        return {
            'period_days': days,
            'total_events': total_events,
            'total_important': total_important,
            'unique_days': len(by_day),
            'daily_stats': daily_stats,
            'emotional_progression': emotional_progression[-50:],  # Last 50 for chart
            'peak_day': max(daily_stats.items(), key=lambda x: x[1]['total'])[0] if daily_stats else None
        }
    
    def get_emotional_timeline(self, days: int = 30) -> List[Dict]:
        """Get emotional changes over time"""
        cutoff = datetime.now() - timedelta(days=days)
        
        # Get recent memories with emotions
        recent = [
            m for m in self.episodic.memories 
            if m['timestamp'] > cutoff and m.get('emotion')
        ]
        
        # Group by hour for smooth timeline
        by_hour = defaultdict(list)
        for mem in recent:
            hour_key = mem['timestamp'].strftime('%Y-%m-%d %H:00')
            by_hour[hour_key].append(mem)
        
        timeline = []
        for hour, mems in sorted(by_hour.items()):
            # Get dominant emotion for this hour
            emotions = Counter(m['emotion'] for m in mems)
            dominant = emotions.most_common(1)[0][0] if emotions else 'neutral'
            
            timeline.append({
                'timestamp': hour,
                'dominant_emotion': dominant,
                'emotion_distribution': dict(emotions),
                'intensity': sum(m['importance'] for m in mems) / len(mems)
            })
        
        return timeline
    
    def get_activity_timeline(self, days: int = 30) -> Dict:
        """Get activity patterns over time"""
        cutoff = datetime.now() - timedelta(days=days)
        
        recent = [m for m in self.episodic.memories if m['timestamp'] > cutoff]
        
        # Activity by hour of day
        by_hour = Counter()
        for mem in recent:
            by_hour[mem['timestamp'].hour] += 1
        
        # Activity by day of week
        by_weekday = Counter()
        for mem in recent:
            by_weekday[mem['timestamp'].weekday()] += 1
        
        # Peak activity times
        peak_hours = [hour for hour, count in by_hour.most_common(3)]
        peak_days = [day for day, count in by_weekday.most_common(3)]
        
        return {
            'by_hour': dict(by_hour),
            'by_weekday': dict(by_weekday),
            'peak_hours': peak_hours,
            'peak_days': peak_days,
            'total_activities': len(recent),
            'avg_per_day': len(recent) / days
        }
    
    def get_milestone_timeline(self) -> List[Dict]:
        """Get timeline of important milestones"""
        milestones = []
        
        for mem in self.episodic.memories:
            if mem['importance'] > 0.8 or 'first' in mem.get('tags', []):
                milestones.append({
                    'date': mem['timestamp'].isoformat(),
                    'content': mem['content'][:100],
                    'importance': mem['importance'],
                    'emotion': mem.get('emotion', 'neutral'),
                    'tags': mem.get('tags', [])
                })
        
        return sorted(milestones, key=lambda x: x['date'])
    
    def get_timeline_for_chart(self, days: int = 30) -> Dict:
        """Get timeline data formatted for charts"""
        cutoff = datetime.now() - timedelta(days=days)
        
        # Generate daily data
        dates = []
        events_count = []
        importance_avg = []
        
        current = cutoff
        while current <= datetime.now():
            day_events = self.get_events_by_date(current)
            dates.append(current.strftime('%Y-%m-%d'))
            events_count.append(len(day_events))
            
            if day_events:
                avg_imp = sum(e['importance'] for e in day_events) / len(day_events)
                importance_avg.append(avg_imp)
            else:
                importance_avg.append(0)
            
            current += timedelta(days=1)
        
        return {
            'labels': dates,
            'datasets': {
                'events': events_count,
                'importance': importance_avg
            }
        }
    
    def search_timeline(self, query: str, days: int = 30) -> List[Dict]:
        """Search timeline for specific events"""
        cutoff = datetime.now() - timedelta(days=days)
        query_lower = query.lower()
        
        results = []
        for mem in self.episodic.memories:
            if mem['timestamp'] < cutoff:
                continue
            
            if query_lower in mem['content'].lower():
                results.append({
                    'date': mem['timestamp'].isoformat(),
                    'content': mem['content'],
                    'importance': mem['importance'],
                    'emotion': mem.get('emotion', 'neutral'),
                    'context': mem.get('context', {})
                })
        
        return sorted(results, key=lambda x: x['date'], reverse=True)
    
    def get_timeline_stats(self) -> Dict:
        """Get comprehensive timeline statistics"""
        all_memories = list(self.episodic.memories)
        
        if not all_memories:
            return {'total_memories': 0}
        
        first_date = min(m['timestamp'] for m in all_memories)
        last_date = max(m['timestamp'] for m in all_memories)
        total_days = (last_date - first_date).days + 1
        
        # Memories per day
        memories_per_day = len(all_memories) / total_days if total_days > 0 else 0
        
        # Most active day
        by_day = Counter(m['timestamp'].date() for m in all_memories)
        most_active_day = by_day.most_common(1)[0] if by_day else None
        
        # Emotional diversity
        emotions = Counter(m.get('emotion', 'neutral') for m in all_memories)
        
        return {
            'total_memories': len(all_memories),
            'first_memory': first_date.isoformat(),
            'last_memory': last_date.isoformat(),
            'total_days': total_days,
            'memories_per_day': round(memories_per_day, 2),
            'most_active_day': {
                'date': most_active_day[0].isoformat() if most_active_day else None,
                'count': most_active_day[1] if most_active_day else 0
            },
            'emotional_diversity': len(emotions),
            'top_emotions': emotions.most_common(5)
        }


__all__ = ['MemoryTimeline']
