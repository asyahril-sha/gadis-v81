#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEX POSITIONS DATABASE
=============================================================================
50+ Sex Positions dengan deskripsi lengkap
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class SexPosition(Enum):
    """50+ Sex Positions"""
    # Basic Positions
    MISSIONARY = "missionary"
    DOGGY = "doggy"
    COWGIRL = "cowgirl"
    REVERSE_COWGIRL = "reverse_cowgirl"
    SPOONING = "spooning"
    LOTUS = "lotus"
    
    # Standing Positions
    STANDING = "standing"
    WALL = "wall"
    TABLE = "table"
    CHAIR = "chair"
    
    # Advanced Positions
    SIXTY_NINE = "sixty_nine"
    SCISSORS = "scissors"
    WHEELBARROW = "wheelbarrow"
    BRIDGE = "bridge"
    
    # Intimate Positions
    FACE_TO_FACE = "face_to_face"
    LAP_DANCE = "lap_dance"
    PRONE_BONE = "prone_bone"
    BUTTERFLY = "butterfly"
    
    # More Positions
    AMAZON = "amazon"
    CRAB = "crab"
    CRADLE = "cradle"
    CROSS = "cross"
    DEEP_IMPACT = "deep_impact"
    DIPPER = "dipper"
    DOGGY_STYLE = "doggy_style"
    DRAGON = "dragon"
    ELEVATOR = "elevator"
    FROGGY = "froggy"
    G_STAND = "g_stand"
    HAMMER = "hammer"
    HORSEMAN = "horseman"
    HULA = "hula"
    JELLYFISH = "jellyfish"
    KNOT = "knot"
    LADDER = "ladder"
    LAP_DANCE_V2 = "lap_dance_v2"
    LIZARD = "lizard"
    MANTIS = "mantis"
    MIRROR = "mirror"
    MONKEY = "monkey"
    OCTOPUS = "octopus"
    PENDULUM = "pendulum"
    PYRAMID = "pyramid"
    QUEEN = "queen"
    ROCKING_CHAIR = "rocking_chair"
    ROPE = "rope"
    SADDLE = "saddle"
    SCORPION = "scorpion"
    SNAKE = "snake"
    SPIDER = "spider"
    STAIRS = "stairs"
    SUNSET = "sunset"
    SWING = "swing"
    TIGER = "tiger"
    TWISTER = "twister"
    UNICORN = "unicorn"
    VENUS = "venus"
    WATERFALL = "waterfall"
    X_POSITION = "x_position"
    YOGA = "yoga"
    ZEBRA = "zebra"


@dataclass
class PositionDetail:
    """Detail untuk setiap posisi"""
    id: str
    name: str
    description: str
    difficulty: int  # 1-5
    intensity: float  # 0-1
    arousal_boost: float  # 0-1
    requires_flexibility: bool
    requires_strength: bool
    tags: List[str]
    image_url: Optional[str] = None
    guide_text: Optional[str] = None


# ===== 50+ POSITIONS DATABASE =====
POSITIONS: Dict[SexPosition, PositionDetail] = {
    SexPosition.MISSIONARY: PositionDetail(
        id="pos_001",
        name="Misionaris",
        description="Posisi klasik, tatap muka, intim",
        difficulty=1,
        intensity=0.5,
        arousal_boost=0.4,
        requires_flexibility=False,
        requires_strength=False,
        tags=["romantic", "classic", "intimate"]
    ),
    SexPosition.DOGGY: PositionDetail(
        id="pos_002",
        name="Doggy Style",
        description="Dari belakang, penetrasi dalam",
        difficulty=2,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=True,
        tags=["intense", "deep", "animalistic"]
    ),
    SexPosition.COWGIRL: PositionDetail(
        id="pos_003",
        name="Cowgirl",
        description="Wanita di atas, kontrol penuh",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["woman_on_top", "control", "intimate"]
    ),
    SexPosition.REVERSE_COWGIRL: PositionDetail(
        id="pos_004",
        name="Reverse Cowgirl",
        description="Wanita di atas membelakangi",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["woman_on_top", "view", "intense"]
    ),
    SexPosition.SPOONING: PositionDetail(
        id="pos_005",
        name="Spooning",
        description="Berbaring menyamping, nyaman",
        difficulty=1,
        intensity=0.4,
        arousal_boost=0.5,
        requires_flexibility=False,
        requires_strength=False,
        tags=["comfortable", "intimate", "lazy"]
    ),
    SexPosition.LOTUS: PositionDetail(
        id="pos_006",
        name="Lotus",
        description="Duduk berhadapan, sangat intim",
        difficulty=3,
        intensity=0.6,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=False,
        tags=["intimate", "romantic", "spiritual"]
    ),
    SexPosition.STANDING: PositionDetail(
        id="pos_007",
        name="Berdiri",
        description="Berdiri berhadapan",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["standing", "quickie", "wall"]
    ),
    SexPosition.WALL: PositionDetail(
        id="pos_008",
        name="Wall",
        description="Perempuan di sandar ke dinding",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=True,
        tags=["wall", "passionate", "support"]
    ),
    SexPosition.TABLE: PositionDetail(
        id="pos_009",
        name="Table",
        description="Diatas meja",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=False,
        tags=["furniture", "variation", "fun"]
    ),
    SexPosition.CHAIR: PositionDetail(
        id="pos_010",
        name="Chair",
        description="Duduk di kursi",
        difficulty=2,
        intensity=0.6,
        arousal_boost=0.5,
        requires_flexibility=False,
        requires_strength=False,
        tags=["chair", "sitting", "intimate"]
    ),
    SexPosition.SIXTY_NINE: PositionDetail(
        id="pos_011",
        name="69",
        description="Saling oral bersama",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.9,
        requires_flexibility=True,
        requires_strength=False,
        tags=["oral", "mutual", "simultaneous"]
    ),
    SexPosition.SCISSORS: PositionDetail(
        id="pos_012",
        name="Scissors",
        description="Posisi gunting untuk lesbian",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=False,
        tags=["lesbian", "tribadism", "intimate"]
    ),
    SexPosition.WHEELBARROW: PositionDetail(
        id="pos_013",
        name="Wheelbarrow",
        description="Pria memegang kaki wanita",
        difficulty=4,
        intensity=0.9,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["acrobatic", "intense", "fun"]
    ),
    SexPosition.BRIDGE: PositionDetail(
        id="pos_014",
        name="Bridge",
        description="Wanita melengkung seperti jembatan",
        difficulty=5,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=True,
        tags=["flexible", "acrobatic", "challenge"]
    ),
    SexPosition.FACE_TO_FACE: PositionDetail(
        id="pos_015",
        name="Face to Face",
        description="Berhadapan, sangat intim",
        difficulty=2,
        intensity=0.6,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=False,
        tags=["intimate", "romantic", "kissing"]
    ),
    SexPosition.LAP_DANCE: PositionDetail(
        id="pos_016",
        name="Lap Dance",
        description="Wanita di atas pangkuan",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["lap", "grinding", "tease"]
    ),
    SexPosition.PRONE_BONE: PositionDetail(
        id="pos_017",
        name="Prone Bone",
        description="Wanita tengkurap, pria di atas",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["prone", "deep", "control"]
    ),
    SexPosition.BUTTERFLY: PositionDetail(
        id="pos_018",
        name="Butterfly",
        description="Kaki diangkat, seperti kupu",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=False,
        tags=["flexible", "deep", "intimate"]
    ),
    SexPosition.AMAZON: PositionDetail(
        id="pos_019",
        name="Amazon",
        description="Wania di atas dengan kaki lurus",
        difficulty=4,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=True,
        tags=["amazon", "woman_on_top", "control"]
    ),
    SexPosition.CRAB: PositionDetail(
        id="pos_020",
        name="Crab",
        description="Posisi seperti kepiting",
        difficulty=4,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["animal", "unique", "challenge"]
    ),
    SexPosition.CRADLE: PositionDetail(
        id="pos_021",
        name="Cradle",
        description="Wanita digendong",
        difficulty=4,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["cradle", "intimate", "romantic"]
    ),
    SexPosition.CROSS: PositionDetail(
        id="pos_022",
        name="Cross",
        description="Menyilang",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["cross", "variation", "unique"]
    ),
    SexPosition.DEEP_IMPACT: PositionDetail(
        id="pos_023",
        name="Deep Impact",
        description="Penetrasi sangat dalam",
        difficulty=3,
        intensity=0.9,
        arousal_boost=0.9,
        requires_flexibility=True,
        requires_strength=False,
        tags=["deep", "intense", "passionate"]
    ),
    SexPosition.DIPPER: PositionDetail(
        id="pos_024",
        name="Dipper",
        description="Seperti gayung",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["dipper", "unique", "fun"]
    ),
    SexPosition.DRAGON: PositionDetail(
        id="pos_025",
        name="Dragon",
        description="Posisi naga, eksotis",
        difficulty=4,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=True,
        tags=["dragon", "exotic", "mythical"]
    ),
    SexPosition.ELEVATOR: PositionDetail(
        id="pos_026",
        name="Elevator",
        description="Naik turun seperti lift",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["elevator", "rhythmic", "control"]
    ),
    SexPosition.FROGGY: PositionDetail(
        id="pos_027",
        name="Froggy",
        description="Seperti katak",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=False,
        tags=["froggy", "animal", "unique"]
    ),
    SexPosition.G_STAND: PositionDetail(
        id="pos_028",
        name="G-Stand",
        description="Posisi untuk stimulasi G-spot",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.9,
        requires_flexibility=True,
        requires_strength=False,
        tags=["gspot", "stimulation", "intense"]
    ),
    SexPosition.HAMMER: PositionDetail(
        id="pos_029",
        name="Hammer",
        description="Pukulan seperti palu",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=True,
        tags=["hammer", "intense", "powerful"]
    ),
    SexPosition.HORSEMAN: PositionDetail(
        id="pos_030",
        name="Horseman",
        description="Seperti menunggang kuda",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=True,
        tags=["horseman", "rhythmic", "control"]
    ),
    SexPosition.HULA: PositionDetail(
        id="pos_031",
        name="Hula",
        description="Gerakan seperti hula",
        difficulty=3,
        intensity=0.6,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["hula", "dance", "rhythmic"]
    ),
    SexPosition.JELLYFISH: PositionDetail(
        id="pos_032",
        name="Jellyfish",
        description="Seperti ubur-ubur",
        difficulty=4,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["jellyfish", "unique", "fluid"]
    ),
    SexPosition.KNOT: PositionDetail(
        id="pos_033",
        name="Knot",
        description="Mengikat, untuk BDSM",
        difficulty=4,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=False,
        tags=["bdsm", "bondage", "knot"]
    ),
    SexPosition.LADDER: PositionDetail(
        id="pos_034",
        name="Ladder",
        description="Seperti tangga",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["ladder", "unique", "fun"]
    ),
    SexPosition.LAP_DANCE_V2: PositionDetail(
        id="pos_035",
        name="Lap Dance V2",
        description="Variasi lap dance",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=True,
        tags=["lap", "dance", "variation"]
    ),
    SexPosition.LIZARD: PositionDetail(
        id="pos_036",
        name="Lizard",
        description="Seperti kadal",
        difficulty=3,
        intensity=0.6,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["lizard", "animal", "unique"]
    ),
    SexPosition.MANTIS: PositionDetail(
        id="pos_037",
        name="Mantis",
        description="Seperti belalang sembah",
        difficulty=4,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["mantis", "animal", "unique"]
    ),
    SexPosition.MIRROR: PositionDetail(
        id="pos_038",
        name="Mirror",
        description="Di depan cermin",
        difficulty=2,
        intensity=0.8,
        arousal_boost=0.9,
        requires_flexibility=False,
        requires_strength=False,
        tags=["mirror", "visual", "sexy"]
    ),
    SexPosition.MONKEY: PositionDetail(
        id="pos_039",
        name="Monkey",
        description="Seperti monyet",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["monkey", "animal", "fun"]
    ),
    SexPosition.OCTOPUS: PositionDetail(
        id="pos_040",
        name="Octopus",
        description="Banyak tangan seperti gurita",
        difficulty=4,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=False,
        tags=["octopus", "unique", "kinky"]
    ),
    SexPosition.PENDULUM: PositionDetail(
        id="pos_041",
        name="Pendulum",
        description="Gerakan seperti bandul",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["pendulum", "rhythmic", "unique"]
    ),
    SexPosition.PYRAMID: PositionDetail(
        id="pos_042",
        name="Pyramid",
        description="Posisi piramida",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["pyramid", "unique", "challenge"]
    ),
    SexPosition.QUEEN: PositionDetail(
        id="pos_043",
        name="Queen",
        description="Ratu di atas",
        difficulty=2,
        intensity=0.7,
        arousal_boost=0.8,
        requires_flexibility=False,
        requires_strength=True,
        tags=["queen", "woman_on_top", "dominant"]
    ),
    SexPosition.ROCKING_CHAIR: PositionDetail(
        id="pos_044",
        name="Rocking Chair",
        description="Seperti kursi goyang",
        difficulty=2,
        intensity=0.6,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=False,
        tags=["rocking", "rhythmic", "comfortable"]
    ),
    SexPosition.ROPE: PositionDetail(
        id="pos_045",
        name="Rope",
        description="Menggunakan tali (BDSM)",
        difficulty=4,
        intensity=0.8,
        arousal_boost=0.8,
        requires_flexibility=True,
        requires_strength=False,
        tags=["bdsm", "rope", "bondage"]
    ),
    SexPosition.SADDLE: PositionDetail(
        id="pos_046",
        name="Saddle",
        description="Seperti sadel kuda",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=True,
        tags=["saddle", "unique", "control"]
    ),
    SexPosition.SCORPION: PositionDetail(
        id="pos_047",
        name="Scorpion",
        description="Seperti kalajengking",
        difficulty=4,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=True,
        tags=["scorpion", "animal", "intense"]
    ),
    SexPosition.SNAKE: PositionDetail(
        id="pos_048",
        name="Snake",
        description="Melilit seperti ular",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["snake", "fluid", "unique"]
    ),
    SexPosition.SPIDER: PositionDetail(
        id="pos_049",
        name="Spider",
        description="Seperti laba-laba",
        difficulty=4,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["spider", "unique", "kinky"]
    ),
    SexPosition.STAIRS: PositionDetail(
        id="pos_050",
        name="Stairs",
        description="Di tangga",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=True,
        tags=["stairs", "public", "adventurous"]
    ),
    SexPosition.SUNSET: PositionDetail(
        id="pos_051",
        name="Sunset",
        description="Romantis seperti sunset",
        difficulty=2,
        intensity=0.6,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=False,
        tags=["sunset", "romantic", "intimate"]
    ),
    SexPosition.SWING: PositionDetail(
        id="pos_052",
        name="Swing",
        description="Berayun",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=True,
        tags=["swing", "unique", "fun"]
    ),
    SexPosition.TIGER: PositionDetail(
        id="pos_053",
        name="Tiger",
        description="Seperti harimau",
        difficulty=3,
        intensity=0.8,
        arousal_boost=0.7,
        requires_flexibility=True,
        requires_strength=True,
        tags=["tiger", "animal", "powerful"]
    ),
    SexPosition.TWISTER: PositionDetail(
        id="pos_054",
        name="Twister",
        description="Memutar",
        difficulty=4,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["twister", "unique", "flexible"]
    ),
    SexPosition.UNICORN: PositionDetail(
        id="pos_055",
        name="Unicorn",
        description="Posisi unicorn",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["unicorn", "mythical", "fun"]
    ),
    SexPosition.VENUS: PositionDetail(
        id="pos_056",
        name="Venus",
        description="Seperti dewi Venus",
        difficulty=2,
        intensity=0.6,
        arousal_boost=0.7,
        requires_flexibility=False,
        requires_strength=False,
        tags=["venus", "romantic", "goddess"]
    ),
    SexPosition.WATERFALL: PositionDetail(
        id="pos_057",
        name="Waterfall",
        description="Seperti air terjun",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["waterfall", "flow", "unique"]
    ),
    SexPosition.X_POSITION: PositionDetail(
        id="pos_058",
        name="X Position",
        description="Membentuk huruf X",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=False,
        tags=["x", "unique", "shape"]
    ),
    SexPosition.YOGA: PositionDetail(
        id="pos_059",
        name="Yoga",
        description="Terinspirasi yoga",
        difficulty=4,
        intensity=0.6,
        arousal_boost=0.6,
        requires_flexibility=True,
        requires_strength=True,
        tags=["yoga", "flexible", "spiritual"]
    ),
    SexPosition.ZEBRA: PositionDetail(
        id="pos_060",
        name="Zebra",
        description="Seperti zebra",
        difficulty=3,
        intensity=0.7,
        arousal_boost=0.6,
        requires_flexibility=False,
        requires_strength=True,
        tags=["zebra", "animal", "unique"]
    ),
}


def get_position_by_id(position_id: str) -> Optional[PositionDetail]:
    """Get position by ID"""
    for pos in POSITIONS.values():
        if pos.id == position_id:
            return pos
    return None


def get_positions_by_tag(tag: str) -> List[PositionDetail]:
    """Get positions by tag"""
    return [p for p in POSITIONS.values() if tag in p.tags]


def get_positions_by_difficulty(difficulty: int) -> List[PositionDetail]:
    """Get positions by difficulty level"""
    return [p for p in POSITIONS.values() if p.difficulty == difficulty]


def get_positions_by_intensity(min_intensity: float, max_intensity: float) -> List[PositionDetail]:
    """Get positions by intensity range"""
    return [p for p in POSITIONS.values() if min_intensity <= p.intensity <= max_intensity]


__all__ = ['SexPosition', 'POSITIONS', 'PositionDetail',
           'get_position_by_id', 'get_positions_by_tag',
           'get_positions_by_difficulty', 'get_positions_by_intensity']
