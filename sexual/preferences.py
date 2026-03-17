#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL PREFERENCES SYSTEM
=============================================================================
Belajar dan menyimpan preferensi seksual user
"""

from typing import Dict, List, Optional, Any
from collections import defaultdict, Counter
from datetime import datetime, timedelta


class SexualPreferences:
    """
    Sexual preferences learning system
    Bot belajar apa yang user suka dari interaksi
    """
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        
        # Position preferences
        self.position_preferences = Counter()
        self.position_success_rate = defaultdict(float)
        self.position_last_used = {}
        
        # Area preferences
        self.area_preferences = Counter()
        self.area_sensitivity = defaultdict(float)  # 0-1 how sensitive
        self.area_last_touched = {}
        
        # Activity preferences
        self.activity_preferences = Counter()
        self.activity_duration = defaultdict(float)  # average duration
        self.activity_last_done = {}
        
        # Climax preferences
        self.climax_preferences = Counter()
        self.climax_intensity = defaultdict(float)  # 0-1
        self.climax_count = 0
        self.together_climax_count = 0
        
        # Timing preferences
        self.peak_hours = Counter()  # hour of day
        self.peak_days = Counter()  # day of week
        
        # Public preferences
        self.public_area_preferences = Counter()
        self.risk_tolerance = 0.5  # 0-1
        self.public_success_rate = 0.0
        
        # Role preferences
        self.favorite_roles = Counter()
        
        # Stats
        self.total_sexual_interactions = 0
        self.first_interaction = None
        self.last_interaction = None
        self.last_update = datetime.now()
    
    def update_position(self, position_id: str, success: bool = True, 
                       duration: int = None, intensity: float = None):
        """Update position preference"""
        self.position_preferences[position_id] += 1
        self.position_last_used[position_id] = datetime.now()
        
        # Update success rate
        old_rate = self.position_success_rate[position_id]
        total = self.position_preferences[position_id]
        self.position_success_rate[position_id] = (old_rate * (total-1) + (1.0 if success else 0.0)) / total
        
        self.total_sexual_interactions += 1
        self.last_interaction = datetime.now()
        if not self.first_interaction:
            self.first_interaction = datetime.now()
    
    def update_area(self, area_id: str, sensitivity: float = None):
        """Update area preference"""
        self.area_preferences[area_id] += 1
        self.area_last_touched[area_id] = datetime.now()
        
        # Update sensitivity (moving average)
        if sensitivity:
            old_sens = self.area_sensitivity[area_id]
            total = self.area_preferences[area_id]
            self.area_sensitivity[area_id] = (old_sens * (total-1) + sensitivity) / total
    
    def update_activity(self, activity_id: str, duration: int = None):
        """Update activity preference"""
        self.activity_preferences[activity_id] += 1
        self.activity_last_done[activity_id] = datetime.now()
        
        # Update average duration
        if duration:
            old_dur = self.activity_duration[activity_id]
            total = self.activity_preferences[activity_id]
            self.activity_duration[activity_id] = (old_dur * (total-1) + duration) / total
    
    def update_climax(self, climax_type: str, intensity: float = 0.5):
        """Update climax preference"""
        self.climax_preferences[climax_type] += 1
        self.climax_count += 1
        
        if climax_type == 'together':
            self.together_climax_count += 1
        
        # Update average intensity
        key = f"climax_{climax_type}"
        old_intensity = self.climax_intensity[key]
        total = self.climax_preferences[climax_type]
        self.climax_intensity[key] = (old_intensity * (total-1) + intensity) / total
    
    def update_time(self, timestamp: datetime = None):
        """Update timing preference"""
        if not timestamp:
            timestamp = datetime.now()
        
        self.peak_hours[timestamp.hour] += 1
        self.peak_days[timestamp.weekday()] += 1
    
    def update_public(self, area_id: str, success: bool):
        """Update public area preference"""
        self.public_area_preferences[area_id] += 1
        
        # Update success rate
        total = self.public_area_preferences[area_id]
        self.public_success_rate = (self.public_success_rate * (total-1) + (1.0 if success else 0.0)) / total
    
    def update_role(self, role: str):
        """Update role preference"""
        self.favorite_roles[role] += 1
    
    def get_favorite_positions(self, limit: int = 5) -> List[tuple]:
        """Get top favorite positions"""
        return self.position_preferences.most_common(limit)
    
    def get_best_positions(self, limit: int = 5) -> List[Dict]:
        """Get positions with highest success rate"""
        positions = []
        for pos_id, rate in self.position_success_rate.items():
            if rate > 0.7:  # Success rate > 70%
                positions.append({
                    'id': pos_id,
                    'success_rate': rate,
                    'times_used': self.position_preferences[pos_id]
                })
        
        return sorted(positions, key=lambda x: x['success_rate'], reverse=True)[:limit]
    
    def get_favorite_areas(self, limit: int = 5) -> List[tuple]:
        """Get top favorite areas"""
        return self.area_preferences.most_common(limit)
    
    def get_most_sensitive_areas(self, limit: int = 5) -> List[Dict]:
        """Get most sensitive areas"""
        areas = []
        for area_id, sens in self.area_sensitivity.items():
            if sens > 0.6:  # Sensitivity > 60%
                areas.append({
                    'id': area_id,
                    'sensitivity': sens,
                    'times_touched': self.area_preferences[area_id]
                })
        
        return sorted(areas, key=lambda x: x['sensitivity'], reverse=True)[:limit]
    
    def get_favorite_activities(self, limit: int = 5) -> List[tuple]:
        """Get top favorite activities"""
        return self.activity_preferences.most_common(limit)
    
    def get_peak_hours(self) -> List[int]:
        """Get peak hours for sexual activity"""
        return [hour for hour, count in self.peak_hours.most_common(3)]
    
    def get_compatibility_score(self, other_prefs: 'SexualPreferences') -> float:
        """Calculate sexual compatibility with another user"""
        if not other_prefs:
            return 0.0
        
        # Compare position preferences
        pos_score = self._compare_counters(
            self.position_preferences, 
            other_prefs.position_preferences
        )
        
        # Compare area preferences
        area_score = self._compare_counters(
            self.area_preferences,
            other_prefs.area_preferences
        )
        
        # Compare activity preferences
        act_score = self._compare_counters(
            self.activity_preferences,
            other_prefs.activity_preferences
        )
        
        # Compare timing
        time_score = self._compare_peak_hours(other_prefs)
        
        # Weighted average
        total_score = (
            pos_score * 0.3 +
            area_score * 0.3 +
            act_score * 0.3 +
            time_score * 0.1
        )
        
        return round(total_score, 2)
    
    def _compare_counters(self, c1: Counter, c2: Counter) -> float:
        """Compare two counters"""
        if not c1 or not c2:
            return 0.5
        
        # Get top 3 from each
        top1 = [item for item, _ in c1.most_common(3)]
        top2 = [item for item, _ in c2.most_common(3)]
        
        # Calculate overlap
        common = set(top1) & set(top2)
        return len(common) / 3.0
    
    def _compare_peak_hours(self, other: 'SexualPreferences') -> float:
        """Compare peak hours"""
        my_hours = [h for h, _ in self.peak_hours.most_common(3)]
        other_hours = [h for h, _ in other.peak_hours.most_common(3)]
        
        if not my_hours or not other_hours:
            return 0.5
        
        common = set(my_hours) & set(other_hours)
        return len(common) / 3.0
    
    def get_summary(self) -> Dict:
        """Get preferences summary"""
        return {
            'favorite_positions': self.get_favorite_positions(3),
            'favorite_areas': self.get_favorite_areas(3),
            'favorite_activities': self.get_favorite_activities(3),
            'most_sensitive_areas': self.get_most_sensitive_areas(3),
            'peak_hours': self.get_peak_hours(),
            'total_climax': self.climax_count,
            'together_climax': self.together_climax_count,
            'risk_tolerance': round(self.risk_tolerance, 2),
            'public_success_rate': round(self.public_success_rate, 2),
            'total_interactions': self.total_sexual_interactions
        }
    
    def to_dict(self) -> Dict:
        """Convert to dict for storage"""
        return {
            'user_id': self.user_id,
            'position_preferences': dict(self.position_preferences),
            'position_success_rate': dict(self.position_success_rate),
            'area_preferences': dict(self.area_preferences),
            'area_sensitivity': dict(self.area_sensitivity),
            'activity_preferences': dict(self.activity_preferences),
            'activity_duration': dict(self.activity_duration),
            'climax_preferences': dict(self.climax_preferences),
            'climax_intensity': dict(self.climax_intensity),
            'climax_count': self.climax_count,
            'together_climax_count': self.together_climax_count,
            'peak_hours': dict(self.peak_hours),
            'peak_days': dict(self.peak_days),
            'public_area_preferences': dict(self.public_area_preferences),
            'risk_tolerance': self.risk_tolerance,
            'public_success_rate': self.public_success_rate,
            'favorite_roles': dict(self.favorite_roles),
            'total_sexual_interactions': self.total_sexual_interactions,
            'first_interaction': self.first_interaction.isoformat() if self.first_interaction else None,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None,
            'last_update': self.last_update.isoformat()
        }


class SexualPreferencesManager:
    """Manager for multiple users' sexual preferences"""
    
    def __init__(self):
        self.user_preferences: Dict[int, SexualPreferences] = {}
    
    def get_preferences(self, user_id: int) -> SexualPreferences:
        """Get or create preferences for user"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = SexualPreferences(user_id)
        return self.user_preferences[user_id]
    
    def calculate_compatibility(self, user1: int, user2: int) -> float:
        """Calculate sexual compatibility between two users"""
        prefs1 = self.get_preferences(user1)
        prefs2 = self.get_preferences(user2)
        return prefs1.get_compatibility_score(prefs2)
    
    def save_all(self) -> Dict[int, Dict]:
        """Save all preferences to dict"""
        return {uid: prefs.to_dict() for uid, prefs in self.user_preferences.items()}
    
    def load_all(self, data: Dict[int, Dict]):
        """Load all preferences from dict"""
        for uid, prefs_data in data.items():
            prefs = SexualPreferences(uid)
            # Load data (implementation depends on storage format)
            self.user_preferences[uid] = prefs


__all__ = ['SexualPreferences', 'SexualPreferencesManager']
