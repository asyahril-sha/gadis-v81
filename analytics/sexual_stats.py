#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL STATISTICS
=============================================================================
Statistik aktivitas seksual untuk single user
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class SexualStatistics:
    """Statistik aktivitas seksual"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        
        # Climax stats
        self.total_climax = 0
        self.bot_climax = 0
        self.user_climax = 0
        self.together_climax = 0
        self.climax_history = []
        
        # Position stats
        self.position_usage = defaultdict(int)
        self.position_climax = defaultdict(int)
        self.position_success_rate = defaultdict(float)
        self.favorite_positions = []
        
        # Area stats
        self.area_touched = defaultdict(int)
        self.area_sensitivity = defaultdict(float)
        self.favorite_areas = []
        
        # Activity stats
        self.activity_count = defaultdict(int)
        self.activity_duration = defaultdict(float)
        self.favorite_activities = []
        
        # Public area stats
        self.public_area_usage = defaultdict(int)
        self.public_success = defaultdict(int)
        self.public_fail = defaultdict(int)
        self.risk_taken = []
        
        # Timing
        self.sexual_peak_hours = defaultdict(int)
        self.last_activity = None
    
    def record_climax(self, climax_type: str, position: str = None, 
                     area: str = None, intensity: float = 0.5):
        """Record a climax"""
        self.total_climax += 1
        
        if climax_type == 'bot':
            self.bot_climax += 1
        elif climax_type == 'user':
            self.user_climax += 1
        elif climax_type == 'together':
            self.together_climax += 1
        
        if position:
            self.position_usage[position] += 1
            self.position_climax[position] += 1
        
        if area:
            self.area_touched[area] += 1
            # Update sensitivity (moving average)
            old_sens = self.area_sensitivity[area]
            total = self.area_touched[area]
            self.area_sensitivity[area] = (old_sens * (total-1) + intensity) / total
        
        # Record in history
        self.climax_history.append({
            'timestamp': datetime.now(),
            'type': climax_type,
            'position': position,
            'area': area,
            'intensity': intensity
        })
        
        # Update peak hours
        self.sexual_peak_hours[datetime.now().hour] += 1
        self.last_activity = datetime.now()
        
        # Update favorites
        self._update_favorites()
    
    def record_public_activity(self, area: str, success: bool, risk: float):
        """Record public area activity"""
        self.public_area_usage[area] += 1
        if success:
            self.public_success[area] += 1
        else:
            self.public_fail[area] += 1
        
        self.risk_taken.append({
            'timestamp': datetime.now(),
            'area': area,
            'risk': risk,
            'success': success
        })
    
    def record_activity(self, activity: str, duration: int = None):
        """Record sexual activity"""
        self.activity_count[activity] += 1
        if duration:
            old_dur = self.activity_duration[activity]
            total = self.activity_count[activity]
            self.activity_duration[activity] = (old_dur * (total-1) + duration) / total
    
    def _update_favorites(self):
        """Update favorite lists"""
        # Favorite positions
        self.favorite_positions = [
            pos for pos, count in 
            sorted(self.position_usage.items(), key=lambda x: x[1], reverse=True)
        ][:5]
        
        # Favorite areas
        self.favorite_areas = [
            area for area, count in 
            sorted(self.area_touched.items(), key=lambda x: x[1], reverse=True)
        ][:5]
        
        # Favorite activities
        self.favorite_activities = [
            act for act, count in 
            sorted(self.activity_count.items(), key=lambda x: x[1], reverse=True)
        ][:5]
        
        # Update success rates
        for pos in self.position_usage:
            if self.position_usage[pos] > 0:
                self.position_success_rate[pos] = self.position_climax[pos] / self.position_usage[pos]
    
    def get_stats(self) -> Dict:
        """Get complete sexual statistics"""
        return {
            'total_climax': self.total_climax,
            'bot_climax': self.bot_climax,
            'user_climax': self.user_climax,
            'together_climax': self.together_climax,
            'favorite_positions': self.favorite_positions,
            'favorite_areas': self.favorite_areas,
            'favorite_activities': self.favorite_activities,
            'position_success_rates': dict(self.position_success_rate),
            'peak_hours': dict(self.sexual_peak_hours),
            'public_area_stats': {
                area: {
                    'total': self.public_area_usage[area],
                    'success': self.public_success[area],
                    'fail': self.public_fail[area],
                    'success_rate': self.public_success[area] / self.public_area_usage[area] if self.public_area_usage[area] > 0 else 0
                }
                for area in self.public_area_usage
            },
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }
    
    def get_daily_report(self) -> Dict:
        """Get daily sexual report"""
        today = datetime.now().date()
        today_climax = [
            c for c in self.climax_history
            if c['timestamp'].date() == today
        ]
        
        return {
            'date': today.isoformat(),
            'total_climax': len(today_climax),
            'by_type': {
                'bot': sum(1 for c in today_climax if c['type'] == 'bot'),
                'user': sum(1 for c in today_climax if c['type'] == 'user'),
                'together': sum(1 for c in today_climax if c['type'] == 'together')
            },
            'favorite_position': max(
                [(p['position'], p['position'] in today_climax) for p in self.favorite_positions],
                key=lambda x: x[1]
            )[0] if self.favorite_positions else None
        }


__all__ = ['SexualStatistics']
