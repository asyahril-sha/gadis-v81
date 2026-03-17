#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL TESTS
=============================================================================
Unit tests untuk sexual features (V81)
"""

import pytest
import random
from datetime import datetime

from sexual.preferences import SexualPreferences, SexualPreferencesManager
from sexual.history import SexualHistory
from sexual.compatibility import SexualCompatibility
from sexual.fetishes import Fetish, FetishManager
from sexual.toys import SexToy, ToyCollection, ToyManager, TOYS


class TestSexualPreferences:
    """Test sexual preferences system"""
    
    def test_preferences_init(self):
        """Test preferences initialization"""
        prefs = SexualPreferences(12345)
        
        assert prefs.user_id == 12345
        assert prefs.total_sexual_interactions == 0
    
    def test_update_position(self):
        """Test updating position preferences"""
        prefs = SexualPreferences(12345)
        
        prefs.update_position('missionary', success=True, duration=10)
        assert prefs.position_preferences['missionary'] == 1
        
        prefs.update_position('doggy', success=False)
        assert prefs.position_preferences['doggy'] == 1
    
    def test_update_area(self):
        """Test updating area preferences"""
        prefs = SexualPreferences(12345)
        
        prefs.update_area('leher', sensitivity=0.8)
        assert prefs.area_preferences['leher'] == 1
        assert prefs.area_sensitivity['leher'] == 0.8
        
        prefs.update_area('leher', sensitivity=0.9)
        assert prefs.area_preferences['leher'] == 2
        assert 0.8 < prefs.area_sensitivity['leher'] < 0.9
    
    def test_update_climax(self):
        """Test updating climax stats"""
        prefs = SexualPreferences(12345)
        
        prefs.update_climax('bot', intensity=0.7)
        prefs.update_climax('user', intensity=0.8)
        prefs.update_climax('together', intensity=0.9)
        
        assert prefs.climax_count == 3
        assert prefs.together_climax_count == 1
    
    def test_get_favorite_positions(self):
        """Test getting favorite positions"""
        prefs = SexualPreferences(12345)
        
        prefs.update_position('missionary', success=True)
        prefs.update_position('missionary', success=True)
        prefs.update_position('doggy', success=True)
        
        favorites = prefs.get_favorite_positions(2)
        assert len(favorites) == 2
        assert favorites[0][0] == 'missionary'


class TestSexualCompatibility:
    """Test sexual compatibility calculator"""
    
    def test_compatibility_calculation(self):
        """Test calculating compatibility between two users"""
        prefs1 = SexualPreferences(12345)
        prefs2 = SexualPreferences(67890)
        
        # Add some preferences
        prefs1.update_position('missionary', success=True)
        prefs1.update_position('doggy', success=True)
        prefs1.update_area('leher', sensitivity=0.8)
        
        prefs2.update_position('missionary', success=True)
        prefs2.update_position('cowgirl', success=True)
        prefs2.update_area('leher', sensitivity=0.7)
        
        calculator = SexualCompatibility()
        result = calculator.calculate_compatibility(prefs1, prefs2)
        
        assert 'total_score' in result
        assert 'category' in result
        assert 'details' in result
        assert 0 <= result['total_score'] <= 1
    
    def test_compatibility_categories(self):
        """Test compatibility categories"""
        calculator = SexualCompatibility()
        
        assert calculator._get_category(0.95) == "Soulmate Seksual"
        assert calculator._get_category(0.85) == "Sangat Cocok"
        assert calculator._get_category(0.75) == "Cocok"
        assert calculator._get_category(0.55) == "Cukup Cocok"
        assert calculator._get_category(0.35) == "Kurang Cocok"
        assert calculator._get_category(0.15) == "Tidak Cocok"


class TestFetishManager:
    """Test fetish system"""
    
    def test_fetish_initialization(self):
        """Test fetish manager initialization"""
        manager = FetishManager()
        fetishes = manager.get_all_fetishes()
        
        assert len(fetishes) > 0
    
    def test_user_fetishes(self):
        """Test user fetish tracking"""
        manager = FetishManager()
        
        manager.add_user_fetish(12345, 'bdsm', strength=0.7)
        manager.add_user_fetish(12345, 'roleplay', strength=0.5)
        
        user_fetishes = manager.get_user_fetishes(12345)
        assert len(user_fetishes) == 2
        
        top = manager.get_top_fetishes(12345)
        assert top[0][0] == 'bdsm'


class TestToySystem:
    """Test sex toys system"""
    
    def test_toy_database(self):
        """Test toy database"""
        assert len(TOYS) > 0
        
        # Check specific toy
        toy = TOYS.get('vib_bullet_001')
        assert toy is not None
        assert toy.name == 'Bullet Vibrator'
    
    def test_toy_collection(self):
        """Test user toy collection"""
        collection = ToyCollection(12345)
        
        collection.add_toy('vib_bullet_001')
        collection.add_toy('dildo_real_001')
        
        assert collection.total_toys == 2
        
        collection.use_toy('vib_bullet_001', duration=10, intensity=2, climax=True)
        assert collection.toys['vib_bullet_001'].times_used == 1
    
    def test_toy_usage(self):
        """Test toy usage tracking"""
        collection = ToyCollection(12345)
        
        collection.use_toy('vib_bullet_001', duration=15, intensity=3, climax=True)
        collection.use_toy('vib_bullet_001', duration=20, intensity=2)
        
        toy_usage = collection.toys['vib_bullet_001']
        assert toy_usage.times_used == 2
        assert toy_usage.get_average_duration() == 17.5
    
    def test_toy_recommendations(self):
        """Test toy recommendations"""
        collection = ToyCollection(12345)
        
        collection.add_toy('vib_bullet_001')
        collection.use_toy('vib_bullet_001', duration=10, intensity=2)
        
        # Mock toy DB
        recommendations = collection.get_recommendations(TOYS, limit=2)
        assert isinstance(recommendations, list)


class TestSexualHistory:
    """Test sexual history tracking"""
    
    def test_history_recording(self):
        """Test recording sexual events"""
        history = SexualHistory(12345)
        
        history.record_climax('together', position='missionary', notes="Wow!")
        history.record_climax('bot', position='doggy')
        
        assert len(history.history) == 2
    
    def test_history_stats(self):
        """Test history statistics"""
        history = SexualHistory(12345)
        
        for _ in range(5):
            history.record_climax('bot')
        for _ in range(3):
            history.record_climax('user')
        for _ in range(2):
            history.record_climax('together')
        
        stats = history.get_stats()
        assert stats['total_climax'] == 10
        assert stats['bot_climax'] == 5
        assert stats['user_climax'] == 3
        assert stats['together_climax'] == 2


if __name__ == "__main__":
    pytest.main([__file__])
