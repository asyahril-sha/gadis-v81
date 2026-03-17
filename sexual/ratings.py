#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL RATINGS SYSTEM
=============================================================================
Rating system untuk posisi, area, dan aktivitas seksual
"""

from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import statistics


class PositionRating:
    """Rating untuk posisi seksual"""
    
    def __init__(self, position_id: str, position_name: str):
        self.position_id = position_id
        self.position_name = position_name
        
        # Rating stats
        self.ratings = []  # List of rating values (1-5)
        self.difficulty_ratings = []  # 1-5
        self.intensity_ratings = []  # 1-5
        self.comfort_ratings = []  # 1-5
        
        # User feedback
        self.user_ratings = defaultdict(list)  # user_id -> ratings
        self.user_comments = []
        
        # Success rate
        self.success_count = 0
        self.fail_count = 0
        
        # Usage stats
        self.total_uses = 0
        self.last_used = None
        self.popularity = 0  # 0-100
        
        # Tags
        self.tags = Counter()
        
        # Relationships
        self.similar_positions = []  # IDs of similar positions
        self.prerequisites = []  # Positions that lead to this
        self.next_positions = []  # Common next positions
    
    def add_rating(self, rating: int, user_id: int = None, 
                  difficulty: int = None, intensity: int = None,
                  comfort: int = None, comment: str = None):
        """Add a rating for this position"""
        rating = max(1, min(5, rating))
        self.ratings.append(rating)
        
        if difficulty:
            self.difficulty_ratings.append(max(1, min(5, difficulty)))
        if intensity:
            self.intensity_ratings.append(max(1, min(5, intensity)))
        if comfort:
            self.comfort_ratings.append(max(1, min(5, comfort)))
        
        if user_id:
            self.user_ratings[user_id].append(rating)
        
        if comment:
            self.user_comments.append({
                'user_id': user_id,
                'comment': comment,
                'timestamp': datetime.now(),
                'rating': rating
            })
        
        self.total_uses += 1
        self.last_used = datetime.now()
    
    def add_use(self, success: bool = True):
        """Record a use of this position"""
        self.total_uses += 1
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
        self.last_used = datetime.now()
    
    def add_tag(self, tag: str):
        """Add tag to position"""
        self.tags[tag] += 1
    
    def get_average_rating(self) -> float:
        """Get average rating"""
        if not self.ratings:
            return 0.0
        return statistics.mean(self.ratings)
    
    def get_average_difficulty(self) -> float:
        """Get average difficulty"""
        if not self.difficulty_ratings:
            return 0.0
        return statistics.mean(self.difficulty_ratings)
    
    def get_average_intensity(self) -> float:
        """Get average intensity"""
        if not self.intensity_ratings:
            return 0.0
        return statistics.mean(self.intensity_ratings)
    
    def get_average_comfort(self) -> float:
        """Get average comfort"""
        if not self.comfort_ratings:
            return 0.0
        return statistics.mean(self.comfort_ratings)
    
    def get_success_rate(self) -> float:
        """Get success rate"""
        total = self.success_count + self.fail_count
        if total == 0:
            return 0.0
        return self.success_count / total
    
    def get_rating_distribution(self) -> Dict[int, int]:
        """Get distribution of ratings"""
        dist = {1:0, 2:0, 3:0, 4:0, 5:0}
        for r in self.ratings:
            dist[r] += 1
        return dist
    
    def get_user_rating(self, user_id: int) -> Optional[float]:
        """Get average rating from specific user"""
        if user_id not in self.user_ratings:
            return None
        ratings = self.user_ratings[user_id]
        return statistics.mean(ratings)
    
    def get_recent_comments(self, limit: int = 10) -> List[Dict]:
        """Get most recent comments"""
        sorted_comments = sorted(
            self.user_comments,
            key=lambda x: x['timestamp'],
            reverse=True
        )
        return sorted_comments[:limit]
    
    def get_top_tags(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Get most common tags"""
        return self.tags.most_common(limit)
    
    def update_popularity(self, all_positions: Dict[str, 'PositionRating']):
        """Update popularity score based on total uses"""
        total_uses = sum(p.total_uses for p in all_positions.values())
        if total_uses > 0:
            self.popularity = (self.total_uses / total_uses) * 100
    
    def to_dict(self) -> Dict:
        """Convert to dict for storage"""
        return {
            'position_id': self.position_id,
            'position_name': self.position_name,
            'average_rating': self.get_average_rating(),
            'average_difficulty': self.get_average_difficulty(),
            'average_intensity': self.get_average_intensity(),
            'average_comfort': self.get_average_comfort(),
            'success_rate': self.get_success_rate(),
            'total_uses': self.total_uses,
            'popularity': self.popularity,
            'rating_distribution': self.get_rating_distribution(),
            'top_tags': self.get_top_tags(5),
            'last_used': self.last_used.isoformat() if self.last_used else None
        }


class AreaRating:
    """Rating untuk area sensitif"""
    
    def __init__(self, area_id: str, area_name: str):
        self.area_id = area_id
        self.area_name = area_name
        
        # Sensitivity ratings
        self.sensitivity_ratings = []  # 1-5
        self.pleasure_ratings = []  # 1-5
        
        # User feedback
        self.user_ratings = defaultdict(list)
        self.user_comments = []
        
        # Usage stats
        self.total_touches = 0
        self.last_touched = None
        
        # Success rate (how often touch leads to climax)
        self.climax_after_touch = 0
        self.touches_without_climax = 0
        
        # Tags
        self.tags = Counter()
        
        # Related areas
        self.connected_areas = []  # Areas often touched together
    
    def add_rating(self, sensitivity: int, pleasure: int, 
                  user_id: int = None, comment: str = None):
        """Add rating for this area"""
        sensitivity = max(1, min(5, sensitivity))
        pleasure = max(1, min(5, pleasure))
        
        self.sensitivity_ratings.append(sensitivity)
        self.pleasure_ratings.append(pleasure)
        
        if user_id:
            self.user_ratings[user_id].append((sensitivity, pleasure))
        
        if comment:
            self.user_comments.append({
                'user_id': user_id,
                'comment': comment,
                'timestamp': datetime.now(),
                'sensitivity': sensitivity,
                'pleasure': pleasure
            })
    
    def add_touch(self, led_to_climax: bool = False):
        """Record a touch to this area"""
        self.total_touches += 1
        self.last_touched = datetime.now()
        
        if led_to_climax:
            self.climax_after_touch += 1
        else:
            self.touches_without_climax += 1
    
    def add_tag(self, tag: str):
        """Add tag to area"""
        self.tags[tag] += 1
    
    def get_average_sensitivity(self) -> float:
        """Get average sensitivity rating"""
        if not self.sensitivity_ratings:
            return 0.0
        return statistics.mean(self.sensitivity_ratings)
    
    def get_average_pleasure(self) -> float:
        """Get average pleasure rating"""
        if not self.pleasure_ratings:
            return 0.0
        return statistics.mean(self.pleasure_ratings)
    
    def get_climax_probability(self) -> float:
        """Get probability that touching this area leads to climax"""
        total = self.climax_after_touch + self.touches_without_climax
        if total == 0:
            return 0.0
        return self.climax_after_touch / total
    
    def get_user_rating(self, user_id: int) -> Optional[Tuple[float, float]]:
        """Get average rating from specific user"""
        if user_id not in self.user_ratings:
            return None
        ratings = self.user_ratings[user_id]
        avg_sens = statistics.mean(r[0] for r in ratings)
        avg_pleasure = statistics.mean(r[1] for r in ratings)
        return (avg_sens, avg_pleasure)
    
    def get_recent_comments(self, limit: int = 10) -> List[Dict]:
        """Get most recent comments"""
        sorted_comments = sorted(
            self.user_comments,
            key=lambda x: x['timestamp'],
            reverse=True
        )
        return sorted_comments[:limit]
    
    def get_top_tags(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Get most common tags"""
        return self.tags.most_common(limit)
    
    def to_dict(self) -> Dict:
        """Convert to dict for storage"""
        return {
            'area_id': self.area_id,
            'area_name': self.area_name,
            'average_sensitivity': self.get_average_sensitivity(),
            'average_pleasure': self.get_average_pleasure(),
            'climax_probability': self.get_climax_probability(),
            'total_touches': self.total_touches,
            'top_tags': self.get_top_tags(5),
            'last_touched': self.last_touched.isoformat() if self.last_touched else None
        }


class ActivityRating:
    """Rating untuk aktivitas seksual"""
    
    def __init__(self, activity_id: str, activity_name: str):
        self.activity_id = activity_id
        self.activity_name = activity_name
        
        # Rating stats
        self.enjoyment_ratings = []  # 1-5
        self.intensity_ratings = []  # 1-5
        
        # Duration stats
        self.durations = []  # in minutes
        
        # User feedback
        self.user_ratings = defaultdict(list)
        self.user_comments = []
        
        # Usage stats
        self.total_performed = 0
        self.last_performed = None
        
        # Success rate
        self.success_count = 0
        self.fail_count = 0
        
        # Tags
        self.tags = Counter()
        
        # Related activities
        self.common_before = []  # Activities often done before
        self.common_after = []  # Activities often done after
    
    def add_rating(self, enjoyment: int, intensity: int = None,
                  duration: int = None, user_id: int = None,
                  success: bool = True, comment: str = None):
        """Add rating for this activity"""
        enjoyment = max(1, min(5, enjoyment))
        self.enjoyment_ratings.append(enjoyment)
        
        if intensity:
            self.intensity_ratings.append(max(1, min(5, intensity)))
        
        if duration:
            self.durations.append(duration)
        
        if user_id:
            self.user_ratings[user_id].append(enjoyment)
        
        if comment:
            self.user_comments.append({
                'user_id': user_id,
                'comment': comment,
                'timestamp': datetime.now(),
                'enjoyment': enjoyment
            })
        
        self.total_performed += 1
        self.last_performed = datetime.now()
        
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
    
    def add_tag(self, tag: str):
        """Add tag to activity"""
        self.tags[tag] += 1
    
    def get_average_enjoyment(self) -> float:
        """Get average enjoyment rating"""
        if not self.enjoyment_ratings:
            return 0.0
        return statistics.mean(self.enjoyment_ratings)
    
    def get_average_intensity(self) -> float:
        """Get average intensity rating"""
        if not self.intensity_ratings:
            return 0.0
        return statistics.mean(self.intensity_ratings)
    
    def get_average_duration(self) -> float:
        """Get average duration in minutes"""
        if not self.durations:
            return 0.0
        return statistics.mean(self.durations)
    
    def get_success_rate(self) -> float:
        """Get success rate"""
        total = self.success_count + self.fail_count
        if total == 0:
            return 0.0
        return self.success_count / total
    
    def get_user_rating(self, user_id: int) -> Optional[float]:
        """Get average rating from specific user"""
        if user_id not in self.user_ratings:
            return None
        ratings = self.user_ratings[user_id]
        return statistics.mean(ratings)
    
    def get_recent_comments(self, limit: int = 10) -> List[Dict]:
        """Get most recent comments"""
        sorted_comments = sorted(
            self.user_comments,
            key=lambda x: x['timestamp'],
            reverse=True
        )
        return sorted_comments[:limit]
    
    def get_top_tags(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Get most common tags"""
        return self.tags.most_common(limit)
    
    def to_dict(self) -> Dict:
        """Convert to dict for storage"""
        return {
            'activity_id': self.activity_id,
            'activity_name': self.activity_name,
            'average_enjoyment': self.get_average_enjoyment(),
            'average_intensity': self.get_average_intensity(),
            'average_duration': self.get_average_duration(),
            'success_rate': self.get_success_rate(),
            'total_performed': self.total_performed,
            'top_tags': self.get_top_tags(5),
            'last_performed': self.last_performed.isoformat() if self.last_performed else None
        }


class RatingManager:
    """Manager for all ratings"""
    
    def __init__(self):
        self.positions: Dict[str, PositionRating] = {}
        self.areas: Dict[str, AreaRating] = {}
        self.activities: Dict[str, ActivityRating] = {}
    
    def add_position(self, position_id: str, position_name: str) -> PositionRating:
        """Add a new position"""
        if position_id not in self.positions:
            self.positions[position_id] = PositionRating(position_id, position_name)
        return self.positions[position_id]
    
    def add_area(self, area_id: str, area_name: str) -> AreaRating:
        """Add a new area"""
        if area_id not in self.areas:
            self.areas[area_id] = AreaRating(area_id, area_name)
        return self.areas[area_id]
    
    def add_activity(self, activity_id: str, activity_name: str) -> ActivityRating:
        """Add a new activity"""
        if activity_id not in self.activities:
            self.activities[activity_id] = ActivityRating(activity_id, activity_name)
        return self.activities[activity_id]
    
    def get_top_positions(self, limit: int = 10, 
                         min_uses: int = 5) -> List[PositionRating]:
        """Get top rated positions"""
        candidates = [p for p in self.positions.values() if p.total_uses >= min_uses]
        sorted_positions = sorted(
            candidates,
            key=lambda x: x.get_average_rating(),
            reverse=True
        )
        return sorted_positions[:limit]
    
    def get_top_areas(self, limit: int = 10,
                     min_touches: int = 5) -> List[AreaRating]:
        """Get top rated areas"""
        candidates = [a for a in self.areas.values() if a.total_touches >= min_touches]
        sorted_areas = sorted(
            candidates,
            key=lambda x: x.get_average_pleasure(),
            reverse=True
        )
        return sorted_areas[:limit]
    
    def get_top_activities(self, limit: int = 10,
                          min_performed: int = 5) -> List[ActivityRating]:
        """Get top rated activities"""
        candidates = [a for a in self.activities.values() if a.total_performed >= min_performed]
        sorted_activities = sorted(
            candidates,
            key=lambda x: x.get_average_enjoyment(),
            reverse=True
        )
        return sorted_activities[:limit]
    
    def get_most_popular_positions(self, limit: int = 10) -> List[PositionRating]:
        """Get most used positions"""
        sorted_positions = sorted(
            self.positions.values(),
            key=lambda x: x.total_uses,
            reverse=True
        )
        return sorted_positions[:limit]
    
    def get_most_sensitive_areas(self, limit: int = 10) -> List[AreaRating]:
        """Get most sensitive areas"""
        sorted_areas = sorted(
            self.areas.values(),
            key=lambda x: x.get_average_sensitivity(),
            reverse=True
        )
        return sorted_areas[:limit]
    
    def update_popularity_scores(self):
        """Update popularity scores for all items"""
        for pos in self.positions.values():
            pos.update_popularity(self.positions)
    
    def get_recommendations(self, user_preferences: Dict, 
                           limit: int = 5) -> Dict[str, List]:
        """Get personalized recommendations based on user preferences"""
        recommendations = {
            'positions': [],
            'areas': [],
            'activities': []
        }
        
        # Get favorite tags from user
        fav_tags = user_preferences.get('favorite_tags', [])
        
        # Recommend positions with matching tags
        for pos in self.positions.values():
            pos_tags = [tag for tag, _ in pos.get_top_tags(3)]
            if any(tag in fav_tags for tag in pos_tags):
                recommendations['positions'].append(pos)
        
        # Sort by rating
        recommendations['positions'] = sorted(
            recommendations['positions'],
            key=lambda x: x.get_average_rating(),
            reverse=True
        )[:limit]
        
        # Similar for areas and activities
        recommendations['areas'] = sorted(
            self.areas.values(),
            key=lambda x: x.get_average_pleasure(),
            reverse=True
        )[:limit]
        
        recommendations['activities'] = sorted(
            self.activities.values(),
            key=lambda x: x.get_average_enjoyment(),
            reverse=True
        )[:limit]
        
        return recommendations
    
    def to_dict(self) -> Dict:
        """Convert all ratings to dict"""
        return {
            'positions': {pid: p.to_dict() for pid, p in self.positions.items()},
            'areas': {aid: a.to_dict() for aid, a in self.areas.items()},
            'activities': {aid: a.to_dict() for aid, a in self.activities.items()}
        }


__all__ = [
    'PositionRating',
    'AreaRating',
    'ActivityRating',
    'RatingManager'
]
