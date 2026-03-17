#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MEMORY CONSOLIDATION SYSTEM
=============================================================================
Memindahkan memori jangka pendek ke jangka panjang
Membentuk semantic memory dari episodic memory
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from collections import defaultdict, Counter

from utils.logger import logger
from config import settings


class MemoryConsolidation:
    """
    Memory consolidation - seperti tidur pada manusia
    
    Proses:
    1. Identifikasi memori penting dari hari ini
    2. Buat ringkasan semantic
    3. Pindahkan ke long-term storage
    4. Hapus memori tidak penting
    """
    
    def __init__(self, vector_db, episodic_memory, semantic_memory):
        self.vector_db = vector_db
        self.episodic = episodic_memory
        self.semantic = semantic_memory
        
        # Consolidation schedule
        self.last_consolidation = datetime.now()
        self.consolidation_interval = timedelta(hours=6)  # Setiap 6 jam
        
        # Stats
        self.stats = {
            'total_consolidations': 0,
            'memories_consolidated': 0,
            'semantic_facts_created': 0,
            'memories_forgotten': 0
        }
        
        logger.info("🔄 Memory Consolidation system initialized")
    
    async def consolidate(self, force: bool = False) -> Dict:
        """
        Run memory consolidation
        Returns stats about consolidation
        """
        now = datetime.now()
        
        # Check if it's time to consolidate
        if not force and (now - self.last_consolidation) < self.consolidation_interval:
            next_time = self.last_consolidation + self.consolidation_interval
            return {
                'status': 'skipped',
                'next': next_time.isoformat(),
                'reason': 'too_soon'
            }
        
        logger.info("🔄 Running memory consolidation...")
        
        stats = {
            'episodic_to_semantic': 0,
            'important_memories': 0,
            'forgotten_memories': 0,
            'patterns_found': 0
        }
        
        # 1. Get recent episodic memories
        recent = self.episodic.recall_recent(hours=24, limit=200)
        
        # 2. Identify important memories
        important = [m for m in recent if m['importance'] > 0.7]
        stats['important_memories'] = len(important)
        
        # 3. Extract semantic knowledge from important memories
        for memory in important:
            facts = self._extract_facts(memory)
            for fact in facts:
                self.semantic.learn_fact(
                    category=fact['category'],
                    fact=fact['content'],
                    confidence=fact['confidence']
                )
                stats['episodic_to_semantic'] += 1
        
        # 4. Find patterns in recent memories
        patterns = self._find_patterns(recent)
        for pattern_type, items in patterns.items():
            for item, count in items:
                if count > 2:  # Pattern muncul minimal 3 kali
                    self.semantic.learn_pattern(pattern_type, item, count)
                    stats['patterns_found'] += 1
        
        # 5. Create consolidated summary
        summary = self._create_summary(recent, important, patterns)
        if summary:
            await self.vector_db.add_memory(
                content=summary,
                memory_type='consolidated',
                importance=0.8,
                context={
                    'type': 'daily_summary',
                    'date': now.date().isoformat(),
                    'memories_processed': len(recent)
                }
            )
        
        # 6. Forget old/unimportant memories (semantic forgetting)
        forgotten = self.episodic.forget_old_memories(days=30)
        stats['forgotten_memories'] = forgotten
        
        # Update stats
        self.stats['total_consolidations'] += 1
        self.stats['memories_consolidated'] += stats['episodic_to_semantic']
        self.stats['semantic_facts_created'] += stats['episodic_to_semantic']
        self.stats['memories_forgotten'] += forgotten
        
        self.last_consolidation = now
        
        logger.info(f"✅ Consolidation complete: {stats}")
        
        return {
            'status': 'success',
            'stats': stats,
            'next': (now + self.consolidation_interval).isoformat()
        }
    
    def _extract_facts(self, memory: Dict) -> List[Dict]:
        """Extract semantic facts from episodic memory"""
        facts = []
        content = memory['content'].lower()
        context = memory.get('context', {})
        
        # Extract preferences
        if 'suka' in content or 'favorit' in content or 'senang' in content:
            facts.append({
                'category': 'preference',
                'content': memory['content'][:150],
                'confidence': 0.6
            })
        
        # Extract relationship facts
        if 'kamu' in content and ('suka' in content or 'cinta' in content):
            facts.append({
                'category': 'relationship',
                'content': f"User merasa {memory['content'][:100]}",
                'confidence': 0.7
            })
        
        # Extract facts from context
        if context.get('level'):
            facts.append({
                'category': 'progress',
                'content': f"Level mencapai {context['level']} pada {memory['timestamp'].strftime('%d/%m')}",
                'confidence': 0.9
            })
        
        if context.get('location'):
            facts.append({
                'category': 'location',
                'content': f"Pernah berada di {context['location']}",
                'confidence': 0.8
            })
        
        # V81: Extract sexual preferences
        if context.get('position'):
            facts.append({
                'category': 'sexual_position',
                'content': f"Suka posisi {context['position']}",
                'confidence': 0.7
            })
        
        if context.get('area'):
            facts.append({
                'category': 'sensitive_area',
                'content': f"Area {context['area']} sangat sensitif",
                'confidence': 0.7
            })
        
        if context.get('public_area'):
            facts.append({
                'category': 'public_area',
                'content': f"Pernah di {context['public_area']} (risiko {context.get('risk', 0)*100:.0f}%)",
                'confidence': 0.6
            })
        
        return facts
    
    def _find_patterns(self, memories: List[Dict]) -> Dict:
        """Find patterns in memories"""
        patterns = {
            'favorite_topics': Counter(),
            'favorite_locations': Counter(),
            'favorite_positions': Counter(),
            'favorite_areas': Counter(),
            'emotional_patterns': Counter(),
            'time_patterns': Counter()
        }
        
        for mem in memories:
            content = mem['content'].lower()
            context = mem.get('context', {})
            
            # Topic patterns (simple keywords)
            topics = ['kerja', 'kantor', 'rumah', 'keluarga', 'teman', 'cinta']
            for topic in topics:
                if topic in content:
                    patterns['favorite_topics'][topic] += 1
            
            # Location patterns
            if context.get('location'):
                patterns['favorite_locations'][context['location']] += 1
            
            # Sexual patterns (V81)
            if context.get('position'):
                patterns['favorite_positions'][context['position']] += 1
            if context.get('area'):
                patterns['favorite_areas'][context['area']] += 1
            
            # Emotional patterns
            if context.get('mood'):
                patterns['emotional_patterns'][context['mood']] += 1
            
            # Time patterns
            hour = mem['timestamp'].hour
            if hour < 12:
                patterns['time_patterns']['morning'] += 1
            elif hour < 18:
                patterns['time_patterns']['afternoon'] += 1
            else:
                patterns['time_patterns']['evening'] += 1
        
        return patterns
    
    def _create_summary(self, memories: List[Dict], important: List[Dict], patterns: Dict) -> Optional[str]:
        """Create a summary of recent memories"""
        if not memories:
            return None
        
        # Get top emotions
        emotions = Counter(m['emotion'] for m in memories if m.get('emotion'))
        top_emotion = emotions.most_common(1)[0][0] if emotions else 'netral'
        
        # Get top locations
        locations = Counter(m['context'].get('location') for m in memories if m['context'].get('location'))
        top_location = locations.most_common(1)[0][0] if locations else 'berbagai tempat'
        
        # Get top positions (V81)
        positions = patterns['favorite_positions'].most_common(1)
        position_text = f", favorit posisi {positions[0][0]}" if positions else ""
        
        # Create summary
        summary = f"Hari ini banyak momen {top_emotion} di {top_location}{position_text}. "
        summary += f"Total {len(memories)} interaksi, "
        summary += f"{len(important)} momen penting, "
        summary += f"{patterns['favorite_topics'].most_common(1)[0][0] if patterns['favorite_topics'] else 'berbagai topik'} jadi bahasan utama."
        
        return summary
    
    async def auto_consolidation_loop(self):
        """Auto consolidation loop (runs in background)"""
        logger.info("🔄 Starting auto consolidation loop (every hour check)")
        while True:
            await asyncio.sleep(3600)  # Check every hour
            await self.consolidate()


__all__ = ['MemoryConsolidation']
