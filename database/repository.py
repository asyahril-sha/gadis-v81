#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
REPOSITORY PATTERN
=============================================================================
Abstraction layer untuk database operations dengan SQLAlchemy
"""

from typing import Optional, Dict, List, Any, Union
from datetime import datetime

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    Relationship, Conversation, Memory, Preference,
    HTSFWBRelationship, ClimaxHistory, Ranking,
    SexPositionModel, SensitiveAreaModel, PublicLocation
)
from database.connection import get_session
from utils.logger import logger


class BaseRepository:
    """Base repository with common operations"""
    
    def __init__(self, session: AsyncSession = None):
        self.session = session
    
    async def _get_session(self):
        """Get session (create if not provided)"""
        if self.session:
            return self.session
        async with get_session() as session:
            return session


class RelationshipRepository(BaseRepository):
    """Repository for Relationship model"""
    
    async def get_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Get relationship by user_id"""
        session = await self._get_session()
        query = select(Relationship).where(Relationship.user_id == user_id)
        result = await session.execute(query)
        rel = result.scalar_one_or_none()
        if rel:
            return {c.name: getattr(rel, c.name) for c in rel.__table__.columns}
        return None
    
    async def create(self, user_id: int, bot_name: str, bot_role: str,
                    physical_attrs: Dict = None, clothing: str = None,
                    metadata: Dict = None) -> int:
        """Create new relationship"""
        session = await self._get_session()
        
        rel = Relationship(
            user_id=user_id,
            bot_name=bot_name,
            bot_role=bot_role,
            current_clothing=clothing or "pakaian biasa",
            metadata=metadata
        )
        
        if physical_attrs:
            rel.hair_style = physical_attrs.get('hair_style')
            rel.height = physical_attrs.get('height')
            rel.weight = physical_attrs.get('weight')
            rel.breast_size = physical_attrs.get('breast_size')
            rel.hijab = physical_attrs.get('hijab', 0)
            rel.most_sensitive_area = physical_attrs.get('most_sensitive_area')
            rel.skin_color = physical_attrs.get('skin')
            rel.face_shape = physical_attrs.get('face_shape')
            rel.personality = physical_attrs.get('personality')
        
        session.add(rel)
        await session.flush()
        return rel.id
    
    async def update(self, user_id: int, **kwargs) -> bool:
        """Update relationship fields"""
        session = await self._get_session()
        query = update(Relationship).where(Relationship.user_id == user_id).values(**kwargs)
        result = await session.execute(query)
        return result.rowcount > 0
    
    async def update_clothing(self, user_id: int, clothing: str) -> bool:
        """Update clothing"""
        return await self.update(
            user_id,
            current_clothing=clothing,
            last_clothing_change=datetime.now()
        )
    
    async def delete(self, user_id: int) -> bool:
        """Delete relationship"""
        session = await self._get_session()
        query = delete(Relationship).where(Relationship.user_id == user_id)
        result = await session.execute(query)
        return result.rowcount > 0


class ConversationRepository(BaseRepository):
    """Repository for Conversation model"""
    
    async def save(self, rel_id: int, role: str, content: str,
                  mood: str = None, arousal: float = None,
                  location: str = None, clothing: str = None) -> int:
        """Save conversation message"""
        session = await self._get_session()
        
        conv = Conversation(
            relationship_id=rel_id,
            role=role,
            content=content,
            mood=mood,
            arousal=arousal,
            location=location,
            clothing=clothing
        )
        
        session.add(conv)
        await session.flush()
        return conv.id
    
    async def get_history(self, rel_id: int, limit: int = 50) -> List[Dict]:
        """Get conversation history"""
        session = await self._get_session()
        query = select(Conversation).where(
            Conversation.relationship_id == rel_id
        ).order_by(Conversation.timestamp).limit(limit)
        
        result = await session.execute(query)
        convs = result.scalars().all()
        
        return [{
            'role': c.role,
            'content': c.content,
            'mood': c.mood,
            'arousal': c.arousal,
            'location': c.location,
            'clothing': c.clothing,
            'timestamp': c.timestamp.isoformat()
        } for c in convs]


class HTSFWBRepository(BaseRepository):
    """Repository for HTS/FWB relationships"""
    
    async def save(self, data: Dict) -> str:
        """Save HTS/FWB relationship"""
        session = await self._get_session()
        
        rel = HTSFWBRelationship(**data)
        session.add(rel)
        await session.flush()
        return rel.unique_id
    
    async def get(self, unique_id: str) -> Optional[Dict]:
        """Get by unique_id"""
        session = await self._get_session()
        query = select(HTSFWBRelationship).where(HTSFWBRelationship.unique_id == unique_id)
        result = await session.execute(query)
        rel = result.scalar_one_or_none()
        
        if rel:
            return {c.name: getattr(rel, c.name) for c in rel.__table__.columns}
        return None
    
    async def get_by_user(self, user_id: int, jenis: str = None) -> List[Dict]:
        """Get all by user_id"""
        session = await self._get_session()
        query = select(HTSFWBRelationship).where(HTSFWBRelationship.user_id == user_id)
        
        if jenis:
            query = query.where(HTSFWBRelationship.jenis == jenis)
        
        query = query.order_by(HTSFWBRelationship.last_called.desc())
        
        result = await session.execute(query)
        rels = result.scalars().all()
        
        return [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rels]
    
    async def update_last_called(self, unique_id: str):
        """Update last_called timestamp"""
        session = await self._get_session()
        query = update(HTSFWBRelationship).where(
            HTSFWBRelationship.unique_id == unique_id
        ).values(last_called=datetime.now())
        await session.execute(query)


class SexPositionRepository(BaseRepository):
    """Repository for sex positions (V81)"""
    
    async def get_all(self) -> List[Dict]:
        """Get all positions"""
        session = await self._get_session()
        query = select(SexPositionModel).order_by(SexPositionModel.popularity.desc())
        result = await session.execute(query)
        positions = result.scalars().all()
        
        return [{c.name: getattr(p, c.name) for c in p.__table__.columns} for p in positions]
    
    async def get_by_id(self, position_id: int) -> Optional[Dict]:
        """Get position by ID"""
        session = await self._get_session()
        query = select(SexPositionModel).where(SexPositionModel.id == position_id)
        result = await session.execute(query)
        pos = result.scalar_one_or_none()
        
        if pos:
            return {c.name: getattr(pos, c.name) for c in pos.__table__.columns}
        return None
    
    async def get_by_tags(self, tags: List[str]) -> List[Dict]:
        """Get positions by tags"""
        session = await self._get_session()
        # Simplified - in production would use JSON containment
        query = select(SexPositionModel)
        result = await session.execute(query)
        positions = result.scalars().all()
        
        filtered = []
        for pos in positions:
            if pos.tags and any(tag in pos.tags for tag in tags):
                filtered.append({c.name: getattr(pos, c.name) for c in pos.__table__.columns})
        
        return filtered


class SensitiveAreaRepository(BaseRepository):
    """Repository for sensitive areas (V81)"""
    
    async def get_all(self) -> List[Dict]:
        """Get all areas"""
        session = await self._get_session()
        query = select(SensitiveAreaModel).order_by(SensitiveAreaModel.popularity.desc())
        result = await session.execute(query)
        areas = result.scalars().all()
        
        return [{c.name: getattr(a, c.name) for c in a.__table__.columns} for a in areas]
    
    async def get_by_category(self, category: str) -> List[Dict]:
        """Get areas by category"""
        session = await self._get_session()
        query = select(SensitiveAreaModel).where(
            SensitiveAreaModel.category == category
        ).order_by(SensitiveAreaModel.popularity.desc())
        
        result = await session.execute(query)
        areas = result.scalars().all()
        
        return [{c.name: getattr(a, c.name) for c in a.__table__.columns} for a in areas]


class PublicLocationRepository(BaseRepository):
    """Repository for public locations (V81)"""
    
    async def get_all(self) -> List[Dict]:
        """Get all locations"""
        session = await self._get_session()
        query = select(PublicLocation).order_by(PublicLocation.popularity.desc())
        result = await session.execute(query)
        locations = result.scalars().all()
        
        return [{c.name: getattr(l, c.name) for c in l.__table__.columns} for l in locations]
    
    async def get_by_risk(self, max_risk: float) -> List[Dict]:
        """Get locations with risk <= max_risk"""
        session = await self._get_session()
        query = select(PublicLocation).where(
            PublicLocation.base_risk <= max_risk
        ).order_by(PublicLocation.popularity.desc())
        
        result = await session.execute(query)
        locations = result.scalars().all()
        
        return [{c.name: getattr(l, c.name) for c in l.__table__.columns} for l in locations]


# ===== FACTORY =====

class RepositoryFactory:
    """Factory for creating repositories"""
    
    @staticmethod
    def relationship(session: AsyncSession = None) -> RelationshipRepository:
        return RelationshipRepository(session)
    
    @staticmethod
    def conversation(session: AsyncSession = None) -> ConversationRepository:
        return ConversationRepository(session)
    
    @staticmethod
    def hts_fwb(session: AsyncSession = None) -> HTSFWBRepository:
        return HTSFWBRepository(session)
    
    @staticmethod
    def sex_positions(session: AsyncSession = None) -> SexPositionRepository:
        return SexPositionRepository(session)
    
    @staticmethod
    def sensitive_areas(session: AsyncSession = None) -> SensitiveAreaRepository:
        return SensitiveAreaRepository(session)
    
    @staticmethod
    def public_locations(session: AsyncSession = None) -> PublicLocationRepository:
        return PublicLocationRepository(session)


__all__ = ['RepositoryFactory']
