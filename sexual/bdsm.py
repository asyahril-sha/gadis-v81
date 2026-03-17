#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
BDSM DYNAMICS
=============================================================================
Bondage, Discipline, Dominance, Submission, Sadism, Masochism
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime


class BDSMRole(Enum):
    """Peran dalam BDSM"""
    DOMINANT = "dominant"
    SUBMISSIVE = "submissive"
    SWITCH = "switch"
    SADIST = "sadist"
    MASOCHIST = "masochist"
    MASTER = "master"
    SLAVE = "slave"
    TOP = "top"
    BOTTOM = "bottom"
    RIGGER = "rigger"  # Ahli bondage
    ROPE_BUNNY = "rope_bunny"  # Penerima bondage


class BDSMLevel(Enum):
    """Level pengalaman BDSM"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class BondageType(Enum):
    """Jenis bondage"""
    ROPE = "rope"  # Shibari / Kinbaku
    CUFFS = "cuffs"  # Borgol
    SPREADER = "spreader"  # Spread bar
    COLLAR = "collar"  # Kalung
    LEASH = "leash"  # Tali
    GAG = "gag"  # Sumbat mulut
    BLINDFOLD = "blindfold"  # Penutup mata
    CHAINS = "chains"  # Rantai
    TAPE = "tape"  # Lakban


class ImpactPlay(Enum):
    """Alat untuk impact play"""
    HAND = "hand"  # Tangan
    PADDLE = "paddle"  # Dayung
    WHIP = "whip"  # Cambuk
    FLOGGER = "flogger"  # Cambuk bertali
    CANE = "cane"  # Rotan
    BELT = "belt"  # Ikat pinggang


class TemperaturePlay(Enum):
    """Temperature play"""
    ICE = "ice"  # Es
    WAX = "wax"  # Lilin
    COOLING_GEL = "cooling_gel"
    WARMING_GEL = "warming_gel"


class BDSMDynamic:
    """
    BDSM dynamics antara dua pihak
    """
    
    def __init__(self, dominant_id: int, submissive_id: int):
        self.dominant_id = dominant_id
        self.submissive_id = submissive_id
        
        # Dynamic info
        self.start_date = datetime.now()
        self.dynamic_type = "24/7" if random.random() < 0.3 else "scene_only"
        
        # Rules and limits
        self.rules = []
        self.hard_limits = []
        self.soft_limits = []
        self.safe_words = ["merah", "stop", "aman"]
        
        # Protocols
        self.protocols = []
        
        # Tracking
        self.scenes = []
        self.total_scenes = 0
        self.last_scene = None
        
        # Training progress
        self.training_level = 1
        self.training_progress = 0.0
        
        # Trust level (0-1)
        self.trust_level = 0.5
    
    def add_rule(self, rule: str):
        """Add BDSM rule"""
        self.rules.append({
            'rule': rule,
            'added_at': datetime.now().isoformat(),
            'enforced': True
        })
    
    def add_limit(self, limit: str, is_hard: bool = True):
        """Add limit (hard or soft)"""
        limit_entry = {
            'limit': limit,
            'added_at': datetime.now().isoformat()
        }
        
        if is_hard:
            self.hard_limits.append(limit_entry)
        else:
            self.soft_limits.append(limit_entry)
    
    def add_safe_word(self, word: str):
        """Add safe word"""
        if word not in self.safe_words:
            self.safe_words.append(word)
    
    def start_scene(self, scene_type: str, intensity: int = 1):
        """Start BDSM scene"""
        scene = {
            'id': len(self.scenes) + 1,
            'type': scene_type,
            'intensity': intensity,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'activities': [],
            'aftercare': [],
            'notes': ''
        }
        
        self.scenes.append(scene)
        self.last_scene = datetime.now()
        
        return scene
    
    def end_scene(self, scene_id: int, aftercare: List[str] = None):
        """End BDSM scene with aftercare"""
        for scene in self.scenes:
            if scene['id'] == scene_id and scene['end_time'] is None:
                scene['end_time'] = datetime.now().isoformat()
                if aftercare:
                    scene['aftercare'] = aftercare
                
                self.total_scenes += 1
                
                # Calculate duration
                start = datetime.fromisoformat(scene['start_time'])
                end = datetime.now()
                scene['duration'] = (end - start).total_seconds() / 60
                
                return scene
        
        return None
    
    def add_activity(self, scene_id: int, activity: str, duration: int = None):
        """Add activity to scene"""
        for scene in self.scenes:
            if scene['id'] == scene_id and scene['end_time'] is None:
                scene['activities'].append({
                    'activity': activity,
                    'timestamp': datetime.now().isoformat(),
                    'duration': duration
                })
                return True
        
        return False
    
    def update_training(self, progress: float):
        """Update training progress"""
        self.training_progress += progress
        
        # Level up if progress reaches 100%
        while self.training_progress >= 1.0:
            self.training_level += 1
            self.training_progress -= 1.0
    
    def check_consent(self, activity: str) -> Tuple[bool, str]:
        """Check if activity is within limits"""
        # Check hard limits
        for limit in self.hard_limits:
            if limit['limit'].lower() in activity.lower():
                return False, f"Hard limit: {limit['limit']}"
        
        # Check soft limits (bisa dilanggar dengan negosiasi)
        for limit in self.soft_limits:
            if limit['limit'].lower() in activity.lower():
                return True, f"Soft limit: {limit['limit']} (perlu negosiasi)"
        
        return True, "Within limits"
    
    def get_summary(self) -> Dict:
        """Get BDSM dynamic summary"""
        return {
            'dominant_id': self.dominant_id,
            'submissive_id': self.submissive_id,
            'dynamic_type': self.dynamic_type,
            'duration_days': (datetime.now() - self.start_date).days,
            'total_scenes': self.total_scenes,
            'last_scene': self.last_scene.isoformat() if self.last_scene else None,
            'training_level': self.training_level,
            'trust_level': round(self.trust_level, 2),
            'rules_count': len(self.rules),
            'hard_limits_count': len(self.hard_limits),
            'soft_limits_count': len(self.soft_limits),
            'safe_words': self.safe_words
        }


class BondageSession:
    """Sesi bondage khusus"""
    
    def __init__(self, rigger_id: int, bunny_id: int):
        self.rigger_id = rigger_id  # Yang mengikat
        self.bunny_id = bunny_id  # Yang diikat
        self.rope_type = "jute"  # Jute, hemp, cotton, etc
        self.ties = []
        self.duration = 0
        self.intensity = 1
        self.start_time = None
        self.end_time = None
        
        # Safety
        self.safety_shears_available = True
        self.check_in_interval = 10  # minutes
        self.last_check_in = None
    
    def start_session(self, rope_type: str = "jute"):
        """Start bondage session"""
        self.rope_type = rope_type
        self.start_time = datetime.now()
        self.last_check_in = datetime.now()
        
        return {
            'start_time': self.start_time.isoformat(),
            'rope_type': rope_type,
            'safety_shears': self.safety_shears_available
        }
    
    def add_tie(self, tie_name: str, position: str, duration: int = None):
        """Add a tie to session"""
        tie = {
            'name': tie_name,
            'position': position,
            'time_applied': datetime.now().isoformat(),
            'duration': duration,
            'removed': False
        }
        
        self.ties.append(tie)
        
        return tie
    
    def remove_tie(self, tie_index: int):
        """Remove a tie"""
        if 0 <= tie_index < len(self.ties):
            self.ties[tie_index]['removed'] = True
            self.ties[tie_index]['time_removed'] = datetime.now().isoformat()
            return True
        return False
    
    def check_in(self):
        """Safety check-in"""
        now = datetime.now()
        self.last_check_in = now
        
        minutes_since = (now - self.start_time).total_seconds() / 60
        
        return {
            'time': now.isoformat(),
            'minutes_elapsed': round(minutes_since, 1),
            'ties_active': sum(1 for t in self.ties if not t['removed'])
        }
    
    def end_session(self):
        """End bondage session"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds() / 60
        
        # Remove all remaining ties
        for tie in self.ties:
            if not tie['removed']:
                tie['removed'] = True
                tie['time_removed'] = self.end_time.isoformat()
        
        return {
            'duration': round(self.duration, 1),
            'total_ties': len(self.ties),
            'end_time': self.end_time.isoformat()
        }


class Aftercare:
    """Aftercare setelah scene BDSM"""
    
    def __init__(self):
        self.activities = [
            "cuddling",
            "blankets",
            "warm_drinks",
            "chocolate",
            "massage",
            "talking",
            "music",
            "shower"
        ]
        
        self.physical_needs = [
            "check_rope_marks",
            "moisturizer",
            "warm_compress",
            "stretching",
            "hydration"
        ]
        
        self.emotional_needs = [
            "reassurance",
            "praise",
            "debriefing",
            "validation",
            "quiet_time"
        ]
    
    def get_aftercare_plan(self, scene_intensity: int, 
                          involved_activities: List[str]) -> List[str]:
        """Generate aftercare plan based on scene"""
        plan = []
        
        # Basic aftercare always needed
        plan.append("cuddling")
        plan.append("hydration")
        
        # More intense scene = more aftercare
        if scene_intensity >= 3:
            plan.extend(["blankets", "warm_drinks", "chocolate"])
        
        if scene_intensity >= 5:
            plan.extend(["massage", "quiet_time", "debriefing"])
        
        # Activity-specific aftercare
        if any('rope' in act for act in involved_activities):
            plan.append("check_rope_marks")
            plan.append("moisturizer")
        
        if any('impact' in act for act in involved_activities):
            plan.append("warm_compress")
            plan.append("arnica")
        
        return list(set(plan))  # Remove duplicates
    
    def check_readiness(self, aftercare_done: List[str], 
                        scene_intensity: int) -> bool:
        """Check if aftercare is complete"""
        needed = self.get_aftercare_plan(scene_intensity, [])
        
        # Check if all basic needs met
        basic_needs = ["cuddling", "hydration"]
        for need in basic_needs:
            if need not in aftercare_done:
                return False
        
        # For intense scenes, need more
        if scene_intensity >= 3:
            intense_needs = ["blankets", "warm_drinks"]
            if not all(need in aftercare_done for need in intense_needs):
                return False
        
        return True


# ===== BDSM DATABASE =====

BDSM_DYNAMICS = {
    'roles': [r.value for r in BDSMRole],
    'bondage_types': [b.value for b in BondageType],
    'impact_tools': [i.value for i in ImpactPlay],
    'temperature_play': [t.value for t in TemperaturePlay]
}


class BDSMManager:
    """Manager untuk BDSM dynamics"""
    
    def __init__(self):
        self.dynamics: Dict[str, BDSMDynamic] = {}  # f"{dom}_{sub}" -> dynamic
        self.bondage_sessions: Dict[int, BondageSession] = {}
        self.aftercare = Aftercare()
    
    def create_dynamic(self, dominant_id: int, submissive_id: int) -> BDSMDynamic:
        """Create new BDSM dynamic"""
        key = f"{dominant_id}_{submissive_id}"
        if key not in self.dynamics:
            self.dynamics[key] = BDSMDynamic(dominant_id, submissive_id)
        return self.dynamics[key]
    
    def get_dynamic(self, dominant_id: int, submissive_id: int) -> Optional[BDSMDynamic]:
        """Get BDSM dynamic"""
        key = f"{dominant_id}_{submissive_id}"
        return self.dynamics.get(key)
    
    def start_bondage(self, rigger_id: int, bunny_id: int) -> BondageSession:
        """Start bondage session"""
        session = BondageSession(rigger_id, bunny_id)
        self.bondage_sessions[len(self.bondage_sessions)] = session
        return session
    
    def suggest_aftercare(self, scene_intensity: int, 
                         activities: List[str]) -> List[str]:
        """Suggest aftercare activities"""
        return self.aftercare.get_aftercare_plan(scene_intensity, activities)


__all__ = [
    'BDSMRole',
    'BDSMLevel',
    'BondageType',
    'ImpactPlay',
    'TemperaturePlay',
    'BDSMDynamic',
    'BondageSession',
    'Aftercare',
    'BDSMManager',
    'BDSM_DYNAMICS'
]
