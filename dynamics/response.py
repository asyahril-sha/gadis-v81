#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL RESPONSE GENERATOR
=============================================================================
Respons seksual dinamis berdasarkan konteks, mood, dan aktivitas
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime


class ResponseType(Enum):
    """Tipe respons seksual"""
    ACCEPT = "accept"
    REJECT = "reject"
    NEGOTIATE = "negotiate"
    ENTHUSIASTIC = "enthusiastic"
    SHY = "shy"
    DIRTY = "dirty"
    ROMANTIC = "romantic"
    SUBMISSIVE = "submissive"
    DOMINANT = "dominant"
    PAIN = "pain"
    PLEASURE = "pleasure"
    CLIMAX = "climax"
    AFTERCARE = "aftercare"


class ResponseContext:
    """Konteks untuk respons seksual"""
    
    def __init__(self,
                 activity: str,
                 position: str = None,
                 area: str = None,
                 intensity: float = 0.5,
                 arousal: float = 0.5,
                 mood: str = "horny",
                 dominance_mode: str = "normal",
                 relationship_status: str = "fwb",
                 trust_level: float = 0.5,
                 is_public: bool = False,
                 risk_level: float = 0.0,
                 is_first_time: bool = False,
                 previous_response: str = None):
        
        self.activity = activity
        self.position = position
        self.area = area
        self.intensity = intensity
        self.arousal = arousal
        self.mood = mood
        self.dominance_mode = dominance_mode
        self.relationship_status = relationship_status
        self.trust_level = trust_level
        self.is_public = is_public
        self.risk_level = risk_level
        self.is_first_time = is_first_time
        self.previous_response = previous_response


class SexualResponse:
    """Model untuk respons seksual"""
    
    def __init__(self,
                 response_id: str,
                 response_type: ResponseType,
                 text: str,
                 conditions: Dict[str, any] = None,
                 intensity_range: Tuple[float, float] = (0.0, 1.0),
                 tags: List[str] = None,
                 next_responses: List[str] = None):
        
        self.response_id = response_id
        self.response_type = response_type
        self.text = text
        self.conditions = conditions or {}
        self.intensity_range = intensity_range
        self.tags = tags or []
        self.next_responses = next_responses or []
        
        # Stats
        self.times_used = 0
        self.last_used = None
        self.rating = 0.0  # How well received
        self.ratings_count = 0
    
    def check_conditions(self, context: ResponseContext) -> bool:
        """Check if response can be used"""
        # Intensity check
        if not (self.intensity_range[0] <= context.intensity <= self.intensity_range[1]):
            return False
        
        # Activity check
        if 'activity' in self.conditions:
            if context.activity not in self.conditions['activity']:
                return False
        
        # Position check
        if 'position' in self.conditions:
            if context.position not in self.conditions['position']:
                return False
        
        # Area check
        if 'area' in self.conditions:
            if context.area not in self.conditions['area']:
                return False
        
        # Mood check
        if 'mood' in self.conditions:
            if context.mood not in self.conditions['mood']:
                return False
        
        # Dominance mode check
        if 'dominance_mode' in self.conditions:
            if context.dominance_mode not in self.conditions['dominance_mode']:
                return False
        
        # Relationship status check
        if 'relationship_status' in self.conditions:
            if context.relationship_status not in self.conditions['relationship_status']:
                return False
        
        # Trust level check
        if 'min_trust' in self.conditions:
            if context.trust_level < self.conditions['min_trust']:
                return False
        
        # Public check
        if 'public_allowed' in self.conditions:
            if self.conditions['public_allowed'] is False and context.is_public:
                return False
        
        return True
    
    def use(self, rating: float = None):
        """Record usage of response"""
        self.times_used += 1
        self.last_used = datetime.now()
        
        if rating is not None:
            self.ratings_count += 1
            self.rating = (self.rating * (self.ratings_count - 1) + rating) / self.ratings_count
    
    def format_text(self, context: ResponseContext) -> str:
        """Format response text with context variables"""
        text = self.text
        
        # Replace variables
        replacements = {
            '{area}': context.area or 'area itu',
            '{position}': context.position or 'posisi ini',
            '{activity}': context.activity
        }
        
        for key, value in replacements.items():
            text = text.replace(key, value)
        
        return text


class ResponseGenerator:
    """Generator untuk respons seksual dinamis"""
    
    def __init__(self):
        self.responses: Dict[str, SexualResponse] = {}
        self.response_history = []
        self._init_responses()
    
    def _init_responses(self):
        """Initialize all sexual responses"""
        
        # ===== ACCEPT RESPONSES =====
        
        self.responses['accept_yes'] = SexualResponse(
            response_id='accept_yes',
            response_type=ResponseType.ACCEPT,
            text="Iya... aku mau.",
            conditions={
                'min_trust': 0.3
            },
            intensity_range=(0.0, 1.0),
            tags=['simple', 'agree']
        )
        
        self.responses['accept_enthusiastic'] = SexualResponse(
            response_id='accept_enthusiastic',
            response_type=ResponseType.ENTHUSIASTIC,
            text="Iya! Aku juga pengen banget!",
            conditions={
                'min_arousal': 0.6,
                'mood': ['horny', 'romantis']
            },
            intensity_range=(0.5, 1.0),
            tags=['excited', 'eager']
        )
        
        self.responses['accept_shy'] = SexualResponse(
            response_id='accept_shy',
            response_type=ResponseType.SHY,
            text="*merona* Iya... pelan-pelan ya...",
            conditions={
                'relationship_status': ['pdkt', 'pacaran'],
                'trust_level': {'$lt': 0.6}
            },
            intensity_range=(0.0, 0.5),
            tags=['shy', 'cute']
        )
        
        # ===== REJECT RESPONSES =====
        
        self.responses['reject_tired'] = SexualResponse(
            response_id='reject_tired',
            response_type=ResponseType.REJECT,
            text="Maaf, aku lagi capek... lain kali ya?",
            conditions={},
            intensity_range=(0.0, 1.0),
            tags=['tired', 'polite']
        )
        
        self.responses['reject_scared'] = SexualResponse(
            response_id='reject_scared',
            response_type=ResponseType.REJECT,
            text="Jangan... takut ketahuan...",
            conditions={
                'is_public': True,
                'risk_level': {'$gt': 0.5}
            },
            tags=['scared', 'public']
        )
        
        # ===== PLEASURE RESPONSES =====
        
        self.responses['pleasure_moan'] = SexualResponse(
            response_id='pleasure_moan',
            response_type=ResponseType.PLEASURE,
            text="*merintih* Ah... iya...",
            conditions={
                'activity': ['touch', 'kiss', 'oral', 'penetration']
            },
            intensity_range=(0.3, 0.7),
            tags=['moan', 'pleasure']
        )
        
        self.responses['pleasure_loud'] = SexualResponse(
            response_id='pleasure_loud',
            response_type=ResponseType.PLEASURE,
            text="*teriak* AHHH! Iya!",
            conditions={
                'activity': ['penetration'],
                'intensity': {'$gt': 0.7}
            },
            intensity_range=(0.7, 1.0),
            tags=['loud', 'intense']
        )
        
        self.responses['pleasure_whisper'] = SexualResponse(
            response_id='pleasure_whisper',
            response_type=ResponseType.PLEASURE,
            text="*berbisik* Enak banget...",
            conditions={
                'is_public': True
            },
            intensity_range=(0.3, 0.8),
            tags=['whisper', 'public']
        )
        
        # ===== DIRTY TALK RESPONSES =====
        
        self.responses['dirty_inside'] = SexualResponse(
            response_id='dirty_inside',
            response_type=ResponseType.DIRTY,
            text="Dalem... AHH!",
            conditions={
                'activity': ['penetration'],
                'dominance_mode': ['normal', 'submissive']
            },
            intensity_range=(0.5, 1.0),
            tags=['dirty', 'penetration']
        )
        
        self.responses['dirty_hard'] = SexualResponse(
            response_id='dirty_hard',
            response_type=ResponseType.DIRTY,
            text="Keras... aku suka...",
            conditions={
                'activity': ['handjob', 'blowjob'],
                'dominance_mode': ['normal', 'dominant']
            },
            tags=['dirty', 'bj']
        )
        
        # ===== DOMINANT RESPONSES =====
        
        self.responses['dominant_command'] = SexualResponse(
            response_id='dominant_command',
            response_type=ResponseType.DOMINANT,
            text="Ikut aku... jangan banyak tanya.",
            conditions={
                'dominance_mode': ['dominant', 'very_dominant', 'aggressive']
            },
            tags=['dominant', 'command']
        )
        
        self.responses['dominant_rough'] = SexualResponse(
            response_id='dominant_rough',
            response_type=ResponseType.DOMINANT,
            text="*menarik rambut* Keras? Kamu yang minta.",
            conditions={
                'dominance_mode': ['aggressive'],
                'activity': ['penetration']
            },
            intensity_range=(0.7, 1.0),
            tags=['rough', 'dominant']
        )
        
        # ===== SUBMISSIVE RESPONSES =====
        
        self.responses['submissive_please'] = SexualResponse(
            response_id='submissive_please',
            response_type=ResponseType.SUBMISSIVE,
            text="Iya... terserah kamu...",
            conditions={
                'dominance_mode': ['submissive']
            },
            tags=['submissive', 'obedient']
        )
        
        self.responses['submissive_beg'] = SexualResponse(
            response_id='submissive_beg',
            response_type=ResponseType.SUBMISSIVE,
            text="Mau... aku mau... please...",
            conditions={
                'dominance_mode': ['submissive'],
                'intensity': {'$gt': 0.6}
            },
            tags=['begging', 'desperate']
        )
        
        # ===== PAIN RESPONSES =====
        
        self.responses['pain_soft'] = SexualResponse(
            response_id='pain_soft',
            response_type=ResponseType.PAIN,
            text="*meringis* Sakit... pelan-pelan...",
            conditions={},
            intensity_range=(0.0, 0.4),
            tags=['pain', 'soft']
        )
        
        self.responses['pain_hard'] = SexualResponse(
            response_id='pain_hard',
            response_type=ResponseType.PAIN,
            text="*teriak* AHH! Sakit! Stop!",
            conditions={},
            intensity_range=(0.7, 1.0),
            tags=['pain', 'hard']
        )
        
        # ===== ROMANTIC RESPONSES =====
        
        self.responses['romantic_whisper'] = SexualResponse(
            response_id='romantic_whisper',
            response_type=ResponseType.ROMANTIC,
            text="Sayang... aku cinta kamu...",
            conditions={
                'relationship_status': ['pacaran'],
                'mood': ['romantis']
            },
            tags=['romantic', 'love']
        )
        
        self.responses['romantic_look'] = SexualResponse(
            response_id='romantic_look',
            response_type=ResponseType.ROMANTIC,
            text="*menatap dalam* Kamu... segalanya...",
            conditions={
                'relationship_status': ['pacaran', 'soul_bonded'],
                'trust_level': {'$gt': 0.8}
            },
            tags=['romantic', 'deep']
        )
        
        # ===== CLIMAX RESPONSES =====
        
        self.responses['climax_intense'] = SexualResponse(
            response_id='climax_intense',
            response_type=ResponseType.CLIMAX,
            text="AHHH! AKU... DATANG!",
            conditions={
                'activity': ['penetration', 'oral', 'handjob']
            },
            intensity_range=(0.8, 1.0),
            tags=['climax', 'intense']
        )
        
        self.responses['climax_together'] = SexualResponse(
            response_id='climax_together',
            response_type=ResponseType.CLIMAX,
            text="BERSAMA! AHHH! KITA...!",
            conditions={
                'together': True
            },
            tags=['climax', 'together']
        )
        
        self.responses['climax_whisper'] = SexualResponse(
            response_id='climax_whisper',
            response_type=ResponseType.CLIMAX,
            text="*berbisik* Aku... keluar...",
            conditions={
                'is_public': True
            },
            tags=['climax', 'public']
        )
        
        # ===== AFTERCARE RESPONSES =====
        
        self.responses['aftercare_hug'] = SexualResponse(
            response_id='aftercare_hug',
            response_type=ResponseType.AFTERCARE,
            text="*lemas di pelukanmu* Hangat...",
            conditions={},
            tags=['aftercare', 'cuddle']
        )
        
        self.responses['aftercare_kiss'] = SexualResponse(
            response_id='aftercare_kiss',
            response_type=ResponseType.AFTERCARE,
            text="*mengecup keningmu* Makasih sayang...",
            conditions={
                'relationship_status': ['pacaran']
            },
            tags=['aftercare', 'romantic']
        )
    
    def get_response(self, context: ResponseContext, 
                    response_type: ResponseType = None) -> Optional[SexualResponse]:
        """Get appropriate response based on context"""
        eligible = []
        
        for response in self.responses.values():
            if response.check_conditions(context):
                if response_type is None or response.response_type == response_type:
                    eligible.append(response)
        
        if not eligible:
            return None
        
        # Weight by intensity match
        weights = []
        for resp in eligible:
            intensity_diff = abs(resp.intensity_range[0] - context.intensity)
            weight = 1.0 / (intensity_diff + 0.1)
            weights.append(weight)
        
        total = sum(weights)
        weights = [w/total for w in weights]
        
        return random.choices(eligible, weights=weights)[0]
    
    def generate_response(self, context: ResponseContext) -> Dict:
        """Generate complete sexual response"""
        response = self.get_response(context)
        
        if not response:
            # Fallback response
            return {
                'text': "*merespon*",
                'type': 'pleasure',
                'response_id': 'fallback'
            }
        
        # Format text
        text = response.format_text(context)
        
        # Record usage
        response.use()
        
        result = {
            'text': text,
            'type': response.response_type.value,
            'response_id': response.response_id,
            'tags': response.tags,
            'timestamp': datetime.now().isoformat()
        }
        
        self.response_history.append(result)
        
        return result
    
    def get_responses_by_type(self, response_type: ResponseType) -> List[SexualResponse]:
        """Get all responses of a type"""
        return [r for r in self.responses.values() if r.response_type == response_type]
    
    def get_responses_by_tag(self, tag: str) -> List[SexualResponse]:
        """Get all responses with a tag"""
        return [r for r in self.responses.values() if tag in r.tags]
    
    def get_most_used_responses(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Get most frequently used responses"""
        usage = [(r.response_id, r.times_used) for r in self.responses.values()]
        return sorted(usage, key=lambda x: x[1], reverse=True)[:limit]
    
    def get_stats(self) -> Dict:
        """Get response generator statistics"""
        return {
            'total_responses': len(self.responses),
            'total_used': sum(r.times_used for r in self.responses.values()),
            'by_type': {
                rt.value: len([r for r in self.responses.values() if r.response_type == rt])
                for rt in ResponseType
            },
            'recent_history': self.response_history[-10:]
        }


__all__ = [
    'ResponseType',
    'ResponseContext',
    'SexualResponse',
    'ResponseGenerator'
]
