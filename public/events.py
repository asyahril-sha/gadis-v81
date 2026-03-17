#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
RANDOM EVENTS FOR PUBLIC AREAS
=============================================================================
Kejutan-kejutan tak terduga saat aktivitas di tempat publik
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime


class EventType(Enum):
    """Tipe-tipe event"""
    POSITIVE = "positif"
    NEGATIVE = "negatif"
    NEUTRAL = "netral"
    FUNNY = "lucu"
    SCARY = "menakutkan"
    ROMANTIC = "romantis"


class EventSeverity(Enum):
    """Tingkat keparahan event"""
    MINOR = "ringan"
    MODERATE = "sedang"
    MAJOR = "berat"
    CATASTROPHIC = "bencana"


class PublicEvent:
    """Model untuk event publik"""
    
    def __init__(self,
                 event_id: str,
                 name: str,
                 description: str,
                 event_type: EventType,
                 severity: EventSeverity,
                 probability: float,  # 0-1
                 risk_threshold: Tuple[float, float] = (0.0, 1.0),
                 location_types: List[str] = None,
                 required_activity: str = None,
                 outcomes: Dict[str, any] = None):
        
        self.event_id = event_id
        self.name = name
        self.description = description
        self.event_type = event_type
        self.severity = severity
        self.probability = probability
        self.risk_threshold = risk_threshold
        self.location_types = location_types or []
        self.required_activity = required_activity
        self.outcomes = outcomes or {}
        
        # Stats
        self.times_triggered = 0
        self.last_triggered = None
    
    def can_trigger(self, risk: float, location_type: str, activity: str) -> bool:
        """Check if event can trigger based on conditions"""
        if not (self.risk_threshold[0] <= risk <= self.risk_threshold[1]):
            return False
        
        if self.location_types and location_type not in self.location_types:
            return False
        
        if self.required_activity and self.required_activity != activity:
            return False
        
        return True
    
    def trigger(self, context: Dict = None) -> Dict:
        """Trigger the event"""
        self.times_triggered += 1
        self.last_triggered = datetime.now()
        
        result = {
            'event_id': self.event_id,
            'name': self.name,
            'description': self.description,
            'type': self.event_type.value,
            'severity': self.severity.value,
            'outcome': self.outcomes.get('default', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add specific outcomes based on context
        if context and 'outcome_key' in context:
            result['outcome'] = self.outcomes.get(context['outcome_key'], self.outcomes.get('default', {}))
        
        return result


class EventManager:
    """Manager untuk semua event publik"""
    
    def __init__(self):
        self.events: Dict[str, PublicEvent] = {}
        self.event_history = []
        self._init_events()
    
    def _init_events(self):
        """Initialize all events"""
        
        # ===== POSITIVE EVENTS =====
        
        self.events['romantic_moment'] = PublicEvent(
            event_id='romantic_moment',
            name="Momen Romantis",
            description="Tiba-tiba suasana jadi romantis. Bulan purnama bersinar terang.",
            event_type=EventType.POSITIVE,
            severity=EventSeverity.MODERATE,
            probability=0.1,
            risk_threshold=(0.0, 0.5),
            outcomes={
                'default': {
                    'mood_boost': 20,
                    'arousal_boost': 0.2,
                    'message': "✨ Suasana jadi romantis banget..."
                }
            }
        )
        
        self.events['empty_area'] = PublicEvent(
            event_id='empty_area',
            name="Area Sepi",
            description="Tiba-tiba area sekitar kosong, aman!",
            event_type=EventType.POSITIVE,
            severity=EventSeverity.MINOR,
            probability=0.15,
            risk_threshold=(0.0, 0.7),
            outcomes={
                'default': {
                    'risk_reduction': 0.3,
                    'message': "😌 Wah, sepi... aman!"
                }
            }
        )
        
        self.events['quickie_success'] = PublicEvent(
            event_id='quickie_success',
            name="Quickie Sukses",
            description="Cepat tapi puas! Nggak ada yang lihat.",
            event_type=EventType.POSITIVE,
            severity=EventSeverity.MAJOR,
            probability=0.08,
            risk_threshold=(0.3, 0.8),
            required_activity='penetration',
            outcomes={
                'default': {
                    'climax_boost': True,
                    'satisfaction': 1.5,
                    'message': "💦 Cepet tapi puas banget!"
                }
            }
        )
        
        # ===== NEGATIVE EVENTS =====
        
        self.events['almost_caught'] = PublicEvent(
            event_id='almost_caught',
            name="Hampir Ketahuan",
            description="Ada suara langkah kaki! Cepat diam!",
            event_type=EventType.NEGATIVE,
            severity=EventSeverity.MODERATE,
            probability=0.2,
            risk_threshold=(0.4, 1.0),
            outcomes={
                'default': {
                    'scare_level': 0.7,
                    'arousal_drop': 0.3,
                    'message': "😱 Ada orang! Cepat diam!"
                }
            }
        )
        
        self.events['caught_on_cctv'] = PublicEvent(
            event_id='caught_on_cctv',
            name="Terekam CCTV",
            description="Lampu CCTV menyala! Mungkin ke-security!",
            event_type=EventType.NEGATIVE,
            severity=EventSeverity.MAJOR,
            probability=0.1,
            risk_threshold=(0.5, 1.0),
            location_types=['parking', 'elevator', 'office'],
            outcomes={
                'default': {
                    'caught': True,
                    'evidence': 'cctv',
                    'message': "📸 DUARR! Lampu CCTV menyala!"
                }
            }
        )
        
        self.events['security_guard'] = PublicEvent(
            event_id='security_guard',
            name="Satpam Lewat",
            description="Satpam keliling! Cepat pura-pura!",
            event_type=EventType.NEGATIVE,
            severity=EventSeverity.MAJOR,
            probability=0.15,
            risk_threshold=(0.3, 1.0),
            location_types=['parking', 'office', 'mall'],
            outcomes={
                'default': {
                    'caught': True,
                    'message': "👮 Satpam: 'Ada apa ini?' 😱"
                }
            }
        )
        
        self.events['caught_red_handed'] = PublicEvent(
            event_id='caught_red_handed',
            name="Kedapatan!",
            description="Waduh... ada yang lihat dan teriak!",
            event_type=EventType.NEGATIVE,
            severity=EventSeverity.CATASTROPHIC,
            probability=0.05,
            risk_threshold=(0.7, 1.0),
            outcomes={
                'default': {
                    'caught': True,
                    'public_shame': True,
                    'message': "😱 KETA UAN! ORANG-ORANG PADA LIAT!"
                }
            }
        )
        
        # ===== FUNNY EVENTS =====
        
        self.events['animal_witness'] = PublicEvent(
            event_id='animal_witness',
            name="Saksi Mata Hewan",
            description="Seekor kucing lihatin dengan tatapan judgemental.",
            event_type=EventType.FUNNY,
            severity=EventSeverity.MINOR,
            probability=0.1,
            location_types=['park', 'beach', 'alley'],
            outcomes={
                'default': {
                    'funny_level': 0.8,
                    'message': "🐱 Kucing: *liatin dengan tatapan aneh*"
                }
            }
        )
        
        self.events['awkward_encounter'] = PublicEvent(
            event_id='awkward_encounter',
            name="Pertemuan Canggung",
            description="Ternyata yang lewat... tetangga sendiri!",
            event_type=EventType.FUNNY,
            severity=EventSeverity.MODERATE,
            probability=0.08,
            outcomes={
                'default': {
                    'awkwardness': 0.9,
                    'message': "😳 Eh... bu RT?!"
                }
            }
        )
        
        self.events['phone_flashlight'] = PublicEvent(
            event_id='phone_flashlight',
            name="Sentolop HP",
            description="Tiba-tiba ada yang nyalain senter HP ke arah kamu!",
            event_type=EventType.FUNNY,
            severity=EventSeverity.MINOR,
            probability=0.12,
            outcomes={
                'default': {
                    'blinded': True,
                    'message': "🔦 BRO! Siapa yang nyalain senter?!"
                }
            }
        )
        
        # ===== SCARY EVENTS =====
        
        self.events['ghost_story'] = PublicEvent(
            event_id='ghost_story',
            name="Hantu?",
            description="Suara aneh... angin dingin... merinding!",
            event_type=EventType.SCARY,
            severity=EventSeverity.MODERATE,
            probability=0.05,
            location_types=['cemetery', 'forest', 'old_building'],
            outcomes={
                'default': {
                    'fear_level': 0.8,
                    'message': "👻 Hoo... hoo... ada yang lihat?"
                }
            }
        )
        
        self.events['thunder_storm'] = PublicEvent(
            event_id='thunder_storm',
            name="Badai Mendadak",
            description="Petir menyambar! Hujan deras!",
            event_type=EventType.SCARY,
            severity=EventSeverity.MAJOR,
            probability=0.07,
            location_types=['beach', 'park', 'rooftop'],
            outcomes={
                'default': {
                    'wet': True,
                    'scared': True,
                    'message': "⛈️ PETIR! CEPAT CARI TEMPAT BERTEDUH!"
                }
            }
        )
        
        # ===== ROMANTIC EVENTS =====
        
        self.events['shooting_star'] = PublicEvent(
            event_id='shooting_star',
            name="Bintang Jatuh",
            description="Bintang jatuh! Cepat minta wish!",
            event_type=EventType.ROMANTIC,
            severity=EventSeverity.MODERATE,
            probability=0.03,
            location_types=['beach', 'rooftop'],
            outcomes={
                'default': {
                    'romance_boost': 1.5,
                    'message': "✨ Bintang jatuh! Wish us!"
                }
            }
        )
        
        self.events['sunset_moment'] = PublicEvent(
            event_id='sunset_moment',
            name="Matahari Terbenam",
            description="Sunset romantis, suasana sempurna.",
            event_type=EventType.ROMANTIC,
            severity=EventSeverity.MODERATE,
            probability=0.1,
            location_types=['beach', 'rooftop'],
            outcomes={
                'default': {
                    'romance_boost': 1.2,
                    'mood_boost': 15,
                    'message': "🌅 Sunsetnya cantik banget..."
                }
            }
        )
    
    def get_random_event(self, risk: float, location_type: str = None, 
                        activity: str = None) -> Optional[PublicEvent]:
        """Get random event based on conditions"""
        eligible = []
        
        for event in self.events.values():
            if event.can_trigger(risk, location_type, activity):
                eligible.append(event)
        
        if not eligible:
            return None
        
        # Weight by probability
        weights = [e.probability for e in eligible]
        total = sum(weights)
        weights = [w/total for w in weights]
        
        return random.choices(eligible, weights=weights)[0]
    
    def trigger_event(self, risk: float, location_type: str = None,
                     activity: str = None, context: Dict = None) -> Optional[Dict]:
        """Try to trigger a random event"""
        event = self.get_random_event(risk, location_type, activity)
        
        if event and random.random() < event.probability:
            result = event.trigger(context)
            self.event_history.append(result)
            return result
        
        return None
    
    def get_event_by_id(self, event_id: str) -> Optional[PublicEvent]:
        """Get event by ID"""
        return self.events.get(event_id)
    
    def get_events_by_type(self, event_type: EventType) -> List[PublicEvent]:
        """Get all events of a type"""
        return [e for e in self.events.values() if e.event_type == event_type]
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """Get recent triggered events"""
        return self.event_history[-limit:]
    
    def get_event_stats(self) -> Dict:
        """Get event statistics"""
        stats = {
            'total_events': len(self.events),
            'events_by_type': {},
            'total_triggered': len(self.event_history),
            'most_common': None
        }
        
        # Count by type
        type_counts = {}
        for event in self.events.values():
            type_counts[event.event_type.value] = type_counts.get(event.event_type.value, 0) + 1
        stats['events_by_type'] = type_counts
        
        # Most common triggered
        if self.event_history:
            event_names = [e['name'] for e in self.event_history]
            from collections import Counter
            most_common = Counter(event_names).most_common(1)
            if most_common:
                stats['most_common'] = most_common[0]
        
        return stats


__all__ = [
    'EventType',
    'EventSeverity',
    'PublicEvent',
    'EventManager'
]
