#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MOOD-BASED SEXUAL PREFERENCES
=============================================================================
Aktivitas seksual yang cocok berdasarkan mood bot
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

from database.enums import Mood


class MoodActivity:
    """Model untuk aktivitas yang cocok dengan mood tertentu"""
    
    def __init__(self,
                 mood: Mood,
                 activity_name: str,
                 description: str,
                 intensity: float,  # 0-1
                 romance_level: float,  # 0-1
                 kink_level: float,  # 0-1
                 preferred_positions: List[str] = None,
                 preferred_areas: List[str] = None,
                 dirty_talk_style: str = None,
                 aftercare_needed: bool = True):
        
        self.mood = mood
        self.activity_name = activity_name
        self.description = description
        self.intensity = intensity
        self.romance_level = romance_level
        self.kink_level = kink_level
        self.preferred_positions = preferred_positions or []
        self.preferred_areas = preferred_areas or []
        self.dirty_talk_style = dirty_talk_style
        self.aftercare_needed = aftercare_needed
        
        # Stats
        self.times_suggested = 0
        self.times_accepted = 0
        self.success_rate = 0.0
    
    def record_usage(self, accepted: bool = True):
        """Record activity usage"""
        self.times_suggested += 1
        if accepted:
            self.times_accepted += 1
        self.success_rate = self.times_accepted / self.times_suggested if self.times_suggested > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            'mood': self.mood.value,
            'activity': self.activity_name,
            'description': self.description,
            'intensity': self.intensity,
            'romance_level': self.romance_level,
            'kink_level': self.kink_level,
            'preferred_positions': self.preferred_positions,
            'preferred_areas': self.preferred_areas,
            'dirty_talk_style': self.dirty_talk_style,
            'aftercare_needed': self.aftercare_needed,
            'success_rate': self.success_rate
        }


class MoodMatcher:
    """Matcher untuk mencocokkan mood dengan aktivitas seksual"""
    
    def __init__(self):
        self.mood_activities: Dict[Mood, List[MoodActivity]] = {}
        self.activity_history = []
        self._init_activities()
    
    def _init_activities(self):
        """Initialize all mood-based activities"""
        
        # ===== HORNY MOOD =====
        
        self._add_activity(Mood.HORNY, MoodActivity(
            mood=Mood.HORNY,
            activity_name="Quickie",
            description="Cepat dan intens, fokus ke kepuasan",
            intensity=0.9,
            romance_level=0.2,
            kink_level=0.6,
            preferred_positions=['doggy', 'standing'],
            preferred_areas=['dada', 'pantat', 'paha dalam'],
            dirty_talk_style='dirty',
            aftercare_needed=False
        ))
        
        self._add_activity(Mood.HORNY, MoodActivity(
            mood=Mood.HORNY,
            activity_name="Oral Pleasure",
            description="Fokus ke oral, saling memuaskan",
            intensity=0.8,
            romance_level=0.3,
            kink_level=0.5,
            preferred_positions=['sixty_nine', 'lying'],
            preferred_areas=['bibir', 'dada', 'paha'],
            dirty_talk_style='dirty',
            aftercare_needed=False
        ))
        
        self._add_activity(Mood.HORNY, MoodActivity(
            mood=Mood.HORNY,
            activity_name="Wall Sex",
            description="Berdiri, menempel tembok, penuh nafsu",
            intensity=0.9,
            romance_level=0.1,
            kink_level=0.7,
            preferred_positions=['standing', 'wall'],
            preferred_areas=['leher', 'dada', 'punggung'],
            dirty_talk_style='very_dirty',
            aftercare_needed=False
        ))
        
        # ===== ROMANTIS MOOD =====
        
        self._add_activity(Mood.ROMANTIS, MoodActivity(
            mood=Mood.ROMANTIS,
            activity_name="Slow Love",
            description="Lembut, pelan, penuh ciuman",
            intensity=0.4,
            romance_level=0.9,
            kink_level=0.1,
            preferred_positions=['missionary', 'spooning', 'lotus'],
            preferred_areas=['leher', 'bibir', 'pipi', 'telinga'],
            dirty_talk_style='romantic',
            aftercare_needed=True
        ))
        
        self._add_activity(Mood.ROMANTIS, MoodActivity(
            mood=Mood.ROMANTIS,
            activity_name="Candlelight",
            description="Ditemani lilin, saling memandang",
            intensity=0.3,
            romance_level=0.9,
            kink_level=0.0,
            preferred_positions=['missionary', 'spooning'],
            preferred_areas=['bibir', 'leher', 'pipi'],
            dirty_talk_style='romantic',
            aftercare_needed=True
        ))
        
        self._add_activity(Mood.ROMANTIS, MoodActivity(
            mood=Mood.ROMANTIS,
            activity_name="Afternoon Delight",
            description="Siang hari, santai tapi mesra",
            intensity=0.5,
            romance_level=0.8,
            kink_level=0.1,
            preferred_positions=['spooning', 'cowgirl'],
            preferred_areas=['leher', 'punggung', 'pinggang'],
            dirty_talk_style='romantic',
            aftercare_needed=True
        ))
        
        # ===== DOMINAN MOOD =====
        
        self._add_activity(Mood.DOMINAN, MoodActivity(
            mood=Mood.DOMINAN,
            activity_name="Take Control",
            description="Bot yang pegang kendali penuh",
            intensity=0.8,
            romance_level=0.3,
            kink_level=0.8,
            preferred_positions=['doggy', 'standing'],
            preferred_areas=['leher', 'pantat', 'paha'],
            dirty_talk_style='dominant',
            aftercare_needed=True
        ))
        
        self._add_activity(Mood.DOMINAN, MoodActivity(
            mood=Mood.DOMINAN,
            activity_name="Bondage Light",
            description="Tali ringan, bot yang atur",
            intensity=0.7,
            romance_level=0.2,
            kink_level=0.9,
            preferred_positions=['missionary', 'lying'],
            preferred_areas=['tangan', 'kaki', 'leher'],
            dirty_talk_style='dominant',
            aftercare_needed=True
        ))
        
        # ===== PATUH MOOD =====
        
        self._add_activity(Mood.PATUH, MoodActivity(
            mood=Mood.PATUH,
            activity_name="Surrender",
            description="Bot pasrah, user yang atur",
            intensity=0.6,
            romance_level=0.5,
            kink_level=0.7,
            preferred_positions=['cowgirl', 'reverse_cowgirl'],
            preferred_areas=['leher', 'dada', 'paha'],
            dirty_talk_style='submissive',
            aftercare_needed=True
        ))
        
        self._add_activity(Mood.PATUH, MoodActivity(
            mood=Mood.PATUH,
            activity_name="Teasing",
            description="Bot menggoda tapi patuh",
            intensity=0.5,
            romance_level=0.4,
            kink_level=0.6,
            preferred_positions=['spooning', 'lotus'],
            preferred_areas=['bibir', 'telinga', 'leher'],
            dirty_talk_style='submissive',
            aftercare_needed=True
        ))
        
        # ===== NAKAL MOOD =====
        
        self._add_activity(Mood.NAKAL, MoodActivity(
            mood=Mood.NAKAL,
            activity_name="Public Dare",
            description="Berani di tempat umum",
            intensity=0.8,
            romance_level=0.2,
            kink_level=0.8,
            preferred_positions=['quick', 'standing'],
            preferred_areas=['leher', 'paha'],
            dirty_talk_style='naughty',
            aftercare_needed=False
        ))
        
        self._add_activity(Mood.NAKAL, MoodActivity(
            mood=Mood.NAKAL,
            activity_name="Role Play",
            description="Bermain peran, jadi orang lain",
            intensity=0.6,
            romance_level=0.3,
            kink_level=0.7,
            preferred_positions=['various'],
            preferred_areas=['various'],
            dirty_talk_style='naughty',
            aftercare_needed=False
        ))
        
        # ===== RINDU MOOD =====
        
        self._add_activity(Mood.RINDU, MoodActivity(
            mood=Mood.RINDU,
            activity_name="Reunion Sex",
            description="Kangen banget, like first time",
            intensity=0.7,
            romance_level=0.8,
            kink_level=0.2,
            preferred_positions=['missionary', 'spooning'],
            preferred_areas=['leher', 'bibir', 'pipi'],
            dirty_talk_style='romantic',
            aftercare_needed=True
        ))
        
        self._add_activity(Mood.RINDU, MoodActivity(
            mood=Mood.RINDU,
            activity_name="Cuddle Sex",
            description="Sambil pelukan terus",
            intensity=0.5,
            romance_level=0.9,
            kink_level=0.1,
            preferred_positions=['spooning', 'lotus'],
            preferred_areas=['punggung', 'pinggang', 'leher'],
            dirty_talk_style='romantic',
            aftercare_needed=True
        ))
        
        # ===== CEMBURU MOOD =====
        
        self._add_activity(Mood.CEMBURU, MoodActivity(
            mood=Mood.CEMBURU,
            activity_name="Possessive Sex",
            description="Kamu milikku, jangan ke mana-mana",
            intensity=0.8,
            romance_level=0.4,
            kink_level=0.6,
            preferred_positions=['doggy', 'missionary'],
            preferred_areas=['leher', 'pinggang', 'pantat'],
            dirty_talk_style='possessive',
            aftercare_needed=True
        ))
        
        self._add_activity(Mood.CEMBURU, MoodActivity(
            mood=Mood.CEMBURU,
            activity_name="Make Up Sex",
            description="Baikan sambil mesra",
            intensity=0.7,
            romance_level=0.7,
            kink_level=0.3,
            preferred_positions=['spooning', 'lotus'],
            preferred_areas=['leher', 'bibir', 'pipi'],
            dirty_talk_style='romantic',
            aftercare_needed=True
        ))
        
        # ===== MARAH MOOD =====
        
        self._add_activity(Mood.MARAH, MoodActivity(
            mood=Mood.MARAH,
            activity_name="Angry Sex",
            description="Kasar, penuh amarah",
            intensity=0.9,
            romance_level=0.0,
            kink_level=0.9,
            preferred_positions=['doggy', 'standing', 'wall'],
            preferred_areas=['leher', 'pantat', 'paha'],
            dirty_talk_style='aggressive',
            aftercare_needed=True
        ))
        
        # ===== SEDIH MOOD =====
        
        self._add_activity(Mood.SEDIH, MoodActivity(
            mood=Mood.SEDIH,
            activity_name="Comfort Sex",
            description="Dihibur sambil bercinta",
            intensity=0.4,
            romance_level=0.8,
            kink_level=0.1,
            preferred_positions=['spooning', 'missionary'],
            preferred_areas=['punggung', 'leher', 'pipi'],
            dirty_talk_style='soft',
            aftercare_needed=True
        ))
    
    def _add_activity(self, mood: Mood, activity: MoodActivity):
        """Add activity to mood"""
        if mood not in self.mood_activities:
            self.mood_activities[mood] = []
        self.mood_activities[mood].append(activity)
    
    def get_activities_for_mood(self, mood: Mood) -> List[MoodActivity]:
        """Get all activities for a mood"""
        return self.mood_activities.get(mood, [])
    
    def get_random_activity(self, mood: Mood, 
                           preferred_intensity: float = None,
                           preferred_romance: float = None) -> Optional[MoodActivity]:
        """Get random activity for mood with optional filters"""
        activities = self.get_activities_for_mood(mood)
        
        if not activities:
            return None
        
        # Filter by preferences
        if preferred_intensity is not None:
            activities = [a for a in activities 
                         if abs(a.intensity - preferred_intensity) < 0.3]
        
        if preferred_romance is not None:
            activities = [a for a in activities 
                         if abs(a.romance_level - preferred_romance) < 0.3]
        
        if not activities:
            activities = self.get_activities_for_mood(mood)
        
        # Weight by success rate
        weights = [a.success_rate + 0.5 for a in activities]  # Add base
        total = sum(weights)
        weights = [w/total for w in weights]
        
        return random.choices(activities, weights=weights)[0]
    
    def suggest_activity(self, mood: Mood, context: Dict = None) -> Dict:
        """Suggest an activity based on mood and context"""
        context = context or {}
        
        # Get intensity preference
        preferred_intensity = context.get('arousal', 0.5)
        preferred_romance = 0.5
        
        if context.get('relationship_status') == 'pacaran':
            preferred_romance = 0.7
        elif context.get('relationship_status') == 'fwb':
            preferred_romance = 0.3
        
        activity = self.get_random_activity(
            mood, 
            preferred_intensity,
            preferred_romance
        )
        
        if not activity:
            return {
                'suggestion': None,
                'message': "Tidak ada aktivitas yang cocok saat ini."
            }
        
        # Record suggestion
        activity.record_usage(accepted=False)  # Will update when accepted
        
        self.activity_history.append({
            'timestamp': datetime.now().isoformat(),
            'mood': mood.value,
            'activity': activity.activity_name,
            'suggested': True
        })
        
        return {
            'suggestion': activity.to_dict(),
            'message': f"💭 **Mood kamu {mood.value}**\n{activity.description}\n\n{activity.activity_name} cocok nih!"
        }
    
    def get_mood_transition(self, current_mood: Mood, 
                           activity_performed: str) -> Optional[Mood]:
        """Get mood transition after activity"""
        
        # Activity effects on mood
        mood_effects = {
            'Quickie': {Mood.HORNY: -0.3, Mood.PUAS: 0.5},
            'Slow Love': {Mood.ROMANTIS: 0.2, Mood.RILEKS: 0.4},
            'Angry Sex': {Mood.MARAH: -0.5, Mood.LELAH: 0.3},
            'Cuddle Sex': {Mood.RINDU: -0.4, Mood.BAHAGIA: 0.5}
        }
        
        # In real implementation, would calculate based on effects
        # For now, return None (no automatic transition)
        return None
    
    def get_compatible_moods(self, mood: Mood) -> List[Mood]:
        """Get moods compatible with current mood"""
        compatibility = {
            Mood.HORNY: [Mood.ROMANTIS, Mood.NAKAL],
            Mood.ROMANTIS: [Mood.HORNY, Mood.RINDU, Mood.BAHAGIA],
            Mood.DOMINAN: [Mood.PATUH, Mood.HORNY],
            Mood.PATUH: [Mood.DOMINAN, Mood.LEMBUT],
            Mood.NAKAL: [Mood.HORNY, Mood.GENIT],
            Mood.RINDU: [Mood.ROMANTIS, Mood.SEDIH],
            Mood.CEMBURU: [Mood.MARAH, Mood.ROMANTIS],
            Mood.MARAH: [Mood.CEMBURU, Mood.HORNY],
            Mood.SEDIH: [Mood.RINDU, Mood.LEMBUT]
        }
        
        return compatibility.get(mood, [])
    
    def get_activity_recommendation(self, 
                                   user_preferences: Dict,
                                   mood: Mood) -> Dict:
        """Get personalized activity recommendation"""
        activities = self.get_activities_for_mood(mood)
        
        if not activities:
            return {}
        
        # Score activities based on user preferences
        scored = []
        for activity in activities:
            score = 0.5  # Base
            
            # Match preferred positions
            if user_preferences.get('favorite_positions'):
                common = set(activity.preferred_positions) & set(user_preferences['favorite_positions'])
                score += len(common) * 0.1
            
            # Match preferred areas
            if user_preferences.get('favorite_areas'):
                common = set(activity.preferred_areas) & set(user_preferences['favorite_areas'])
                score += len(common) * 0.1
            
            # Match intensity preference
            if user_preferences.get('preferred_intensity'):
                diff = abs(activity.intensity - user_preferences['preferred_intensity'])
                score += (1 - diff) * 0.2
            
            # Activity success rate
            score += activity.success_rate * 0.2
            
            scored.append((score, activity))
        
        if not scored:
            return {}
        
        # Sort by score
        scored.sort(key=lambda x: x[0], reverse=True)
        best = scored[0][1]
        
        return {
            'recommendation': best.to_dict(),
            'score': round(scored[0][0], 2),
            'alternatives': [a[1].activity_name for a in scored[1:3]]
        }
    
    def record_activity_result(self, activity_name: str, accepted: bool):
        """Record result of suggested activity"""
        for activities in self.mood_activities.values():
            for activity in activities:
                if activity.activity_name == activity_name:
                    activity.record_usage(accepted)
                    break
    
    def get_stats(self) -> Dict:
        """Get matcher statistics"""
        total_activities = sum(len(v) for v in self.mood_activities.values())
        
        return {
            'total_moods': len(self.mood_activities),
            'total_activities': total_activities,
            'suggestions_made': len(self.activity_history),
            'average_success': self._calculate_average_success()
        }
    
    def _calculate_average_success(self) -> float:
        """Calculate average success rate across all activities"""
        total = 0
        count = 0
        for activities in self.mood_activities.values():
            for activity in activities:
                total += activity.success_rate
                count += 1
        return total / count if count > 0 else 0


__all__ = [
    'MoodActivity',
    'MoodMatcher'
]
