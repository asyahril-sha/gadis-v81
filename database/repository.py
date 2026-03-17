#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
REPOSITORY PATTERN DENGAN SQLITE LANGSUNG
=============================================================================
"""

from typing import Optional, Dict, List, Any
from database.connection import execute_query, execute_insert, execute_update


class RelationshipRepository:
    """Repository untuk relationships"""
    
    @classmethod
    async def get_by_user_id(cls, user_id: int) -> Optional[Dict]:
        """Get relationship by user_id"""
        query = "SELECT * FROM relationships WHERE user_id = ?"
        results = await execute_query(query, (user_id,))
        return results[0] if results else None
    
    @classmethod
    async def create(cls, user_id: int, bot_name: str, bot_role: str,
                    physical_attrs: Dict = None, clothing: str = None,
                    metadata: Dict = None) -> int:
        """Create new relationship"""
        query = """
            INSERT INTO relationships 
            (user_id, bot_name, bot_role, current_clothing, metadata)
            VALUES (?, ?, ?, ?, ?)
        """
        return await execute_insert(
            query, 
            (user_id, bot_name, bot_role, clothing or "pakaian biasa", 
             str(metadata) if metadata else None)
        )
    
    @classmethod
    async def update(cls, user_id: int, **kwargs) -> bool:
        """Update relationship"""
        if not kwargs:
            return False
        
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        
        values.append(user_id)
        query = f"""
            UPDATE relationships
            SET {', '.join(fields)}, last_active = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """
        
        return await execute_update(query, tuple(values)) > 0
    
    @classmethod
    async def delete(cls, user_id: int) -> bool:
        """Delete relationship"""
        query = "DELETE FROM relationships WHERE user_id = ?"
        return await execute_update(query, (user_id,)) > 0


class ConversationRepository:
    """Repository untuk conversations"""
    
    @classmethod
    async def save(cls, rel_id: int, role: str, content: str,
                  mood: str = None, arousal: float = None,
                  location: str = None, clothing: str = None) -> int:
        """Save conversation"""
        query = """
            INSERT INTO conversations 
            (relationship_id, role, content, mood, arousal, location, clothing)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return await execute_insert(
            query, (rel_id, role, content, mood, arousal, location, clothing)
        )
    
    @classmethod
    async def get_history(cls, rel_id: int, limit: int = 50) -> List[Dict]:
        """Get conversation history"""
        query = """
            SELECT * FROM conversations
            WHERE relationship_id = ?
            ORDER BY timestamp ASC
            LIMIT ?
        """
        return await execute_query(query, (rel_id, limit))


class HTSFWBRepository:
    """Repository untuk HTS/FWB"""
    
    @classmethod
    async def save(cls, data: Dict) -> str:
        """Save HTS/FWB"""
        query = """
            INSERT INTO hts_fwb_relationships 
            (unique_id, user_id, jenis, role, bot_name, 
             level_terakhir, arousal_terakhir, mood_terakhir,
             bot_climax, user_climax, together_climax, last_touch,
             message_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        await execute_insert(query, (
            data['unique_id'], data['user_id'], data['jenis'],
            data['role'], data['bot_name'], data['level_terakhir'],
            data['arousal_terakhir'], data['mood_terakhir'],
            data.get('bot_climax', 0), data.get('user_climax', 0),
            data.get('together_climax', 0), data.get('last_touch'),
            data.get('message_count', 0)
        ))
        return data['unique_id']
    
    @classmethod
    async def get(cls, unique_id: str) -> Optional[Dict]:
        """Get by unique_id"""
        query = "SELECT * FROM hts_fwb_relationships WHERE unique_id = ?"
        results = await execute_query(query, (unique_id,))
        return results[0] if results else None
    
    @classmethod
    async def get_by_user(cls, user_id: int, jenis: str = None) -> List[Dict]:
        """Get all by user_id"""
        if jenis:
            query = "SELECT * FROM hts_fwb_relationships WHERE user_id = ? AND jenis = ? ORDER BY last_called DESC"
            return await execute_query(query, (user_id, jenis))
        else:
            query = "SELECT * FROM hts_fwb_relationships WHERE user_id = ? ORDER BY last_called DESC"
            return await execute_query(query, (user_id,))
    
    @classmethod
    async def update_last_called(cls, unique_id: str):
        """Update last_called"""
        query = "UPDATE hts_fwb_relationships SET last_called = CURRENT_TIMESTAMP WHERE unique_id = ?"
        await execute_update(query, (unique_id,))


# Factory
class RepositoryFactory:
    """Factory untuk repositories"""
    
    @staticmethod
    def relationship():
        return RelationshipRepository
    
    @staticmethod
    def conversation():
        return ConversationRepository
    
    @staticmethod
    def hts_fwb():
        return HTSFWBRepository
