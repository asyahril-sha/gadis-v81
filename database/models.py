#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
DATABASE MODELS (TANPA SQLALCHEMY)
=============================================================================
Menggunakan dataclasses biasa, bukan SQLAlchemy
"""

from dataclasses import dataclass, field
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


class ConversationState(Enum):
    """Enum untuk conversation states (untuk PTB ConversationHandler)"""
    SELECTING_ROLE = 1
    SELECTING_BOT_NAME = 2
    SELECTING_BOT_ROLE = 3
    SELECTING_DOMINANCE = 4
    SELECTING_PERSONALITY = 5
    SELECTING_APPEARANCE = 6
    CONFIRMATION = 7
    CHATTING = 8
    SELECTING_ACTION = 9
    SELECTING_LOCATION = 10
    SELECTING_CLOTHING = 11
    SELECTING_ACTIVITY = 12
    AWAITING_RESPONSE = 13


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
    
    # Conversation States (untuk PTB ConversationHandler)
    SELECTING_ROLE = ConversationState.SELECTING_ROLE.value
    SELECTING_BOT_NAME = ConversationState.SELECTING_BOT_NAME.value
    SELECTING_BOT_ROLE = ConversationState.SELECTING_BOT_ROLE.value
    SELECTING_DOMINANCE = ConversationState.SELECTING_DOMINANCE.value
    SELECTING_PERSONALITY = ConversationState.SELECTING_PERSONALITY.value
    SELECTING_APPEARANCE = ConversationState.SELECTING_APPEARANCE.value
    CONFIRMATION = ConversationState.CONFIRMATION.value
    CHATTING = ConversationState.CHATTING.value
    SELECTING_ACTION = ConversationState.SELECTING_ACTION.value
    SELECTING_LOCATION = ConversationState.SELECTING_LOCATION.value
    SELECTING_CLOTHING = ConversationState.SELECTING_CLOTHING.value
    SELECTING_ACTIVITY = ConversationState.SELECTING_ACTIVITY.value
    AWAITING_RESPONSE = ConversationState.AWAITING_RESPONSE.value


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
    created_at: Optional[datetime] = None
    last_active: Optional[datetime] = None
    metadata: Optional[Dict] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.unique_id is None:
            import uuid
            self.unique_id = str(uuid.uuid4())


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
    timestamp: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


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
    last_updated: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
        if self.favorite_areas is None:
            self.favorite_areas = []


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
    created_at: Optional[datetime] = None
    last_called: Optional[datetime] = None
    message_count: int = 0
    id: Optional[int] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.unique_id is None:
            import uuid
            self.unique_id = str(uuid.uuid4())


__all__ = [
    'DominanceLevel',
    'RelationshipStage',
    'RelationshipStatus',
    'Mood',
    'ConversationState',
    'Constants',
    'Relationship',
    'Conversation',
    'Preference',
    'HTSFWBRelationship'
]
