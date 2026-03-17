#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEMANTIC MEMORY
=============================================================================
Menyimpan pengetahuan dan fakta yang diekstrak dari pengalaman
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Set
from collections import defaultdict, Counter
import re

from utils.logger import logger


class SemanticMemory:
    """
    Semantic memory - menyimpan pengetahuan umum dan fakta
    
    Berbeda dengan episodic memory yang menyimpan momen spesifik,
    semantic memory menyimpan:
    - Fakta tentang user
    - Preferensi yang diekstrak
    - Pengetahuan umum
    - Pola-pola yang terpelajari
    """
    
    def __init__(self):
        # Facts about user
        self.user_facts = defaultdict(list)
        
        # Preferences (learned)
        self.preferences = defaultdict(Counter)
        
        # Knowledge graph (simple)
        self.knowledge_graph = defaultdict(set)
        
        # User patterns
        self.user_patterns = {
            'favorite_topics': Counter(),
            'favorite_positions': Counter(),  # V81
            'favorite_areas': Counter(),      # V81
            'favorite_activities': Counter(), # V81
            'communication_style': defaultdict(float),
            'peak_hours': Counter(),
            'common_phrases': Counter()
        }
        
        # Statistics
        self.stats = {
            'total_facts': 0,
            'total_preferences': 0,
            'total_patterns': 0,
            'last_updated': datetime.now()
        }
        
        logger.info("📚 Semantic memory initialized")
    
    def learn_fact(self, category: str, fact: str, confidence: float = 0.8):
        """Learn a fact about user or world"""
        self.user_facts[category].append({
            'fact': fact,
            'confidence': confidence,
            'learned_at': datetime.now(),
            'times_confirmed': 1,
            'last_used': None
        })
        self.stats['total_facts'] += 1
    
    def learn_preference(self, category: str, item: str, strength: float = 0.5):
        """Learn user preference"""
        self.preferences[category][item] += strength
        self.stats['total_preferences'] += 1
    
    def learn_pattern(self, pattern_type: str, value: str, weight: float = 1.0):
        """Learn user pattern"""
        if pattern_type in self.user_patterns:
            if isinstance(self.user_patterns[pattern_type], Counter):
                self.user_patterns[pattern_type][value] += weight
            elif isinstance(self.user_patterns[pattern_type], dict):
                self.user_patterns[pattern_type][value] += weight
        self.stats['total_patterns'] += 1
    
    def get_facts(self, category: str, min_confidence: float = 0.5, limit: int = 10) -> List[str]:
        """Get facts in category"""
        facts = self.user_facts.get(category, [])
        # Filter by confidence and sort by recency
        valid = [f for f in facts if f['confidence'] >= min_confidence]
        valid.sort(key=lambda x: x['learned_at'], reverse=True)
        
        # Update last_used
        for f in valid[:limit]:
            f['last_used'] = datetime.now()
        
        return [f['fact'] for f in valid[:limit]]
    
    def get_preferences(self, category: str, limit: int = 10) -> List[tuple]:
        """Get top preferences in category"""
        prefs = self.preferences.get(category, Counter())
        return prefs.most_common(limit)
    
    def get_patterns(self, pattern_type: str, limit: int = 10) -> List[tuple]:
        """Get top patterns"""
        patterns = self.user_patterns.get(pattern_type, Counter())
        return patterns.most_common(limit)
    
    def extract_from_conversation(self, messages: List[Dict]):
        """Extract semantic knowledge from conversation"""
        for msg in messages:
            content = msg.get('content', '').lower()
            role = msg.get('role', 'user')
            
            if role != 'user':
                continue
            
            # Extract preferences
            self._extract_preferences(content)
            
            # Extract communication style
            self._extract_communication_style(content)
            
            # Extract common phrases
            self._extract_common_phrases(content)
    
    def _extract_preferences(self, text: str):
        """Extract preferences from text"""
        # Love keywords
        love_keywords = ['suka', 'sangat suka', 'favorit', 'gemar', 'senang']
        for keyword in love_keywords:
            if keyword in text:
                self._extract_item_after_keyword(text, keyword, +0.3)
        
        # Hate keywords
        hate_keywords = ['tidak suka', 'benci', 'ga suka', 'gak suka']
        for keyword in hate_keywords:
            if keyword in text:
                self._extract_item_after_keyword(text, keyword, -0.3)
        
        # V81: Sexual preferences
        sexual_keywords = ['posisi', 'area', 'aktivitas', 'suka kalau']
        for keyword in sexual_keywords:
            if keyword in text:
                self._extract_sexual_preference(text, keyword)
    
    def _extract_item_after_keyword(self, text: str, keyword: str, delta: float):
        """Extract item after keyword"""
        parts = text.split(keyword, 1)
        if len(parts) > 1:
            after = parts[1].strip().split()[:5]
            for word in after:
                if len(word) > 3 and word not in ['aku', 'kamu', 'ini', 'itu', 'dan', 'atau']:
                    self.learn_preference('general', word, abs(delta))
    
    def _extract_sexual_preference(self, text: str, keyword: str):
        """Extract sexual preference (V81)"""
        if 'posisi' in keyword:
            category = 'favorite_positions'
        elif 'area' in keyword:
            category = 'favorite_areas'
        elif 'aktivitas' in keyword:
            category = 'favorite_activities'
        else:
            category = 'sexual'
        
        parts = text.split(keyword, 1)
        if len(parts) > 1:
            after = parts[1].strip().split()[:3]
            for word in after:
                if len(word) > 2:
                    self.learn_pattern(category, word, 0.5)
    
    def _extract_communication_style(self, text: str):
        """Extract communication style"""
        # Message length
        if len(text) < 20:
            self.learn_pattern('communication_style', 'short', 0.1)
        elif len(text) > 100:
            self.learn_pattern('communication_style', 'long', 0.1)
        
        # Emoji usage
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)
        
        if emoji_pattern.search(text):
            self.learn_pattern('communication_style', 'emoji_user', 0.1)
        
        # Question style
        if '?' in text:
            self.learn_pattern('communication_style', 'questioner', 0.1)
        
        # Time of day
        hour = datetime.now().hour
        time_slot = 'pagi' if hour < 11 else 'siang' if hour < 15 else 'sore' if hour < 18 else 'malam'
        self.learn_pattern('peak_hours', time_slot, 0.1)
    
    def _extract_common_phrases(self, text: str):
        """Extract common phrases"""
        # Get 2-3 word phrases
        words = text.split()
        for i in range(len(words)-1):
            phrase = ' '.join(words[i:i+2])
            if len(phrase) > 5:
                self.learn_pattern('common_phrases', phrase, 0.1)
    
    def get_user_summary(self) -> Dict:
        """Get summary of what we know about user"""
        return {
            'favorite_topics': self.get_patterns('favorite_topics', 5),
            'favorite_positions': self.get_patterns('favorite_positions', 5),
            'favorite_areas': self.get_patterns('favorite_areas', 5),
            'favorite_activities': self.get_patterns('favorite_activities', 5),
            'communication_style': dict(self.user_patterns['communication_style']),
            'peak_hours': self.get_patterns('peak_hours', 3),
            'facts_count': self.stats['total_facts'],
            'preferences_count': self.stats['total_preferences'],
            'patterns_count': self.stats['total_patterns'],
            'categories': list(self.user_facts.keys())
        }
    
    def reinforce_fact(self, category: str, fact: str):
        """Reinforce a fact (increase confidence)"""
        for f in self.user_facts.get(category, []):
            if f['fact'] == fact:
                f['times_confirmed'] += 1
                f['confidence'] = min(1.0, f['confidence'] + 0.1)
                f['learned_at'] = datetime.now()
                break
    
    def decay_knowledge(self, days: int = 30):
        """Decay old knowledge (semantic forgetting)"""
        cutoff = datetime.now() - timedelta(days=days)
        
        old_count = self.stats['total_facts']
        
        # Decay user facts
        for category in list(self.user_facts.keys()):
            self.user_facts[category] = [
                f for f in self.user_facts[category]
                if f['learned_at'] > cutoff or f['times_confirmed'] > 3
            ]
        
        # Decay patterns (older than days)
        for pattern_type in self.user_patterns:
            if isinstance(self.user_patterns[pattern_type], Counter):
                # For Counters, we just keep them (no decay)
                pass
        
        new_count = sum(len(f) for f in self.user_facts.values())
        self.stats['total_facts'] = new_count
        
        logger.info(f"🧹 Decayed semantic knowledge: {old_count - new_count} facts forgotten")
    
    def query_knowledge(self, query: str) -> List[str]:
        """Query semantic knowledge"""
        results = []
        query_lower = query.lower()
        
        # Search in facts
        for category, facts in self.user_facts.items():
            for fact in facts:
                if query_lower in fact['fact'].lower():
                    results.append(fact['fact'])
        
        # Search in patterns
        for pattern_type, counter in self.user_patterns.items():
            if isinstance(counter, Counter):
                for item, count in counter.most_common(5):
                    if query_lower in item.lower():
                        results.append(f"{pattern_type}: {item}")
        
        return results[:10]


__all__ = ['SemanticMemory']
