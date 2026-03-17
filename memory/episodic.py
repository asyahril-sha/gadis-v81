#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
EPISODIC MEMORY
=============================================================================
Menyimpan momen-momen penting dengan konteks lengkap
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from collections import deque

from utils.logger import logger


class EpisodicMemory:
    """
    Episodic memory - menyimpan momen spesifik dengan konteks
    - Kapan, di mana, dengan siapa
    - Apa yang dirasakan
    - Emotional context
    """
    
    def __init__(self, max_size: int = 1000):
        self.memories = deque(maxlen=max_size)
        self.max_size = max_size
        self.stats = {
            "total_memories": 0,
            "important_memories": 0,
            "average_importance": 0.0
        }
        logger.info(f"📖 Episodic memory initialized (max {max_size})")
    
    def add_episode(self, content: str, context: Dict[str, Any]) -> str:
        """
        Add an episodic memory
        
        Args:
            content: What happened
            context: Context (location, mood, level, etc)
        
        Returns:
            episode_id
        """
        episode_id = f"ep_{int(datetime.now().timestamp())}_{len(self.memories)}"
        
        importance = self._calculate_importance(content, context)
        
        episode = {
            'id': episode_id,
            'content': content,
            'timestamp': datetime.now(),
            'context': context.copy(),
            'importance': importance,
            'recall_count': 0,
            'last_recall': None,
            'emotion': context.get('mood', 'neutral'),
            'tags': self._generate_tags(content, context)
        }
        
        self.memories.append(episode)
        
        # Update stats
        self.stats["total_memories"] += 1
        if importance > 0.7:
            self.stats["important_memories"] += 1
        
        total_imp = sum(m['importance'] for m in self.memories)
        self.stats["average_importance"] = total_imp / len(self.memories) if self.memories else 0
        
        return episode_id
    
    def _calculate_importance(self, content: str, context: Dict) -> float:
        """Calculate how important this memory is"""
        importance = 0.5  # Base
        
        # First time experiences are important
        if context.get('is_first_time', False):
            importance += 0.3
        
        # High emotion = important
        if context.get('emotion_intensity', 0) > 0.7:
            importance += 0.2
        
        # Climax moments
        if context.get('is_climax', False):
            importance += 0.3
        
        # High level moments
        if context.get('level', 0) > 10:
            importance += 0.2
        
        # V81: Public area moments
        if context.get('is_public', False):
            importance += 0.15
        
        # V81: New position/activity
        if context.get('new_position', False) or context.get('new_activity', False):
            importance += 0.2
        
        return min(1.0, importance)
    
    def _generate_tags(self, content: str, context: Dict) -> List[str]:
        """Generate tags for memory"""
        tags = []
        
        # Add emotion tag
        if context.get('mood'):
            tags.append(f"emotion:{context['mood']}")
        
        # Add location tag
        if context.get('location'):
            tags.append(f"location:{context['location']}")
        
        # Add role tag
        if context.get('role'):
            tags.append(f"role:{context['role']}")
        
        # Add level tag
        if context.get('level'):
            level_group = (context['level'] // 3) * 3
            tags.append(f"level:{level_group}-{level_group+2}")
        
        # Add important tag
        if context.get('importance', 0.5) > 0.7:
            tags.append("important")
        
        # Add sexual tags (V81)
        if context.get('position'):
            tags.append(f"position:{context['position']}")
        if context.get('activity'):
            tags.append(f"activity:{context['activity']}")
        if context.get('area'):
            tags.append(f"area:{context['area']}")
        
        return tags
    
    def recall_recent(self, hours: int = 24, limit: int = 10) -> List[Dict]:
        """Recall memories from recent hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent = []
        for mem in reversed(self.memories):  # Most recent first
            if mem['timestamp'] > cutoff:
                mem_copy = mem.copy()
                mem_copy['recall_count'] += 1
                mem_copy['last_recall'] = datetime.now()
                recent.append(mem_copy)
                
                if len(recent) >= limit:
                    break
        
        return recent
    
    def recall_by_emotion(self, emotion: str, limit: int = 10) -> List[Dict]:
        """Recall memories with specific emotion"""
        matching = []
        
        for mem in reversed(self.memories):
            if mem['emotion'] == emotion:
                mem_copy = mem.copy()
                mem_copy['recall_count'] += 1
                mem_copy['last_recall'] = datetime.now()
                matching.append(mem_copy)
                
                if len(matching) >= limit:
                    break
        
        return matching
    
    def recall_by_tags(self, tags: List[str], match_all: bool = False, limit: int = 10) -> List[Dict]:
        """Recall memories by tags"""
        matching = []
        
        for mem in reversed(self.memories):
            mem_tags = mem.get('tags', [])
            
            if match_all:
                if all(tag in mem_tags for tag in tags):
                    mem_copy = mem.copy()
                    mem_copy['recall_count'] += 1
                    mem_copy['last_recall'] = datetime.now()
                    matching.append(mem_copy)
            else:
                if any(tag in mem_tags for tag in tags):
                    mem_copy = mem.copy()
                    mem_copy['recall_count'] += 1
                    mem_copy['last_recall'] = datetime.now()
                    matching.append(mem_copy)
            
            if len(matching) >= limit:
                break
        
        return matching
    
    def get_important_memories(self, threshold: float = 0.7, limit: int = 20) -> List[Dict]:
        """Get important memories"""
        important = []
        
        for mem in sorted(self.memories, key=lambda x: x['importance'], reverse=True):
            if mem['importance'] >= threshold:
                mem_copy = mem.copy()
                important.append(mem_copy)
                
                if len(important) >= limit:
                    break
        
        return important
    
    def search_by_keyword(self, keyword: str, case_sensitive: bool = False) -> List[Dict]:
        """Search memories by keyword"""
        results = []
        keyword_lower = keyword.lower() if not case_sensitive else keyword
        
        for mem in self.memories:
            content = mem['content']
            if not case_sensitive:
                content = content.lower()
            
            if keyword_lower in content:
                mem_copy = mem.copy()
                mem_copy['recall_count'] += 1
                mem_copy['last_recall'] = datetime.now()
                results.append(mem_copy)
        
        return results
    
    def get_memory_timeline(self, start_date: datetime = None, 
                           end_date: datetime = None) -> List[Dict]:
        """Get memories in date range"""
        if not start_date:
            start_date = datetime.min
        if not end_date:
            end_date = datetime.now()
        
        timeline = []
        for mem in self.memories:
            if start_date <= mem['timestamp'] <= end_date:
                timeline.append(mem.copy())
        
        return sorted(timeline, key=lambda x: x['timestamp'])
    
    def get_memories_by_location(self, location: str, limit: int = 20) -> List[Dict]:
        """Get memories by location"""
        return self.recall_by_tags([f"location:{location}"], limit=limit)
    
    def get_memories_by_role(self, role: str, limit: int = 20) -> List[Dict]:
        """Get memories by role"""
        return self.recall_by_tags([f"role:{role}"], limit=limit)
    
    def forget_old_memories(self, days: int = 30):
        """Forget memories older than days (semantic forgetting)"""
        cutoff = datetime.now() - timedelta(days=days)
        
        # Keep only recent memories
        old_count = len(self.memories)
        self.memories = deque(
            [m for m in self.memories if m['timestamp'] > cutoff],
            maxlen=self.max_size
        )
        
        forgotten = old_count - len(self.memories)
        logger.info(f"🧹 Forgot {forgotten} memories older than {days} days")
        
        return forgotten
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        return {
            **self.stats,
            "current_size": len(self.memories),
            "max_size": self.max_size,
            "usage_percent": (len(self.memories) / self.max_size) * 100
        }


__all__ = ['EpisodicMemory']
