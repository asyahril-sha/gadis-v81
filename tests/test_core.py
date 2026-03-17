#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
CORE TESTS
=============================================================================
Unit tests untuk core AI components
"""

import pytest
import asyncio
from datetime import datetime

from core.emotion import PADEmotionModel
from core.personality import PersonalityFormingMemory
from core.decision import NeuralDecisionSystem
from core.consciousness import ContinuousConsciousness


class TestEmotionModel:
    """Test PAD emotional model"""
    
    def test_initial_state(self):
        """Test initial emotional state"""
        emotion = PADEmotionModel()
        state = emotion.get_state()
        
        assert 'pleasure' in state['pad']
        assert 'arousal' in state['pad']
        assert 'dominance' in state['pad']
        assert state['emotion'] is not None
    
    def test_process_stimulus(self):
        """Test processing stimulus"""
        emotion = PADEmotionModel()
        initial = emotion.get_state()
        
        # Process positive stimulus
        result = emotion.process_stimulus("aku sayang kamu")
        
        assert 'delta' in result
        assert 'impact' in result
        assert 'emotion' in result
        
        # State should change
        new_state = emotion.get_state()
        assert new_state['pad'] != initial['pad']
    
    def test_decay(self):
        """Test emotional decay"""
        emotion = PADEmotionModel()
        initial = emotion.get_state()
        
        # Decay
        emotion.decay(0.1)
        new_state = emotion.get_state()
        
        # Should move toward baseline
        assert abs(new_state['pad']['pleasure'] - initial['pad']['pleasure']) < 0.2


class TestPersonality:
    """Test personality formation"""
    
    def test_initial_traits(self):
        """Test initial personality traits"""
        personality = PersonalityFormingMemory()
        traits = personality.traits
        
        assert 'openness' in traits
        assert 'conscientiousness' in traits
        assert 'extraversion' in traits
        assert 'agreeableness' in traits
        assert 'neuroticism' in traits
        
        # All traits should be between 0-1
        for value in traits.values():
            assert 0 <= value <= 1
    
    def test_update_from_interaction(self):
        """Test personality update from interaction"""
        personality = PersonalityFormingMemory()
        initial = personality.traits.copy()
        
        # Simulate interaction
        personality.update_from_interaction(
            "kamu baik sekali",
            {'personality_delta': {'agreeableness': 0.05}}
        )
        
        # Traits should change
        assert personality.traits != initial
    
    def test_trust_calculation(self):
        """Test trust level calculation"""
        personality = PersonalityFormingMemory()
        
        trust = personality.should_trust(12345, 10)
        assert 0 <= trust <= 1


class TestDecisionSystem:
    """Test neural decision system"""
    
    @pytest.mark.asyncio
    async def test_choose_response(self):
        """Test response selection"""
        decision = NeuralDecisionSystem()
        
        result = await decision.choose_response(
            message="halo",
            memories=[],
            emotional_state={'emotion': 'ceria'},
            personality={'traits': {'extraversion': 0.5}},
            context={}
        )
        
        assert 'response' in result
        assert 'type' in result
        assert 'confidence' in result
    
    def test_extract_features(self):
        """Test feature extraction"""
        decision = NeuralDecisionSystem()
        
        features = decision._extract_features(
            "Aku sayang kamu?",
            {'level': 5, 'arousal': 0.3}
        )
        
        assert 'length' in features
        assert 'has_question' in features
        assert features['has_question'] is True


class TestConsciousness:
    """Test continuous consciousness"""
    
    @pytest.mark.asyncio
    async def test_thought_generation(self):
        """Test thought generation"""
        consciousness = ContinuousConsciousness()
        
        # Mock agent
        class MockAgent:
            def __init__(self):
                self.emotion = type('obj', (), {'dominant_emotion': 'ceria'})
                self.arousal = 0.3
                self.personality = type('obj', (), {'traits': {}})
        
        thought = await consciousness.next_thought(MockAgent())
        
        if thought:
            assert 'type' in thought
            assert 'content' in thought
            assert 'timestamp' in thought
    
    def test_subconscious_processing(self):
        """Test subconscious processor"""
        consciousness = ContinuousConsciousness()
        
        text, effects = consciousness.subconscious.process("kamu sangat baik")
        
        assert isinstance(text, str)
        assert isinstance(effects, dict)


if __name__ == "__main__":
    pytest.main([__file__])
