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
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


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
    last_updated: datetime = None
    
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
    created_at: datetime = None
    last_called: Optional[datetime] = None
    message_count: int = 0
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
