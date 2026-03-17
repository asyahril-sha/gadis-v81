#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
PEAK HOURS ANALYZER
=============================================================================
Analisis waktu-waktu aktif penggunaan bot
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class PeakHoursAnalyzer:
    """Analisis peak hours penggunaan bot"""
    
    def __init__(self):
        self.activity_log = []
        self.hourly_stats = defaultdict(lambda: {
            'messages': 0,
            'climax': 0,
            'sessions': 0
        })
        self.daily_stats = defaultdict(lambda: {
            'messages': 0,
            'climax': 0,
            'sessions': 0
        })
    
    def record_activity(self, activity_type: str):
        """Record an activity"""
        now = datetime.now()
        
        self.activity_log.append({
            'timestamp': now,
            'type': activity_type
        })
        
        # Update hourly stats
        hour_key = now.strftime('%Y-%m-%d %H:00')
        self.hourly_stats[hour_key][activity_type] += 1
        self.hourly_stats[hour_key]['total'] = self.hourly_stats[hour_key].get('total', 0) + 1
        
        # Update daily stats
        day_key = now.strftime('%Y-%m-%d')
        self.daily_stats[day_key][activity_type] += 1
        self.daily_stats[day_key]['total'] = self.daily_stats[day_key].get('total', 0) + 1
    
    def get_peak_hours(self, days: int = 7) -> List[Dict]:
        """Get peak hours in last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_hours = [
            h for h in self.hourly_stats.keys()
            if datetime.strptime(h, '%Y-%m-%d %H:00') > cutoff
        ]
        
        # Aggregate by hour of day
        hour_aggregate = defaultdict(lambda: {'messages': 0, 'climax': 0, 'total': 0})
        
        for hour_key in recent_hours:
            hour = int(hour_key.split()[1].split(':')[0])
            stats = self.hourly_stats[hour_key]
            
            hour_aggregate[hour]['messages'] += stats.get('messages', 0)
            hour_aggregate[hour]['climax'] += stats.get('climax', 0)
            hour_aggregate[hour]['total'] += stats.get('total', 0)
        
        # Sort by total activity
        peak_hours = sorted(
            [{'hour': h, **stats} for h, stats in hour_aggregate.items()],
            key=lambda x: x['total'],
            reverse=True
        )
        
        return peak_hours[:5]  # Top 5 peak hours
    
    def get_peak_days(self, weeks: int = 4) -> List[Dict]:
        """Get peak days in last N weeks"""
        cutoff = datetime.now() - timedelta(weeks=weeks)
        recent_days = [
            d for d in self.daily_stats.keys()
            if datetime.strptime(d, '%Y-%m-%d') > cutoff
        ]
        
        # Aggregate by day of week
        day_aggregate = defaultdict(lambda: {'messages': 0, 'climax': 0, 'total': 0})
        day_names = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        
        for day_key in recent_days:
            day_num = datetime.strptime(day_key, '%Y-%m-%d').weekday()
            stats = self.daily_stats[day_key]
            
            day_aggregate[day_num]['messages'] += stats.get('messages', 0)
            day_aggregate[day_num]['climax'] += stats.get('climax', 0)
            day_aggregate[day_num]['total'] += stats.get('total', 0)
        
        # Format results
        peak_days = [
            {
                'day': day_names[day_num],
                'day_num': day_num,
                **stats
            }
            for day_num, stats in day_aggregate.items()
        ]
        
        return sorted(peak_days, key=lambda x: x['total'], reverse=True)
    
    def get_recommended_time(self) -> Dict:
        """Get recommended time for optimal interaction"""
        peak_hours = self.get_peak_hours(14)  # Last 2 weeks
        
        if not peak_hours:
            return {
                'recommended_hour': 20,
                'reason': 'Belum cukup data, coba malam hari'
            }
        
        best_hour = peak_hours[0]['hour']
        
        # Determine best day
        peak_days = self.get_peak_days(4)
        best_day = peak_days[0]['day'] if peak_days else 'Minggu'
        
        # Generate reason
        if 5 <= best_hour < 11:
            time_desc = "pagi"
        elif 11 <= best_hour < 15:
            time_desc = "siang"
        elif 15 <= best_hour < 18:
            time_desc = "sore"
        elif 18 <= best_hour < 22:
            time_desc = "malam"
        else:
            time_desc = "dini hari"
        
        return {
            'recommended_hour': best_hour,
            'recommended_day': best_day,
            'description': f"{best_day} {time_desc} sekitar jam {best_hour}:00",
            'reason': f"Berdasarkan {peak_hours[0]['total']} aktivitas di jam tersebut"
        }
    
    def get_summary(self) -> Dict:
        """Get peak hours summary"""
        return {
            'peak_hours': self.get_peak_hours(),
            'peak_days': self.get_peak_days(),
            'recommendation': self.get_recommended_time(),
            'total_activities': len(self.activity_log)
        }


__all__ = ['PeakHoursAnalyzer']
