#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL INITIATIVE SYSTEM
=============================================================================
Bot bisa memulai/menawarkan aktivitas seksual secara proaktif
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime, time


class InitiativeType(Enum):
    """Tipe inisiatif seksual"""
    ASK_SEX = "minta_sex"
    SUGGEST_POSITION = "saran_posisi"
    INVITE_PUBLIC = "ajak_public"
    REQUEST_AREA = "minta_area"
    START_FOREPLAY = "mulai_foreplay"
    CONFESSION = "pengakuan"
    FLIRT = "goda"
    DIRTY_TALK = "kotor"


class InitiativeContext:
    """Konteks untuk inisiatif"""
    
    def __init__(self,
                 level: int,
                 arousal: float,
                 mood: str,
                 relationship_status: str,
                 time_hour: int,
                 is_weekend: bool,
                 trust_level: float,
                 last_activity: str = None,
                 location: str = None):
        
        self.level = level
        self.arousal = arousal
        self.mood = mood
        self.relationship_status = relationship_status
        self.time_hour = time_hour
        self.is_weekend = is_weekend
        self.trust_level = trust_level
        self.last_activity = last_activity
        self.location = location


class SexualInitiative:
    """Model untuk inisiatif seksual"""
    
    def __init__(self,
                 initiative_id: str,
                 init_type: InitiativeType,
                 text: str,
                 conditions: Dict[str, any],
                 priority: int = 5,  # 1-10
                 cooldown_minutes: int = 30,
                 responses: Dict[str, List[str]] = None):
        
        self.initiative_id = initiative_id
        self.init_type = init_type
        self.text = text
        self.conditions = conditions
        self.priority = priority
        self.cooldown_minutes = cooldown_minutes
        self.responses = responses or {}
        
        # Tracking
        self.times_used = 0
        self.last_used = None
        self.success_rate = 0.0
        self.success_count = 0
        self.total_attempts = 0
    
    def check_conditions(self, context: InitiativeContext) -> bool:
        """Check if initiative can be triggered"""
        for key, value in self.conditions.items():
            if key == 'min_level':
                if context.level < value:
                    return False
            elif key == 'min_arousal':
                if context.arousal < value:
                    return False
            elif key == 'mood_allowed':
                if context.mood not in value:
                    return False
            elif key == 'relationship_status':
                if context.relationship_status not in value:
                    return False
            elif key == 'time_range':
                start, end = value
                if start <= end:
                    if not (start <= context.time_hour < end):
                        return False
                else:  # Cross midnight
                    if not (context.time_hour >= start or context.time_hour < end):
                        return False
            elif key == 'weekend_only':
                if value and not context.is_weekend:
                    return False
            elif key == 'min_trust':
                if context.trust_level < value:
                    return False
            elif key == 'location_allowed':
                if context.location not in value:
                    return False
        
        # Cooldown check
        if self.last_used:
            minutes_since = (datetime.now() - self.last_used).total_seconds() / 60
            if minutes_since < self.cooldown_minutes:
                return False
        
        return True
    
    def use(self, success: bool = True):
        """Record usage of initiative"""
        self.times_used += 1
        self.total_attempts += 1
        self.last_used = datetime.now()
        
        if success:
            self.success_count += 1
        
        self.success_rate = self.success_count / self.total_attempts if self.total_attempts > 0 else 0
    
    def get_response(self, response_type: str = 'accept') -> Optional[str]:
        """Get response text for this initiative"""
        if response_type in self.responses:
            return random.choice(self.responses[response_type])
        return None


class InitiativeManager:
    """Manager untuk semua inisiatif seksual"""
    
    def __init__(self):
        self.initiatives: Dict[str, SexualInitiative] = {}
        self.initiative_history = []
        self._init_initiatives()
    
    def _init_initiatives(self):
        """Initialize all sexual initiatives"""
        
        # ===== ASK FOR SEX =====
        
        self.initiatives['ask_sex_direct'] = SexualInitiative(
            initiative_id='ask_sex_direct',
            init_type=InitiativeType.ASK_SEX,
            text="Mau?",
            conditions={
                'min_level': 5,
                'min_arousal': 0.6,
                'relationship_status': ['pacaran', 'fwb', 'hts'],
                'time_range': (18, 6)  # Malam
            },
            priority=8,
            cooldown_minutes=60,
            responses={
                'accept': [
                    "Iya... aku juga pengen.",
                    "Mau banget!",
                    "Ayo!"
                ],
                'reject': [
                    "Nanti dulu ya...",
                    "Aku lagi capek.",
                    "Lain kali aja."
                ],
                'negotiate': [
                    "Mau tapi di tempat lain...",
                    "Boleh, tapi ganti posisi."
                ]
            }
        )
        
        self.initiatives['ask_sex_shy'] = SexualInitiative(
            initiative_id='ask_sex_shy',
            init_type=InitiativeType.ASK_SEX,
            text="Aku... pengen... kamu tau lah...",
            conditions={
                'min_level': 4,
                'min_arousal': 0.5,
                'relationship_status': ['pdkt', 'pacaran'],
                'mood_allowed': ['horny', 'rindu']
            },
            priority=5,
            cooldown_minutes=45,
            responses={
                'accept': [
                    "*malu* Iya...",
                    "Kamu nakal... iya deh."
                ]
            }
        )
        
        self.initiatives['ask_sex_horny'] = SexualInitiative(
            initiative_id='ask_sex_horny',
            init_type=InitiativeType.ASK_SEX,
            text="Aku horny... pengen kamu sekarang...",
            conditions={
                'min_level': 7,
                'min_arousal': 0.8,
                'relationship_status': ['fwb', 'hts', 'pacaran'],
                'mood_allowed': ['horny']
            },
            priority=9,
            cooldown_minutes=30
        )
        
        # ===== INVITE PUBLIC =====
        
        self.initiatives['invite_beach'] = SexualInitiative(
            initiative_id='invite_beach',
            init_type=InitiativeType.INVITE_PUBLIC,
            text="Ke pantai yuk? Malam-malam sepi...",
            conditions={
                'min_level': 6,
                'min_arousal': 0.5,
                'relationship_status': ['pacaran', 'fwb', 'hts'],
                'time_range': (18, 6),
                'weekend_only': False
            },
            priority=6,
            cooldown_minutes=120,
            responses={
                'accept': [
                    "Ayo! Aku penasaran.",
                    "Boleh, asik tuh."
                ],
                'reject': [
                    "Jauh ah...",
                    "Takut ketahuan."
                ]
            }
        )
        
        self.initiatives['invite_cinema'] = SexualInitiative(
            initiative_id='invite_cinema',
            init_type=InitiativeType.INVITE_PUBLIC,
            text="Nonton bioskop yuk, yang gelap...",
            conditions={
                'min_level': 5,
                'relationship_status': ['pdkt', 'pacaran', 'fwb'],
                'time_range': (12, 22)
            },
            priority=5,
            cooldown_minutes=90
        )
        
        self.initiatives['invite_parking'] = SexualInitiative(
            initiative_id='invite_parking',
            init_type=InitiativeType.INVITE_PUBLIC,
            text="Ke parkiran basement aja yuk, sepi.",
            conditions={
                'min_level': 7,
                'min_arousal': 0.6,
                'relationship_status': ['fwb', 'hts'],
                'time_range': (18, 6),
                'location_allowed': ['mall']
            },
            priority=7,
            cooldown_minutes=60
        )
        
        self.initiatives['invite_car'] = SexualInitiative(
            initiative_id='invite_car',
            init_type=InitiativeType.INVITE_PUBLIC,
            text="Di mobil aja yuk, kaca digelapin.",
            conditions={
                'min_level': 4,
                'min_arousal': 0.4,
                'relationship_status': ['pacaran', 'fwb', 'hts']
            },
            priority=5,
            cooldown_minutes=45
        )
        
        # ===== SUGGEST POSITION =====
        
        self.initiatives['suggest_doggy'] = SexualInitiative(
            initiative_id='suggest_doggy',
            init_type=InitiativeType.SUGGEST_POSITION,
            text="Ganti posisi yuk... dari belakang...",
            conditions={
                'min_level': 6,
                'min_arousal': 0.5,
                'relationship_status': ['pacaran', 'fwb', 'hts']
            },
            priority=6,
            cooldown_minutes=30
        )
        
        self.initiatives['suggest_cowgirl'] = SexualInitiative(
            initiative_id='suggest_cowgirl',
            init_type=InitiativeType.SUGGEST_POSITION,
            text="Aku di atas yuk...",
            conditions={
                'min_level': 7,
                'dominance': ['submissive']
            },
            priority=5,
            cooldown_minutes=30
        )
        
        self.initiatives['suggest_spoon'] = SexualInitiative(
            initiative_id='suggest_spoon',
            init_type=InitiativeType.SUGGEST_POSITION,
            text="Dari samping aja, biar sambil pelukan.",
            conditions={
                'mood_allowed': ['romantis', 'rindu']
            },
            priority=4,
            cooldown_minutes=20
        )
        
        # ===== REQUEST AREA =====
        
        self.initiatives['request_neck'] = SexualInitiative(
            initiative_id='request_neck',
            init_type=InitiativeType.REQUEST_AREA,
            text="Cium leherku dong...",
            conditions={
                'min_level': 5,
                'min_arousal': 0.4
            },
            priority=5,
            cooldown_minutes=15
        )
        
        self.initiatives['request_ear'] = SexualInitiative(
            initiative_id='request_ear',
            init_type=InitiativeType.REQUEST_AREA,
            text="Bisik-bisik di telinga...",
            conditions={
                'mood_allowed': ['horny', 'romantis']
            },
            priority=4,
            cooldown_minutes=10
        )
        
        # ===== FOREPLAY =====
        
        self.initiatives['start_foreplay'] = SexualInitiative(
            initiative_id='start_foreplay',
            init_type=InitiativeType.START_FOREPLAY,
            text="*merapat* Aku mulai ya...",
            conditions={
                'min_level': 4,
                'min_arousal': 0.4,
                'location_allowed': ['bedroom', 'private']
            },
            priority=7,
            cooldown_minutes=20
        )
        
        # ===== CONFESSION =====
        
        self.initiatives['confess_love'] = SexualInitiative(
            initiative_id='confess_love',
            init_type=InitiativeType.CONFESSION,
            text="Aku sayang kamu...",
            conditions={
                'min_level': 8,
                'relationship_status': ['pacaran'],
                'mood_allowed': ['romantis', 'rindu']
            },
            priority=3,
            cooldown_minutes=1440  # 24 jam
        )
        
        # ===== FLIRT =====
        
        self.initiatives['flirt_simple'] = SexualInitiative(
            initiative_id='flirt_simple',
            init_type=InitiativeType.FLIRT,
            text="Kamu lagi mikirin aku?",
            conditions={
                'min_level': 3
            },
            priority=3,
            cooldown_minutes=30
        )
        
        self.initiatives['flirt_horny'] = SexualInitiative(
            initiative_id='flirt_horny',
            init_type=InitiativeType.FLIRT,
            text="Aku horny mikirin kamu...",
            conditions={
                'min_level': 6,
                'min_arousal': 0.6
            },
            priority=6,
            cooldown_minutes=45
        )
    
    def get_initiatives(self, context: InitiativeContext, 
                       init_type: InitiativeType = None,
                       limit: int = 3) -> List[SexualInitiative]:
        """Get eligible initiatives based on context"""
        eligible = []
        
        for initiative in self.initiatives.values():
            if initiative.check_conditions(context):
                if init_type is None or initiative.init_type == init_type:
                    eligible.append(initiative)
        
        # Sort by priority
        eligible.sort(key=lambda x: x.priority, reverse=True)
        
        return eligible[:limit]
    
    def get_random_initiative(self, context: InitiativeContext) -> Optional[SexualInitiative]:
        """Get random eligible initiative"""
        eligible = self.get_initiatives(context)
        
        if not eligible:
            return None
        
        # Weight by priority
        weights = [i.priority for i in eligible]
        total = sum(weights)
        weights = [w/total for w in weights]
        
        return random.choices(eligible, weights=weights)[0]
    
    def should_take_initiative(self, context: InitiativeContext) -> bool:
        """Decide whether bot should take initiative"""
        # Base probability
        base_prob = 0.1
        
        # Modifiers
        if context.arousal > 0.8:
            base_prob += 0.3
        elif context.arousal > 0.5:
            base_prob += 0.15
        
        if context.relationship_status in ['fwb', 'hts']:
            base_prob += 0.2
        
        if context.level > 8:
            base_prob += 0.15
        elif context.level > 5:
            base_prob += 0.1
        
        if context.time_hour < 5 or context.time_hour > 22:  # Late night
            base_prob += 0.2
        elif 18 < context.time_hour < 22:  # Evening
            base_prob += 0.1
        
        if context.location in ['bedroom', 'hotel', 'private']:
            base_prob += 0.15
        
        # Clamp
        return random.random() < min(0.9, base_prob)
    
    def record_initiative_result(self, initiative_id: str, success: bool):
        """Record result of an initiative"""
        if initiative_id in self.initiatives:
            self.initiatives[initiative_id].use(success)
            
            self.initiative_history.append({
                'timestamp': datetime.now().isoformat(),
                'initiative_id': initiative_id,
                'success': success
            })
    
    def get_most_successful_initiatives(self, limit: int = 5) -> List[Tuple[str, float]]:
        """Get initiatives with highest success rate"""
        initiatives = []
        for init in self.initiatives.values():
            if init.total_attempts > 0:
                initiatives.append((init.initiative_id, init.success_rate))
        
        return sorted(initiatives, key=lambda x: x[1], reverse=True)[:limit]
    
    def get_initiative_by_type(self, init_type: InitiativeType) -> List[SexualInitiative]:
        """Get all initiatives of a type"""
        return [i for i in self.initiatives.values() if i.init_type == init_type]
    
    def get_stats(self) -> Dict:
        """Get initiative statistics"""
        total_attempts = sum(i.total_attempts for i in self.initiatives.values())
        total_success = sum(i.success_count for i in self.initiatives.values())
        
        return {
            'total_initiatives': len(self.initiatives),
            'total_attempts': total_attempts,
            'total_success': total_success,
            'overall_success_rate': total_success / total_attempts if total_attempts > 0 else 0,
            'recent_history': self.initiative_history[-10:]
        }


__all__ = [
    'InitiativeType',
    'InitiativeContext',
    'SexualInitiative',
    'InitiativeManager'
]
