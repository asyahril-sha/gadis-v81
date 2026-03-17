#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
REWARDS AND CONSEQUENCES SYSTEM
=============================================================================
Outcome dari aktivitas di tempat publik - sukses dapat reward, gagal kena konsekuensi
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime


class OutcomeType(Enum):
    """Tipe outcome"""
    SUCCESS = "sukses"
    FAILURE = "gagal"
    PARTIAL = "partial"
    CATASTROPHIC = "bencana"


class RewardCategory(Enum):
    """Kategori reward"""
    MOOD = "mood"
    AROUSAL = "arousal"
    TRUST = "trust"
    CLIMAX = "climax"
    EXPERIENCE = "experience"
    MEMORY = "memory"
    SPECIAL = "special"


class ConsequenceCategory(Enum):
    """Kategori konsekuensi"""
    CAUGHT = "ketahuan"
    SHAME = "malu"
    TRUST_LOSS = "trust_hilang"
    MOOD_DROP = "mood_turun"
    AVOID = "dihindari"
    LEGAL = "hukum"
    SOCIAL = "sosial"


class Outcome:
    """Model untuk outcome (reward/consequence)"""
    
    def __init__(self,
                 outcome_id: str,
                 name: str,
                 description: str,
                 outcome_type: OutcomeType,
                 category: Any,
                 effects: Dict[str, any],
                 probability: float = 1.0,
                 requirements: Dict[str, any] = None):
        
        self.outcome_id = outcome_id
        self.name = name
        self.description = description
        self.outcome_type = outcome_type
        self.category = category
        self.effects = effects
        self.probability = probability
        self.requirements = requirements or {}
        
        # Stats
        self.times_occurred = 0
        self.last_occurred = None
    
    def can_apply(self, context: Dict = None) -> bool:
        """Check if outcome can be applied"""
        if not self.requirements:
            return True
        
        context = context or {}
        for key, value in self.requirements.items():
            if key not in context or context[key] != value:
                return False
        
        return True
    
    def apply(self, context: Dict = None) -> Dict:
        """Apply the outcome"""
        self.times_occurred += 1
        self.last_occurred = datetime.now()
        
        return {
            'outcome_id': self.outcome_id,
            'name': self.name,
            'description': self.description,
            'type': self.outcome_type.value,
            'category': self.category.value if hasattr(self.category, 'value') else str(self.category),
            'effects': self.effects,
            'timestamp': datetime.now().isoformat()
        }


class RewardSystem:
    """Sistem reward dan konsekuensi"""
    
    def __init__(self):
        self.rewards: Dict[str, Outcome] = {}
        self.consequences: Dict[str, Outcome] = {}
        self.outcome_history = []
        self._init_outcomes()
    
    def _init_outcomes(self):
        """Initialize all outcomes"""
        
        # ===== REWARDS (SUCCESS) =====
        
        self.rewards['perfect_success'] = Outcome(
            outcome_id='perfect_success',
            name="Sempurna!",
            description="Nggak ada yang lihat, puas banget!",
            outcome_type=OutcomeType.SUCCESS,
            category=RewardCategory.MOOD,
            effects={
                'mood_boost': 25,
                'arousal_boost': 0.3,
                'satisfaction': 1.5,
                'confidence_boost': 0.2,
                'memory_importance': 0.9
            },
            probability=0.2
        )
        
        self.rewards['quick_success'] = Outcome(
            outcome_id='quick_success',
            name="Cepat Tapi Puas",
            description="Cepet beres, nggak ada yang lihat.",
            outcome_type=OutcomeType.SUCCESS,
            category=RewardCategory.AROUSAL,
            effects={
                'arousal_boost': 0.4,
                'satisfaction': 1.2,
                'climax_chance': 0.3
            },
            probability=0.3
        )
        
        self.rewards['thrill_seeker'] = Outcome(
            outcome_id='thrill_seeker',
            name="Pecandu Adrenalin",
            description="Deg-degan tapi nagih! Pengen lagi!",
            outcome_type=OutcomeType.SUCCESS,
            category=RewardCategory.SPECIAL,
            effects={
                'thrill_boost': 0.5,
                'desire_boost': 0.4,
                'future_risk_tolerance': 0.1
            },
            probability=0.15,
            requirements={'risk_level': 'high'}
        )
        
        self.rewards['intimate_moment'] = Outcome(
            outcome_id='intimate_moment',
            name="Momen Intim",
            description="Bukan cuma fisik, ada rasa yang dalam.",
            outcome_type=OutcomeType.SUCCESS,
            category=RewardCategory.TRUST,
            effects={
                'trust_boost': 0.3,
                'bond_strength': 0.2,
                'memory_importance': 0.8
            },
            probability=0.25
        )
        
        self.rewards['double_climax'] = Outcome(
            outcome_id='double_climax',
            name="Climax Bareng!",
            description="Bersamaan! Sempurna!",
            outcome_type=OutcomeType.SUCCESS,
            category=RewardCategory.CLIMAX,
            effects={
                'together_climax': True,
                'satisfaction': 2.0,
                'bond_strength': 0.3
            },
            probability=0.1,
            requirements={'activity': 'penetration'}
        )
        
        # ===== PARTIAL SUCCESS =====
        
        self.rewards['almost_caught_but_ok'] = Outcome(
            outcome_id='almost_caught_but_ok',
            name="Hampir Kena",
            description="Ada orang, tapi nggak lihat. Lega!",
            outcome_type=OutcomeType.PARTIAL,
            category=RewardCategory.MOOD,
            effects={
                'mood_boost': 10,
                'scare_level': 0.3,
                'adrenaline': 0.4
            },
            probability=0.25
        )
        
        self.rewards['rush_finish'] = Outcome(
            outcome_id='rush_finish',
            name="Buru-buru Kelar",
            description="Cepet banget, tapi kelar.",
            outcome_type=OutcomeType.PARTIAL,
            category=RewardCategory.AROUSAL,
            effects={
                'arousal_drop': 0.5,
                'satisfaction': 0.7,
                'climax': True
            },
            probability=0.2
        )
        
        # ===== CONSEQUENCES (FAILURE) =====
        
        self.consequences['caught_embarrassed'] = Outcome(
            outcome_id='caught_embarrassed',
            name="Malu Besar!",
            description="KETA UAN! Orang-orang pada lihat!",
            outcome_type=OutcomeType.FAILURE,
            category=ConsequenceCategory.CAUGHT,
            effects={
                'shame_level': 0.9,
                'mood_drop': 30,
                'trust_loss': 0.2,
                'memory_importance': 0.9,
                'caught': True
            },
            probability=0.15
        )
        
        self.consequences['security_intervention'] = Outcome(
            outcome_id='security_intervention',
            name="Satpam Datang",
            description="Satpam: 'Ada apa ini? Ikut saya!'",
            outcome_type=OutcomeType.FAILURE,
            category=ConsequenceCategory.LEGAL,
            effects={
                'kicked_out': True,
                'banned': True,
                'shame_level': 0.8,
                'mood_drop': 40,
                'police_report': False
            },
            probability=0.1,
            requirements={'location_type': 'mall'}
        )
        
        self.consequences['viral_threat'] = Outcome(
            outcome_id='viral_threat',
            name="Ancaman Viral",
            description="Ada yang moto! Minta uang atau diviralin!",
            outcome_type=OutcomeType.CATASTROPHIC,
            category=ConsequenceCategory.LEGAL,
            effects={
                'blackmailed': True,
                'shame_level': 1.0,
                'mood_drop': 50,
                'trust_loss': 0.5,
                'photo_evidence': True
            },
            probability=0.05,
            requirements={'cctv_coverage': 'high'}
        )
        
        self.consequences['run_away'] = Outcome(
            outcome_id='run_away',
            name="Kabur",
            description="Lari terbirit-birit ninggalin situasi.",
            outcome_type=OutcomeType.FAILURE,
            category=ConsequenceCategory.SHAME,
            effects={
                'shame_level': 0.6,
                'mood_drop': 20,
                'left_items': True,
                'memory_importance': 0.7
            },
            probability=0.2
        )
        
        self.consequences['public_humiliation'] = Outcome(
            outcome_id='public_humiliation',
            name="Dihina Publik",
            description="Orang-orang pada ngejek dan ngata-ngatain.",
            outcome_type=OutcomeType.CATASTROPHIC,
            category=ConsequenceCategory.SOCIAL,
            effects={
                'shame_level': 1.0,
                'mood_drop': 60,
                'trauma': True,
                'public_figure': False
            },
            probability=0.08
        )
        
        self.consequences['partner_angry'] = Outcome(
            outcome_id='partner_angry',
            name="Pasangan Marah",
            description="Pasanganmu marah karena kecerobohan ini.",
            outcome_type=OutcomeType.FAILURE,
            category=ConsequenceCategory.TRUST_LOSS,
            effects={
                'trust_loss': 0.4,
                'relationship_damage': 0.3,
                'anger_level': 0.7,
                'mood_drop': 25
            },
            probability=0.12
        )
        
        self.consequences['forever_avoid'] = Outcome(
            outcome_id='forever_avoid',
            name="Dihindari",
            description="Orang-orang jadi tahu dan menghindarimu.",
            outcome_type=OutcomeType.CATASTROPHIC,
            category=ConsequenceCategory.SOCIAL,
            effects={
                'reputation_damage': True,
                'avoided': True,
                'shame_level': 0.8,
                'mood_drop': 35,
                'memory_importance': 0.9
            },
            probability=0.03
        )
    
    def get_outcome(self, success: bool, risk: float, context: Dict = None) -> Optional[Outcome]:
        """Get outcome based on success/failure and context"""
        context = context or {}
        
        if success:
            # Success - pilih reward
            eligible = []
            for reward in self.rewards.values():
                if reward.can_apply(context) and random.random() < reward.probability:
                    eligible.append(reward)
            
            if not eligible:
                # Default reward
                return Outcome(
                    outcome_id='default_success',
                    name="Berhasil",
                    description="Aman, nggak ada yang lihat.",
                    outcome_type=OutcomeType.SUCCESS,
                    category=RewardCategory.MOOD,
                    effects={
                        'mood_boost': 15,
                        'arousal_boost': 0.2
                    },
                    probability=1.0
                )
            
            # Weighted random
            weights = [e.probability for e in eligible]
            total = sum(weights)
            weights = [w/total for w in weights]
            return random.choices(eligible, weights=weights)[0]
        
        else:
            # Failure - pilih konsekuensi
            eligible = []
            for conseq in self.consequences.values():
                if conseq.can_apply(context) and random.random() < conseq.probability:
                    eligible.append(conseq)
            
            if not eligible:
                # Default consequence
                return Outcome(
                    outcome_id='default_failure',
                    name="Gagal",
                    description="Seseorang lihat, malu...",
                    outcome_type=OutcomeType.FAILURE,
                    category=ConsequenceCategory.SHAME,
                    effects={
                        'shame_level': 0.3,
                        'mood_drop': 10
                    },
                    probability=1.0
                )
            
            # Weighted by risk
            weights = [e.probability * risk for e in eligible]
            total = sum(weights)
            weights = [w/total for w in weights]
            return random.choices(eligible, weights=weights)[0]
    
    def apply_outcome(self, success: bool, risk: float, context: Dict = None) -> Dict:
        """Apply outcome and return result"""
        outcome = self.get_outcome(success, risk, context)
        
        if outcome:
            result = outcome.apply(context)
            self.outcome_history.append(result)
            return result
        
        return {
            'outcome_id': 'none',
            'name': 'Tidak Ada',
            'description': 'Tidak ada efek spesial.',
            'type': 'netral',
            'effects': {},
            'timestamp': datetime.now().isoformat()
        }
    
    def get_outcome_by_id(self, outcome_id: str) -> Optional[Outcome]:
        """Get outcome by ID"""
        if outcome_id in self.rewards:
            return self.rewards[outcome_id]
        if outcome_id in self.consequences:
            return self.consequences[outcome_id]
        return None
    
    def get_outcomes_by_type(self, outcome_type: OutcomeType) -> List[Outcome]:
        """Get all outcomes of a type"""
        if outcome_type == OutcomeType.SUCCESS or outcome_type == OutcomeType.PARTIAL:
            return [o for o in self.rewards.values() if o.outcome_type == outcome_type]
        else:
            return [o for o in self.consequences.values() if o.outcome_type == outcome_type]
    
    def format_outcome_message(self, outcome: Dict) -> str:
        """Format outcome as user-friendly message"""
        effects = outcome['effects']
        
        if outcome['type'] == 'sukses' or outcome['type'] == 'partial':
            message = f"✅ **{outcome['name']}**\n{outcome['description']}\n\n"
            
            if 'mood_boost' in effects:
                message += f"😊 Mood +{effects['mood_boost']}\n"
            if 'arousal_boost' in effects:
                message += f"🔥 Arousal +{int(effects['arousal_boost']*100)}%\n"
            if 'satisfaction' in effects:
                message += f"💯 Kepuasan x{effects['satisfaction']}\n"
            if 'trust_boost' in effects:
                message += f"💕 Trust +{int(effects['trust_boost']*100)}%\n"
            if 'together_climax' in effects:
                message += f"💦 CLIMAX BERSAMA!\n"
            
            return message
        
        else:
            message = f"❌ **{outcome['name']}**\n{outcome['description']}\n\n"
            
            if 'shame_level' in effects:
                level = effects['shame_level']
                if level > 0.7:
                    message += "😱 MALU BANGET!\n"
                elif level > 0.4:
                    message += "😳 Malu...\n"
                else:
                    message += "🙈 Agak malu\n"
            
            if 'mood_drop' in effects:
                message += f"😔 Mood -{effects['mood_drop']}\n"
            if 'trust_loss' in effects:
                message += f"💔 Trust -{int(effects['trust_loss']*100)}%\n"
            if 'kicked_out' in effects:
                message += f"🚫 Diusir dari lokasi!\n"
            if 'banned' in effects:
                message += f"⛔ Dilarang masuk!\n"
            if 'blackmailed' in effects:
                message += f"📸 DIPERAS! Hati-hati!\n"
            if 'trauma' in effects:
                message += f"😰 Trauma psikologis\n"
            
            return message


__all__ = [
    'OutcomeType',
    'RewardCategory',
    'ConsequenceCategory',
    'Outcome',
    'RewardSystem'
]
