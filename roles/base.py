#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
BASE ROLE CLASS
=============================================================================
Semua role mewarisi class ini
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from random import choice, random
from datetime import datetime

from database.enums import Mood


class BaseRole(ABC):
    """
    Base class untuk semua role
    Setiap role punya karakteristik unik
    """
    
    def __init__(self, name: str):
        self.name = name
        self.role_name = self.__class__.__name__.lower()
        
        # Role characteristics
        self.description = ""
        self.personality_traits = {
            'openness': 0.5,
            'conscientiousness': 0.5,
            'extraversion': 0.5,
            'agreeableness': 0.5,
            'neuroticism': 0.5
        }
        self.sensitive_areas = []
        self.clothing_styles = []
        self.greetings = []
        self.secrets = []
        self.memories = []
        
        # Physical attributes (diisi subclass)
        self.physical = self._generate_physical()
        
        # State
        self.current_mood = Mood.CERIA
        self.trust_level = 0.2
        self.secret_count = 0
        self.memory_count = 0
        self.created_at = datetime.now()
        self.last_interaction = datetime.now()
        
        # Stats
        self.total_interactions = 0
        self.total_climax = 0
        self.favorite_areas = []
        self.favorite_positions = []
    
    @abstractmethod
    def _generate_physical(self) -> Dict:
        """Generate physical attributes"""
        pass
    
    @abstractmethod
    def get_intro(self) -> str:
        """Get role-specific introduction"""
        pass
    
    def get_greeting(self) -> str:
        """Get random greeting"""
        if self.greetings:
            return choice(self.greetings).format(name=self.name)
        return f"Halo, aku {self.name}."
    
    def get_sensitive_areas(self) -> List[str]:
        return self.sensitive_areas
    
    def get_clothing(self, location: str = None, mood: Mood = None) -> str:
        if self.clothing_styles:
            return choice(self.clothing_styles)
        return "pakaian biasa"
    
    def get_secret(self) -> Optional[str]:
        if self.secrets and self.trust_level > 0.7:
            self.secret_count += 1
            return choice(self.secrets)
        return None
    
    def get_memory(self) -> Optional[str]:
        if self.memories and self.trust_level > 0.4:
            self.memory_count += 1
            return choice(self.memories)
        return None
    
    def update_trust(self, delta: float):
        self.trust_level += delta
        self.trust_level = max(0.0, min(1.0, self.trust_level))
    
    def update_interaction(self):
        self.total_interactions += 1
        self.last_interaction = datetime.now()
    
    def update_favorite(self, category: str, item: str):
        if category == 'area':
            if item not in self.favorite_areas:
                self.favorite_areas.append(item)
            self.favorite_areas = self.favorite_areas[-5:]
        elif category == 'position':
            if item not in self.favorite_positions:
                self.favorite_positions.append(item)
            self.favorite_positions = self.favorite_positions[-5:]
    
    def get_trust_message(self) -> str:
        if self.trust_level < 0.2:
            return "*menjaga jarak*"
        elif self.trust_level < 0.4:
            return "*mulai nyaman*"
        elif self.trust_level < 0.6:
            return "*tersenyum*"
        elif self.trust_level < 0.8:
            return "*merapat*"
        else:
            return "*sepenuhnya percaya*"
    
    def get_response_modifier(self, context: Dict) -> Dict:
        return {
            'personality_shift': self.personality_traits,
            'sensitive_areas': self.sensitive_areas,
            'trust_level': self.trust_level,
            'trust_message': self.get_trust_message(),
            'secrets_revealed': self.secret_count,
            'memories_shared': self.memory_count,
            'favorite_areas': self.favorite_areas,
            'favorite_positions': self.favorite_positions
        }
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'role': self.role_name,
            'description': self.description,
            'physical': self.physical,
            'trust_level': self.trust_level,
            'secrets_revealed': self.secret_count,
            'memories_shared': self.memory_count,
            'total_interactions': self.total_interactions,
            'total_climax': self.total_climax,
            'favorite_areas': self.favorite_areas,
            'favorite_positions': self.favorite_positions,
            'created_at': self.created_at.isoformat(),
            'last_interaction': self.last_interaction.isoformat()
        }


__all__ = ['BaseRole']
