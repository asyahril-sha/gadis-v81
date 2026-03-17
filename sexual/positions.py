#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEX POSITIONS
=============================================================================
50+ Sex Positions dengan deskripsi lengkap
⚠️ Konten dewasa (18+)
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field


class SexPosition(Enum):
    """50+ Sex Positions"""
    # ===== BASIC POSITIONS =====
    MISSIONARY = "missionary"
    DOGGY = "doggy"
    COWGIRL = "cowgirl"
    REVERSE_COWGIRL = "reverse_cowgirl"
    SPOONING = "spooning"
    LOTUS = "lotus"
    STANDING = "standing"
    
    # ===== VARIATIONS =====
    MISSIONARY_LEGS_UP = "missionary_legs_up"
    MISSIONARY_LEGS_SHOULDERS = "missionary_legs_shoulders"
    DEEP_DOGGY = "deep_doggy"
    DOGGY_BENT_OVER = "doggy_bent_over"
    COWGIRL_LEANING = "cowgirl_leaning"
    REVERSE_COWGIRL_LEANING = "reverse_cowgirl_leaning"
    
    # ===== SITTING POSITIONS =====
    CHAIR = "chair"
    REVERSE_CHAIR = "reverse_chair"
    LAP_DANCE = "lap_dance"
    REVERSE_LAP = "reverse_lap"
    TABLE = "table"
    
    # ===== STANDING POSITIONS =====
    WALL = "wall"
    REVERSE_WALL = "reverse_wall"
    LIFTED = "lifted"
    REVERSE_LIFTED = "reverse_lifted"
    
    # ===== ORAL POSITIONS =====
    SIXTY_NINE = "sixty_nine"
    SIXTY_NINE_SIDE = "sixty_nine_side"
    FACE_SITTING = "face_sitting"
    FACE_SITTING_REVERSE = "face_sitting_reverse"
    KNEELING_ORAL = "kneeling_oral"
    STANDING_ORAL = "standing_oral"
    
    # ===== SCISSORS POSITIONS =====
    SCISSORS = "scissors"
    REVERSE_SCISSORS = "reverse_scissors"
    TRIBAD = "tribad"
    
    # ===== ADVANCED POSITIONS =====
    WHEELBARROW = "wheelbarrow"
    WHEELBARROW_REVERSE = "wheelbarrow_reverse"
    BRIDGE = "bridge"
    DROP_ZONE = "drop_zone"
    PARALLEL = "parallel"
    CROSS = "cross"
    T_STAND = "t_stand"
    
    # ===== FLEXIBLE POSITIONS =====
    SPLIT = "split"
    BUTTERFLY = "butterfly"
    FROGGY = "froggy"
    PRONE_BONE = "prone_bone"
    CAT = "cat"
    COBRA = "cobra"
    
    # ===== BEDROOM POSITIONS =====
    BED_POST = "bed_post"
    BED_EDGE = "bed_edge"
    PILLOW_HIGH = "pillow_high"
    MATTRESS_EDGE = "mattress_edge"
    
    # ===== SHOWER POSITIONS =====
    SHOWER_WALL = "shower_wall"
    SHOWER_KNEELING = "shower_kneeling"
    SHOWER_SEATED = "shower_seated"
    
    # ===== CHAIR POSITIONS =====
    ARMCHAIR = "armchair"
    ARMCHAIR_REVERSE = "armchair_reverse"
    OTTOMAN = "ottoman"
    DESK_CHAIR = "desk_chair"
    
    # ===== FLOOR POSITIONS =====
    RUG = "rug"
    FLOOR_SPOON = "floor_spoon"
    FLOOR_SCISSORS = "floor_scissors"
    FLOOR_LOTUS = "floor_lotus"
    
    # ===== INTENSE POSITIONS =====
    AMAZON = "amazon"
    AMAZON_REVERSE = "amazon_reverse"
    DEEP_IMPACT = "deep_impact"
    FULL_NELSON = "full_nelson"
    HALF_NELSON = "half_nelson"
    
    # ===== ROMANTIC POSITIONS =====
    ROMANTIC_SPOON = "romantic_spoon"
    WRAPPED = "wrapped"
    HEART_TO_HEART = "heart_to_heart"
    EYE_CONTACT = "eye_contact"
    KISSING = "kissing_position"


@dataclass
class PositionDetail:
    """Detail untuk setiap posisi"""
    name: str
    display_name: str
    description: str
    difficulty: int  # 1-5
    intensity: float  # 0-1
    arousal_boost: float  # 0-1
    requires_flexibility: bool
    requires_strength: bool
    tags: List[str]
    image_url: Optional[str] = None
    guide_text: Optional[str] = None
    popularity: int = 0
    rating: float = 0.0


# ===== 50+ POSITIONS DATABASE =====
POSITIONS: Dict[SexPosition, PositionDetail] = {
    # ===== BASIC =====
    SexPosition.MISSIONARY: PositionDetail(
        name="missionary",
        display_name="Misionaris",
        description="Posisi klasik, tatap muka, intim. Cocok untuk pemula.",
        difficulty=1,
        intensity=0.5,
        arousal_boost=0.4,
        requires_flexibility=False,
        requires_strength=False,
        tags=["romantic", "basic", "intimate", "face_to_face"]
    ),
    
    SexPosition.DOGGY: PositionDetail(
        name="doggy",
        display_name="Doggy Style",
        description="Dari belakang, penetrasi dalam. Posisi favorit banyak pasangan.",
        difficulty=2,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=False,
        tags=["intense", "deep", "from_behind", "popular"]
    ),
    
    SexPosition.COWGIRL: PositionDetail(
        name="cowgirl",
        display_name="Cowgirl",
        description="Wanita di atas, kontrol penuh. Bisa atur kecepatan dan kedalaman.",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["woman_on_top", "control", "eye_contact"]
    ),
    
    SexPosition.REVERSE_COWGIRL: PositionDetail(
        name="reverse_cowgirl",
        display_name="Reverse Cowgirl",
        description="Wanita di atas membelakangi, stimulasi berbeda.",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["woman_on_top", "reverse", "back_view"]
    ),
    
    SexPosition.SPOONING: PositionDetail(
        name="spooning",
        display_name="Spooning",
        description="Berbaring miring seperti sendok, intim dan nyaman.",
        difficulty=1,
        intensity=0.4,
        arousal_boost=0.5,
        requires_flexibility=False,
        requires_strength=False,
        tags=["romantic", "intimate", "cuddly", "slow"]
    ),
    
    SexPosition.LOTUS: PositionDetail(
        name="lotus",
        display_name="Lotus",
        description="Duduk berhadapan sambil memeluk, sangat intim.",
        difficulty=3,
        intensity=0.5,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["romantic", "intimate", "sitting", "face_to_face"]
    ),
    
    SexPosition.STANDING: PositionDetail(
        name="standing",
        display_name="Berdiri",
        description="Berdiri berhadapan, romantis tapi butuh tenaga.",
        difficulty=3,
        intensity=0.6,
        arousal_boost=0.5,
        requires_flexibility=False,
        requires_strength=True,
        tags=["standing", "romantic", "face_to_face"]
    ),
    
    # ===== VARIATIONS =====
    SexPosition.MISSIONARY_LEGS_UP: PositionDetail(
        name="missionary_legs_up",
        display_name="Misionaris Kaki Angkat",
        description="Kaki wanita diangkat, penetrasi lebih dalam.",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["missionary", "deep", "variation"]
    ),
    
    SexPosition.DEEP_DOGGY: PositionDetail(
        name="deep_doggy",
        display_name="Deep Doggy",
        description="Doggy dengan tubuh lebih rendah, penetrasi sangat dalam.",
        difficulty=2,
        intensity=0.9,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["doggy", "deep", "intense"]
    ),
    
    SexPosition.COWGIRL_LEANING: PositionDetail(
        name="cowgirl_leaning",
        display_name="Cowgirl Bersandar",
        description="Wanita bersandar ke belakang, stimulasi klitoris maksimal.",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=True,
        tags=["cowgirl", "clitoral", "control"]
    ),
    
    # ===== SITTING =====
    SexPosition.CHAIR: PositionDetail(
        name="chair",
        display_name="Kursi",
        description="Pria duduk, wanita di atas menghadap, nyaman.",
        difficulty=2,
        intensity=0.6,
        arousal_boost=0.5,
        requires_flexibility=False,
        requires_strength=False,
        tags=["sitting", "chair", "face_to_face"]
    ),
    
    SexPosition.REVERSE_CHAIR: PositionDetail(
        name="reverse_chair",
        display_name="Reverse Chair",
        description="Pria duduk, wanita membelakangi, variasi.",
        difficulty=2,
        intensity=0.6,
        arousal_boost=0.5,
        requires_flexibility=False,
        requires_strength=False,
        tags=["sitting", "chair", "reverse"]
    ),
    
    # ===== ORAL =====
    SexPosition.SIXTY_NINE: PositionDetail(
        name="sixty_nine",
        display_name="69",
        description="Saling oral bersamaan, stimulasi timbal balik.",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=False,
        tags=["oral", "mutual", "69"]
    ),
    
    SexPosition.FACE_SITTING: PositionDetail(
        name="face_sitting",
        display_name="Face Sitting",
        description="Wanita duduk di wajah pasangan, kontrol penuh.",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["oral", "woman_on_top", "control"]
    ),
    
    SexPosition.KNEELING_ORAL: PositionDetail(
        name="kneeling_oral",
        display_name="Kneeling Oral",
        description="Berlutut memberikan oral, posisi klasik.",
        difficulty=2,
        intensity=0.5,
        arousal_boost=0.5,
        requires_flexibility=False,
        requires_strength=False,
        tags=["oral", "kneeling"]
    ),
    
    # ===== SCISSORS =====
    SexPosition.SCISSORS: PositionDetail(
        name="scissors",
        display_name="Scissors",
        description="Posisi gunting, klitoris bergesekan.",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=True,
        tags=["scissors", "clitoral", "lesbian"]
    ),
    
    # ===== ADVANCED =====
    SexPosition.WHEELBARROW: PositionDetail(
        name="wheelbarrow",
        display_name="Wheelbarrow",
        description="Kaki wanita dipegang seperti gerobak dorong.",
        difficulty=4,
        intensity=0.9,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=True,
        tags=["advanced", "intense", "acrobatic"]
    ),
    
    SexPosition.BRIDGE: PositionDetail(
        name="bridge",
        display_name="Bridge",
        description="Wanita melengkung seperti jembatan.",
        difficulty=5,
        intensity=0.9,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=True,
        tags=["advanced", "flexible", "intense"]
    ),
    
    SexPosition.PRONE_BONE: PositionDetail(
        name="prone_bone",
        display_name="Prone Bone",
        description="Wanita tengkurap, pria di atas dari belakang.",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["prone", "from_behind", "intimate"]
    ),
    
    # ===== INTENSE =====
    SexPosition.AMAZON: PositionDetail(
        name="amazon",
        display_name="Amazon",
        description="Wanita di atas dengan kaki melingkar, dominan.",
        difficulty=4,
        intensity=0.9,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=True,
        tags=["amazon", "dominant", "intense"]
    ),
    
    SexPosition.FULL_NELSON: PositionDetail(
        name="full_nelson",
        display_name="Full Nelson",
        description="Lengan pria melingkar di bawah lengan wanita.",
        difficulty=4,
        intensity=0.9,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=True,
        tags=["nelson", "dominant", "intense"]
    ),
    
    # ===== ROMANTIC =====
    SexPosition.ROMANTIC_SPOON: PositionDetail(
        name="romantic_spoon",
        display_name="Romantic Spoon",
        description="Spooning sambil berbisik, sangat intim.",
        difficulty=1,
        intensity=0.4,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=False,
        tags=["romantic", "spoon", "intimate", "slow"]
    ),
    
    SexPosition.HEART_TO_HEART: PositionDetail(
        name="heart_to_heart",
        display_name="Heart to Heart",
        description="Duduk berhadapan, dinding dada bertemu.",
        difficulty=2,
        intensity=0.5,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=False,
        tags=["romantic", "sitting", "face_to_face", "intimate"]
    ),
}


class PositionManager:
    """Manager untuk sex positions"""
    
    def __init__(self):
        self.positions = POSITIONS
    
    def get_position(self, position: SexPosition) -> Optional[PositionDetail]:
        """Get position details"""
        return self.positions.get(position)
    
    def get_all_positions(self) -> List[Dict]:
        """Get all positions"""
        return [
            {
                'id': pos.value,
                'name': detail.display_name,
                'difficulty': detail.difficulty,
                'intensity': detail.intensity,
                'tags': detail.tags
            }
            for pos, detail in self.positions.items()
        ]
    
    def get_by_difficulty(self, level: int) -> List[SexPosition]:
        """Get positions by difficulty"""
        return [
            pos for pos, detail in self.positions.items()
            if detail.difficulty == level
        ]
    
    def get_by_intensity(self, min_intensity: float, max_intensity: float) -> List[SexPosition]:
        """Get positions by intensity range"""
        return [
            pos for pos, detail in self.positions.items()
            if min_intensity <= detail.intensity <= max_intensity
        ]
    
    def get_by_tags(self, tags: List[str]) -> List[SexPosition]:
        """Get positions by tags"""
        return [
            pos for pos, detail in self.positions.items()
            if any(tag in detail.tags for tag in tags)
        ]
    
    def get_random(self) -> SexPosition:
        """Get random position"""
        import random
        return random.choice(list(self.positions.keys()))
    
    def get_beginner_friendly(self) -> List[SexPosition]:
        """Get beginner friendly positions"""
        return self.get_by_difficulty(1)
    
    def get_intense_positions(self) -> List[SexPosition]:
        """Get intense positions"""
        return self.get_by_intensity(0.7, 1.0)
    
    def get_romantic_positions(self) -> List[SexPosition]:
        """Get romantic positions"""
        return self.get_by_tags(['romantic'])


# ===== GLOBAL INSTANCE =====
position_manager = PositionManager()


__all__ = [
    'SexPosition',
    'PositionDetail',
    'POSITIONS',
    'position_manager',
    'PositionManager'
]
