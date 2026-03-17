#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
DATABASE MODELS (TANPA SQLALCHEMY)
=============================================================================
Menggunakan dataclasses biasa, bukan SQLAlchemy
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List, Any
from enum import Enum


class DominanceLevel(Enum):
    """Enum untuk dominance level"""
    NORMAL = "normal"
    DOMINANT = "dominant"
    SUBMISSIVE = "submissive"
    SWITCH = "switch"
    
    @classmethod
    def from_string(cls, value: str):
        """Convert string to enum"""
        try:
            return cls(value.lower())
        except ValueError:
            return cls.NORMAL
    
    @classmethod
    def values(cls):
        """Get all values"""
        return [item.value for item in cls]


class RelationshipStage(Enum):
    """Enum untuk relationship stages"""
    STRANGER = "stranger"
    FRIEND = "friend"
    CLOSE_FRIEND = "close_friend"
    LOVER = "lover"
    PARTNER = "partner"
    MARRIED = "married"
    
    @classmethod
    def from_string(cls, value: str):
        """Convert string to enum"""
        try:
            return cls(value.lower())
        except ValueError:
            return cls.STRANGER


class RelationshipStatus(Enum):
    """Enum untuk relationship status"""
    PDKT = "pdkt"
    SINGLE = "single"
    COMPLICATED = "complicated"
    EXCLUSIVE = "exclusive"
    
    @classmethod
    def from_string(cls, value: str):
        """Convert string to enum"""
        try:
            return cls(value.lower())
        except ValueError:
            return cls.PDKT


class Mood(Enum):
    """Enum untuk mood"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    EXCITED = "excited"
    AROUSED = "aroused"
    TIRED = "tired"
    ROMANTIC = "romantic"
    PLAYFUL = "playful"
    BORED = "bored"
    
    @classmethod
    def from_string(cls, value: str):
        """Convert string to enum"""
        try:
            return cls(value.lower())
        except ValueError:
            return cls.HAPPY


class Constants:
    """Constants for relationship models"""
    
    # Relationship stages
    STAGE_STRANGER = "stranger"
    STAGE_FRIEND = "friend"
    STAGE_CLOSE_FRIEND = "close_friend"
    STAGE_LOVER = "lover"
    STAGE_PARTNER = "partner"
    STAGE_MARRIED = "married"
    
    # Relationship statuses
    STATUS_PDKT = "pdkt"
    STATUS_SINGLE = "single"
    STATUS_COMPLICATED = "complicated"
    STATUS_EXCLUSIVE = "exclusive"
    
    # Dominance types
    DOM_NORMAL = "normal"
    DOM_DOMINANT = "dominant"
    DOM_SUBMISSIVE = "submissive"
    DOM_SWITCH = "switch"
    
    # Relationship types for HTS/FWB
    TYPE_HTS = "hts"  # Hubungan Tanpa Status
    TYPE_FWB = "fwb"  # Friends With Benefits
    TYPE_ONS = "ons"  # One Night Stand
    
    # Roles
    ROLE_USER = "user"
    ROLE_BOT = "bot"
    
    # Moods
    MOOD_HAPPY = "happy"
    MOOD_SAD = "sad"
    MOOD_ANGRY = "angry"
    MOOD_EXCITED = "excited"
    MOOD_AROUSED = "aroused"
    MOOD_TIRED = "tired"
    MOOD_ROMANTIC = "romantic"
    MOOD_PLAYFUL = "playful"
    MOOD_BORED = "bored"
    
    # Default values
    DEFAULT_LEVEL = 1
    DEFAULT_AROUSAL = 0.0
    DEFAULT_CLIMAX = 0
    DEFAULT_ANGER = 0


@dataclass
class Relationship:
    """Model relationship tanpa SQLAlchemy"""
    user_id: int
    bot_name: str
    bot_role: str
    level: int = 1
    stage: str = "stranger"
    dominance: str = "normal"
    total_messages: int = 0
    bot_climax: int = 0
    user_climax: int = 0
    together_climax: int = 0
    hair_style: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    breast_size: Optional[str] = None
    hijab: bool = False
    most_sensitive_area: Optional[str] = None
    skin_color: Optional[str] = None
    face_shape: Optional[str] = None
    personality: Optional[str] = None
    current_clothing: str = "pakaian biasa"
    last_clothing_change: Optional[datetime] = None
    anger_level: int = 0
    relationship_status: str = "pdkt"
    unique_id: Optional[str] = None
    created_at: datetime = None
    last_active: Optional[datetime] = None
    metadata: Optional[Dict] = None
    id: Optional[int] = None  # Primary key
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.unique_id is None:
            import uuid
            self.unique_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bot_name': self.bot_name,
            'bot_role': self.bot_role,
            'level': self.level,
            'stage': self.stage,
            'dominance': self.dominance,
            'total_messages': self.total_messages,
            'bot_climax': self.bot_climax,
            'user_climax': self.user_climax,
            'together_climax': self.together_climax,
            'hair_style': self.hair_style,
            'height': self.height,
            'weight': self.weight,
            'breast_size': self.breast_size,
            'hijab': self.hijab,
            'most_sensitive_area': self.most_sensitive_area,
            'skin_color': self.skin_color,
            'face_shape': self.face_shape,
            'personality': self.personality,
            'current_clothing': self.current_clothing,
            'last_clothing_change': self.last_clothing_change.isoformat() if self.last_clothing_change else None,
            'anger_level': self.anger_level,
            'relationship_status': self.relationship_status,
            'unique_id': self.unique_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'metadata': self.metadata
        }
    
    @property
    def dominance_enum(self) -> DominanceLevel:
        """Get dominance as enum"""
        return DominanceLevel.from_string(self.dominance)
    
    @property
    def stage_enum(self) -> RelationshipStage:
        """Get stage as enum"""
        return RelationshipStage.from_string(self.stage)
    
    @property
    def status_enum(self) -> RelationshipStatus:
        """Get status as enum"""
        return RelationshipStatus.from_string(self.relationship_status)


@dataclass
class Conversation:
    """Model conversation"""
    relationship_id: int
    role: str
    content: str
    mood: Optional[str] = None
    arousal: Optional[float] = None
    location: Optional[str] = None
    clothing: Optional[str] = None
    timestamp: datetime = None
    id: Optional[int] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'relationship_id': self.relationship_id,
            'role': self.role,
            'content': self.content,
            'mood': self.mood,
            'arousal': self.arousal,
            'location': self.location,
            'clothing': self.clothing,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @property
    def mood_enum(self) -> Optional[Mood]:
        """Get mood as enum"""
        if self.mood:
            return Mood.from_string(self.mood)
        return None


@dataclass
class Preference:
    """Model preferences"""
    user_id: int
    romantic_score: float = 0.0
    vulgar_score: float = 0.0
    dominant_score: float = 0.0
    submissive_score: float = 0.0
    speed_score: float = 0.0
    total_interactions: int = 0
    favorite_areas: Optional[List[str]] = None
    last_updated: datetime = None
    id: Optional[int] = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
        if self.favorite_areas is None:
            self.favorite_areas = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'romantic_score': self.romantic_score,
            'vulgar_score': self.vulgar_score,
            'dominant_score': self.dominant_score,
            'submissive_score': self.submissive_score,
            'speed_score': self.speed_score,
            'total_interactions': self.total_interactions,
            'favorite_areas': self.favorite_areas,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    def update_scores(self, message_type: str, intensity: float = 1.0):
        """Update preference scores based on interaction"""
        self.total_interactions += 1
        
        if message_type == "romantic":
            self.romantic_score += intensity
        elif message_type == "vulgar":
            self.vulgar_score += intensity
        elif message_type == "dominant":
            self.dominant_score += intensity
        elif message_type == "submissive":
            self.submissive_score += intensity
        
        self.last_updated = datetime.now()


@dataclass
class HTSFWBRelationship:
    """Model HTS/FWB"""
    unique_id: str
    user_id: int
    jenis: str
    role: str
    bot_name: str
    level_terakhir: int
    arousal_terakhir: float
    mood_terakhir: str
    bot_climax: int = 0
    user_climax: int = 0
    together_climax: int = 0
    last_touch: Optional[str] = None
    created_at: datetime = None
    last_called: Optional[datetime] = None
    message_count: int = 0
    id: Optional[int] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.unique_id is None:
            import uuid
            self.unique_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'unique_id': self.unique_id,
            'user_id': self.user_id,
            'jenis': self.jenis,
            'role': self.role,
            'bot_name': self.bot_name,
            'level_terakhir': self.level_terakhir,
            'arousal_terakhir': self.arousal_terakhir,
            'mood_terakhir': self.mood_terakhir,
            'bot_climax': self.bot_climax,
            'user_climax': self.user_climax,
            'together_climax': self.together_climax,
            'last_touch': self.last_touch,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_called': self.last_called.isoformat() if self.last_called else None,
            'message_count': self.message_count
        }
    
    @property
    def mood_enum(self) -> Optional[Mood]:
        """Get mood as enum"""
        if self.mood_terakhir:
            return Mood.from_string(self.mood_terakhir)
        return None


# Untuk memudahkan import
__all__ = [
    'DominanceLevel',
    'RelationshipStage',
    'RelationshipStatus',
    'Mood',
    'Constants',
    'Relationship',
    'Conversation',
    'Preference',
    'HTSFWBRelationship'
]
