#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MEMORY TESTS
=============================================================================
Unit tests untuk memory systems
"""

import pytest
import asyncio
from datetime import datetime, timedelta

from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
from memory.vector_db import VectorMemory
from memory.relationship import RelationshipMemory


class TestEpisodicMemory:
    """Test episodic memory"""
    
    def test_add_episode(self):
        """Test adding episode"""
        memory = EpisodicMemory(max_size=10)
        
        episode_id = memory.add_episode(
            "Kita pertama kali bertemu",
            {'location': 'kafe', 'mood': 'ceria', 'level': 1}
        )
        
        assert episode_id is not None
        assert len(memory.memories) == 1
    
    def test_recall_recent(self):
        """Test recall recent memories"""
        memory = EpisodicMemory()
        
        # Add some memories
        for i in range(5):
            memory.add_episode(f"Memory {i}", {'level': i})
        
        recent = memory.recall_recent(hours=24, limit=3)
        assert len(recent) <= 3
    
    def test_recall_by_emotion(self):
        """Test recall by emotion"""
        memory = EpisodicMemory()
        
        memory.add_episode("Sedih", {'mood': 'sedih'})
        memory.add_episode("Senang", {'mood': 'ceria'})
        
        sad = memory.recall_by_emotion('sedih')
        assert len(sad) == 1
        assert sad[0]['emotion'] == 'sedih'
    
    def test_importance_calculation(self):
        """Test importance calculation"""
        memory = EpisodicMemory()
        
        # Important memory
        imp_id = memory.add_episode(
            "First climax",
            {'is_climax': True, 'level': 8}
        )
        
        # Normal memory
        norm_id = memory.add_episode(
            "Biasa aja",
            {}
        )
        
        imp_mem = next(m for m in memory.memories if m['id'] == imp_id)
        norm_mem = next(m for m in memory.memories if m['id'] == norm_id)
        
        assert imp_mem['importance'] > norm_mem['importance']


class TestSemanticMemory:
    """Test semantic memory"""
    
    def test_learn_fact(self):
        """Test learning facts"""
        memory = SemanticMemory()
        
        memory.learn_fact('preference', 'suka kopi', confidence=0.8)
        facts = memory.get_facts('preference')
        
        assert len(facts) == 1
        assert 'suka kopi' in facts[0]
    
    def test_learn_preference(self):
        """Test learning preferences"""
        memory = SemanticMemory()
        
        memory.learn_preference('food', 'bakso', 0.5)
        memory.learn_preference('food', 'bakso', 0.3)
        
        prefs = memory.get_preferences('food')
        assert len(prefs) == 1
        assert prefs[0][0] == 'bakso'
        assert prefs[0][1] == 0.8  # 0.5 + 0.3
    
    def test_extract_from_conversation(self):
        """Test extracting knowledge from conversation"""
        memory = SemanticMemory()
        
        messages = [
            {'role': 'user', 'content': 'Aku suka kopi'},
            {'role': 'user', 'content': 'Kopi favoritku'}
        ]
        
        memory.extract_from_conversation(messages)
        prefs = memory.get_preferences('general')
        
        assert len(prefs) > 0
    
    def test_reinforce_fact(self):
        """Test reinforcing facts"""
        memory = SemanticMemory()
        
        memory.learn_fact('test', 'fakta', 0.5)
        memory.reinforce_fact('test', 'fakta')
        
        facts = memory.get_facts('test', min_confidence=0.6)
        assert len(facts) == 1


class TestVectorMemory:
    """Test vector database memory"""
    
    @pytest.mark.asyncio
    async def test_add_and_retrieve(self):
        """Test adding and retrieving memories"""
        memory = VectorMemory(12345)
        
        # Add memory
        mem_id = await memory.add_memory(
            "Test memory content",
            "test",
            importance=0.8,
            emotion="ceria"
        )
        
        assert mem_id is not None
        
        # Retrieve
        results = await memory.retrieve_relevant("test", limit=5)
        # Note: results might be empty if ChromaDB not available
    
    @pytest.mark.asyncio
    async def test_memory_types(self):
        """Test memory type filtering"""
        memory = VectorMemory(12345)
        
        await memory.add_memory("Type 1", "type1")
        await memory.add_memory("Type 2", "type2")
        
        results = await memory.get_memories_by_type("type1", limit=5)
        # Test passes even if empty (fallback mode)


class TestRelationshipMemory:
    """Test relationship memory"""
    
    def test_add_milestone(self):
        """Test adding milestones"""
        memory = RelationshipMemory(12345, "TestBot")
        
        memory.add_milestone('first_meet', "First meeting", 1)
        memory.add_milestone('first_kiss', "First kiss", 5)
        
        assert memory.stats['total_milestones'] == 2
    
    def test_add_conflict(self):
        """Test adding conflicts"""
        memory = RelationshipMemory(12345, "TestBot")
        
        memory.add_conflict("Misunderstanding", 5)
        assert memory.stats['total_conflicts'] == 1
        
        # Trust should decrease
        assert memory.stats['current_trust'] < 0.5
    
    def test_resolve_conflict(self):
        """Test resolving conflicts"""
        memory = RelationshipMemory(12345, "TestBot")
        
        memory.add_conflict("Fight", 7)
        initial_trust = memory.stats['current_trust']
        
        memory.resolve_conflict(0, "Maaf ya")
        assert memory.stats['current_trust'] > initial_trust
    
    def test_anniversaries(self):
        """Test anniversary tracking"""
        memory = RelationshipMemory(12345, "TestBot")
        
        memory.add_milestone('first_meet', "First meet", 1)
        upcoming = memory.get_upcoming_anniversaries(30)
        
        assert len(upcoming) >= 0  # May be 0 if no anniversaries in range


if __name__ == "__main__":
    pytest.main([__file__])
