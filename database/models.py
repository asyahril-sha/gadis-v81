#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SQLALCHEMY MODELS
=============================================================================
Semua database models untuk PostgreSQL
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class Relationship(Base):
    """Main relationship table"""
    __tablename__ = "relationships"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    bot_name: Mapped[str] = mapped_column(String(50), nullable=False)
    bot_role: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Level & Progress
    level: Mapped[int] = mapped_column(Integer, default=1)
    stage: Mapped[str] = mapped_column(String(50), default="stranger")
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    
    # Climax counters
    bot_climax: Mapped[int] = mapped_column(Integer, default=0)
    user_climax: Mapped[int] = mapped_column(Integer, default=0)
    together_climax: Mapped[int] = mapped_column(Integer, default=0)
    
    # Physical attributes
    hair_style: Mapped[Optional[str]] = mapped_column(String(50))
    height: Mapped[Optional[int]] = mapped_column(Integer)
    weight: Mapped[Optional[int]] = mapped_column(Integer)
    breast_size: Mapped[Optional[str]] = mapped_column(String(20))
    hijab: Mapped[bool] = mapped_column(Boolean, default=False)
    most_sensitive_area: Mapped[Optional[str]] = mapped_column(String(50))
    skin_color: Mapped[Optional[str]] = mapped_column(String(30))
    face_shape: Mapped[Optional[str]] = mapped_column(String(30))
    personality: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Clothing
    current_clothing: Mapped[str] = mapped_column(String(100), default="pakaian biasa")
    last_clothing_change: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Emotional state
    anger_level: Mapped[int] = mapped_column(Integer, default=0)
    jealousy_level: Mapped[int] = mapped_column(Integer, default=0)
    dominance_mode: Mapped[str] = mapped_column(String(30), default="normal")
    
    # Relationship status
    relationship_status: Mapped[str] = mapped_column(String(20), default="pdkt")
    unique_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    trust_level: Mapped[float] = mapped_column(Float, default=0.5)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_active: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Relationships
    conversations: Mapped[List["Conversation"]] = relationship(back_populates="relationship")
    memories: Mapped[List["Memory"]] = relationship(back_populates="relationship")
    
    __table_args__ = (
        Index("idx_relationships_user", "user_id"),
        Index("idx_relationships_status", "relationship_status"),
    )


class Conversation(Base):
    """Conversation history"""
    __tablename__ = "conversations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    relationship_id: Mapped[int] = mapped_column(ForeignKey("relationships.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # 'user' or 'bot'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Context
    mood: Mapped[Optional[str]] = mapped_column(String(30))
    arousal: Mapped[Optional[float]] = mapped_column(Float)
    location: Mapped[Optional[str]] = mapped_column(String(50))
    clothing: Mapped[Optional[str]] = mapped_column(String(100))
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # Relationships
    relationship: Mapped["Relationship"] = relationship(back_populates="conversations")
    
    __table_args__ = (
        Index("idx_conversations_rel", "relationship_id"),
        Index("idx_conversations_time", "timestamp"),
    )


class Memory(Base):
    """Memory storage"""
    __tablename__ = "memories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    relationship_id: Mapped[int] = mapped_column(ForeignKey("relationships.id", ondelete="CASCADE"))
    memory_id: Mapped[str] = mapped_column(String(50), unique=True)
    memory: Mapped[str] = mapped_column(Text, nullable=False)
    memory_type: Mapped[str] = mapped_column(String(30), nullable=False)
    
    importance: Mapped[float] = mapped_column(Float, default=0.5)
    emotion: Mapped[Optional[str]] = mapped_column(String(30))
    context: Mapped[Optional[dict]] = mapped_column(JSON)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_accessed: Mapped[Optional[datetime]] = mapped_column(DateTime)
    access_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    relationship: Mapped["Relationship"] = relationship(back_populates="memories")
    
    __table_args__ = (
        Index("idx_memories_rel", "relationship_id"),
        Index("idx_memories_type", "memory_type"),
    )


class Preference(Base):
    """User preferences"""
    __tablename__ = "preferences"
    
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Personality scores
    romantic_score: Mapped[float] = mapped_column(Float, default=0.0)
    vulgar_score: Mapped[float] = mapped_column(Float, default=0.0)
    dominant_score: Mapped[float] = mapped_column(Float, default=0.0)
    submissive_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # V81 Sexual preferences
    favorite_positions: Mapped[Optional[list]] = mapped_column(JSON)  # List of position IDs
    favorite_areas: Mapped[Optional[list]] = mapped_column(JSON)  # List of area IDs
    favorite_activities: Mapped[Optional[list]] = mapped_column(JSON)  # List of activity IDs
    risk_tolerance: Mapped[float] = mapped_column(Float, default=0.5)  # For public areas
    
    total_interactions: Mapped[int] = mapped_column(Integer, default=0)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class HTSFWBRelationship(Base):
    """HTS/FWB relationships"""
    __tablename__ = "hts_fwb_relationships"
    
    unique_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    jenis: Mapped[str] = mapped_column(String(10), nullable=False)  # 'HTS' or 'FWB'
    
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    bot_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Last state
    level_terakhir: Mapped[int] = mapped_column(Integer)
    arousal_terakhir: Mapped[float] = mapped_column(Float)
    mood_terakhir: Mapped[str] = mapped_column(String(30))
    
    # Climax stats
    bot_climax: Mapped[int] = mapped_column(Integer, default=0)
    user_climax: Mapped[int] = mapped_column(Integer, default=0)
    together_climax: Mapped[int] = mapped_column(Integer, default=0)
    
    last_touch: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_called: Mapped[Optional[datetime]] = mapped_column(DateTime)
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # V81 New fields
    favorite_position: Mapped[Optional[str]] = mapped_column(String(50))
    favorite_area: Mapped[Optional[str]] = mapped_column(String(50))
    total_public_encounters: Mapped[int] = mapped_column(Integer, default=0)
    risk_success_rate: Mapped[float] = mapped_column(Float, default=0.0)


class ClimaxHistory(Base):
    """Climax history tracking"""
    __tablename__ = "climax_history"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    unique_id: Mapped[str] = mapped_column(String(100), ForeignKey("hts_fwb_relationships.unique_id", ondelete="CASCADE"))
    climax_type: Mapped[str] = mapped_column(String(20), nullable=False)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    trigger_message: Mapped[Optional[str]] = mapped_column(Text)
    arousal_before: Mapped[Optional[float]] = mapped_column(Float)
    mood_before: Mapped[Optional[str]] = mapped_column(String(30))
    bot_response: Mapped[Optional[str]] = mapped_column(Text)
    
    # V81 New fields
    position: Mapped[Optional[str]] = mapped_column(String(50))  # Position used
    location: Mapped[Optional[str]] = mapped_column(String(50))  # Location
    public_risk: Mapped[Optional[float]] = mapped_column(Float)  # Risk level if public
    was_caught: Mapped[bool] = mapped_column(Boolean, default=False)


class Ranking(Base):
    """TOP 10 ranking"""
    __tablename__ = "ranking"
    
    rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_id: Mapped[str] = mapped_column(String(100), ForeignKey("hts_fwb_relationships.unique_id", ondelete="CASCADE"), unique=True)
    
    total_climax: Mapped[int] = mapped_column(Integer, default=0)
    bot_climax: Mapped[int] = mapped_column(Integer, default=0)
    user_climax: Mapped[int] = mapped_column(Integer, default=0)
    together_climax: Mapped[int] = mapped_column(Integer, default=0)
    
    # V81 New fields
    total_public_climax: Mapped[int] = mapped_column(Integer, default=0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


# ===== V81 NEW MODELS =====

class SexPositionModel(Base):
    """Sex positions database"""
    __tablename__ = "sex_positions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    
    # Difficulty & intensity
    difficulty: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    intensity: Mapped[float] = mapped_column(Float, default=0.5)  # 0-1
    arousal_boost: Mapped[float] = mapped_column(Float, default=0.3)
    
    # Requirements
    requires_flexibility: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_strength: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Tags
    tags: Mapped[Optional[list]] = mapped_column(JSON)  # ['romantic', 'intense', 'public_friendly']
    
    # Media
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    guide_text: Mapped[Optional[str]] = mapped_column(Text)
    
    # Stats
    popularity: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Float, default=0.0)


class SensitiveAreaModel(Base):
    """Sensitive areas database"""
    __tablename__ = "sensitive_areas"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    
    # Sensitivity level
    sensitivity: Mapped[float] = mapped_column(Float, default=0.5)  # 0-1
    arousal_boost: Mapped[float] = mapped_column(Float, default=0.2)
    
    # Location category
    category: Mapped[str] = mapped_column(String(50))  # 'head', 'upper_body', 'lower_body'
    
    # Tags
    tags: Mapped[Optional[list]] = mapped_column(JSON)
    
    # Stats
    popularity: Mapped[int] = mapped_column(Integer, default=0)


class PublicLocation(Base):
    """Public locations database"""
    __tablename__ = "public_locations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    
    # Risk levels
    base_risk: Mapped[float] = mapped_column(Float, default=0.5)  # 0-1
    time_multipliers: Mapped[Optional[dict]] = mapped_column(JSON)  # {'day': 1.2, 'night': 0.8}
    
    # Thrill factor
    thrill_boost: Mapped[float] = mapped_column(Float, default=0.3)
    
    # Requirements
    requires_vehicle: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_privacy: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Possible events
    possible_events: Mapped[Optional[list]] = mapped_column(JSON)
    
    # Stats
    popularity: Mapped[int] = mapped_column(Integer, default=0)
    success_rate: Mapped[float] = mapped_column(Float, default=0.0)


__all__ = [
    'Base', 'Relationship', 'Conversation', 'Memory', 'Preference',
    'HTSFWBRelationship', 'ClimaxHistory', 'Ranking',
    'SexPositionModel', 'SensitiveAreaModel', 'PublicLocation'
]
