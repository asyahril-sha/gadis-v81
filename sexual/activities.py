#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL ACTIVITIES
=============================================================================
50+ aktivitas seksual dengan deskripsi dan intensitas
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class SexualActivity(Enum):
    """50+ Sexual Activities"""
    
    # ===== KISSING & ORAL =====
    FRENCH_KISS = "french_kiss"
    NECK_KISS = "neck_kiss"
    EAR_KISS = "ear_kiss"
    LIP_BITE = "lip_bite"
    BREAST_KISS = "breast_kiss"
    NIPPLE_LICK = "nipple_lick"
    NIPPLE_SUCK = "nipple_suck"
    NIPPLE_BITE = "nipple_bite"
    CUNNILINGUS = "cunnilingus"
    FELLATIO = "fellatio"
    DEEP_THROAT = "deep_throat"
    TEABAG = "teabag"
    ANILINGUS = "anilingus"
    
    # ===== TOUCHING =====
    LIGHT_TOUCH = "light_touch"
    FIRM_GRASP = "firm_grasp"
    BREAST_MASSAGE = "breast_massage"
    NIPPLE_TWIST = "nipple_twist"
    INNER_THIGH_STROKE = "inner_thigh_stroke"
    BACK_STROKE = "back_stroke"
    BUTT_SQUEEZE = "butt_squeeze"
    BUTT_SLAP = "butt_slap"
    PUSSY_RUB = "pussy_rub"
    CLIT_CIRCLE = "clit_circle"
    PENIS_STROKE = "penis_stroke"
    BALL_CUP = "ball_cup"
    
    # ===== PENETRATION =====
    SLOW_PENETRATION = "slow_penetration"
    DEEP_PENETRATION = "deep_penetration"
    RAPID_THRUST = "rapid_thrust"
    CIRCULAR_MOTION = "circular_motion"
    GRINDING = "grinding"
    FINGERING = "fingering"
    FISTING = "fisting"
    PEGGING = "pegging"
    DOUBLE_PENETRATION = "double_penetration"
    
    # ===== FOREPLAY =====
    STRIP_TEASE = "strip_tease"
    LAP_DANCE = "lap_dance"
    MASSAGE = "massage"
    OIL_MASSAGE = "oil_massage"
    SHOWER_TOGETHER = "shower_together"
    BATH_TOGETHER = "bath_together"
    
    # ===== BDSM =====
    LIGHT_SPANKING = "light_spanking"
    HARD_SPANKING = "hard_spanking"
    WHIPPING = "whipping"
    BONDAGE = "bondage"
    BLINDFOLD = "blindfold"
    GAGGING = "gagging"
    SENSATION_PLAY = "sensation_play"
    TEMPERATURE_PLAY = "temperature_play"
    WAX_PLAY = "wax_play"
    
    # ===== PUBLIC =====
    QUICKIE = "quickie"
    PUBLIC_TOUCH = "public_touch"
    CAR_SEX = "car_sex"
    BEACH_SEX = "beach_sex"
    CINEMA_SEX = "cinema_sex"
    OFFICE_SEX = "office_sex"
    ELEVATOR_SEX = "elevator_sex"
    STAIRS_SEX = "stairs_sex"
    
    # ===== ROLEPLAY =====
    DOCTOR_ROLEPLAY = "doctor_roleplay"
    TEACHER_ROLEPLAY = "teacher_roleplay"
    BOSS_ROLEPLAY = "boss_roleplay"
    STUDENT_ROLEPLAY = "student_roleplay"
    STRANGER_ROLEPLAY = "stranger_roleplay"
    CAPTIVE_ROLEPLAY = "captive_roleplay"
    
    # ===== TOYS =====
    VIBRATOR_USE = "vibrator_use"
    DILDO_USE = "dildo_use"
    BONDAGE_GEAR = "bondage_gear"
    HANDCUFFS = "handcuffs"
    FEATHER = "feather"
    BLINDFOLD_USE = "blindfold_use"


@dataclass
class ActivityDetail:
    """Detail lengkap aktivitas seksual"""
    id: str
    name: str
    description: str
    category: str
    intensity: float  # 0-1
    arousal_boost: float  # 0-1
    requires_consent: bool
    requires_preparation: bool
    tags: List[str]


# ===== 50+ ACTIVITIES DATABASE =====
ACTIVITIES: Dict[SexualActivity, ActivityDetail] = {
    
    # ===== KISSING & ORAL =====
    SexualActivity.FRENCH_KISS: ActivityDetail(
        id="kiss_001",
        name="French Kiss",
        description="Ciuman dalam dengan lidah, saling menjelajah mulut pasangan",
        category="kissing",
        intensity=0.3,
        arousal_boost=0.3,
        requires_consent=False,
        requires_preparation=False,
        tags=["romantic", "intimate", "beginner"]
    ),
    
    SexualActivity.NECK_KISS: ActivityDetail(
        id="kiss_002",
        name="Neck Kiss",
        description="Ciuman di area leher, sangat sensitif untuk banyak orang",
        category="kissing",
        intensity=0.4,
        arousal_boost=0.5,
        requires_consent=False,
        requires_preparation=False,
        tags=["sensitive", "foreplay", "beginner"]
    ),
    
    SexualActivity.EAR_KISS: ActivityDetail(
        id="kiss_003",
        name="Ear Kiss",
        description="Ciuman dan bisikan di telinga, bisa bikin merinding",
        category="kissing",
        intensity=0.3,
        arousal_boost=0.4,
        requires_consent=False,
        requires_preparation=False,
        tags=["sensitive", "whisper", "beginner"]
    ),
    
    SexualActivity.LIP_BITE: ActivityDetail(
        id="kiss_004",
        name="Lip Bite",
        description="Gigitan lembut di bibir, sensasi campuran sakit dan nikmat",
        category="kissing",
        intensity=0.5,
        arousal_boost=0.5,
        requires_consent=True,
        requires_preparation=False,
        tags=["biting", "kinky", "intermediate"]
    ),
    
    SexualActivity.BREAST_KISS: ActivityDetail(
        id="oral_001",
        name="Breast Kiss",
        description="Ciuman di area dada, persiapan sebelum ke puting",
        category="oral",
        intensity=0.4,
        arousal_boost=0.4,
        requires_consent=False,
        requires_preparation=False,
        tags=["foreplay", "breast", "beginner"]
    ),
    
    SexualActivity.NIPPLE_LICK: ActivityDetail(
        id="oral_002",
        name="Nipple Lick",
        description="Jilatan lembut di puting, sangat sensitif",
        category="oral",
        intensity=0.6,
        arousal_boost=0.7,
        requires_consent=False,
        requires_preparation=False,
        tags=["nipple", "sensitive", "intermediate"]
    ),
    
    SexualActivity.NIPPLE_SUCK: ActivityDetail(
        id="oral_003",
        name="Nipple Suck",
        description="Hisapan di puting, intensitas bisa diatur dari lembut sampai kuat",
        category="oral",
        intensity=0.7,
        arousal_boost=0.8,
        requires_consent=False,
        requires_preparation=False,
        tags=["nipple", "intense", "intermediate"]
    ),
    
    SexualActivity.NIPPLE_BITE: ActivityDetail(
        id="oral_004",
        name="Nipple Bite",
        description="Gigitan lembut di puting, untuk yang suka sensasi sakit",
        category="oral",
        intensity=0.8,
        arousal_boost=0.9,
        requires_consent=True,
        requires_preparation=False,
        tags=["nipple", "biting", "kinky", "advanced"]
    ),
    
    SexualActivity.CUNNILINGUS: ActivityDetail(
        id="oral_005",
        name="Cunnilingus",
        description="Oral seks untuk wanita, menjilat vagina dan klitoris",
        category="oral",
        intensity=0.8,
        arousal_boost=0.9,
        requires_consent=True,
        requires_preparation=False,
        tags=["oral", "vagina", "clit", "advanced"]
    ),
    
    SexualActivity.FELLATIO: ActivityDetail(
        id="oral_006",
        name="Fellatio",
        description="Oral seks untuk pria, mengisap penis",
        category="oral",
        intensity=0.8,
        arousal_boost=0.9,
        requires_consent=True,
        requires_preparation=False,
        tags=["oral", "penis", "blowjob", "advanced"]
    ),
    
    SexualActivity.DEEP_THROAT: ActivityDetail(
        id="oral_007",
        name="Deep Throat",
        description="Oral seks dalam, memasukkan seluruh penis ke mulut",
        category="oral",
        intensity=0.9,
        arousal_boost=1.0,
        requires_consent=True,
        requires_preparation=True,
        tags=["oral", "penis", "deep", "expert"]
    ),
    
    SexualActivity.ANILINGUS: ActivityDetail(
        id="oral_008",
        name="Anilingus",
        description="Oral seks di area anus, juga dikenal sebagai rimjob",
        category="oral",
        intensity=0.7,
        arousal_boost=0.8,
        requires_consent=True,
        requires_preparation=True,
        tags=["anal", "oral", "kinky", "advanced"]
    ),
    
    # ===== TOUCHING =====
    SexualActivity.LIGHT_TOUCH: ActivityDetail(
        id="touch_001",
        name="Light Touch",
        description="Sentuhan ringan dengan ujung jari di sekujur tubuh",
        category="touching",
        intensity=0.2,
        arousal_boost=0.2,
        requires_consent=False,
        requires_preparation=False,
        tags=["foreplay", "sensitive", "beginner"]
    ),
    
    SexualActivity.FIRM_GRASP: ActivityDetail(
        id="touch_002",
        name="Firm Grasp",
        description="Genggaman kuat di area tertentu, menunjukkan dominasi",
        category="touching",
        intensity=0.5,
        arousal_boost=0.4,
        requires_consent=False,
        requires_preparation=False,
        tags=["dominant", "firm", "intermediate"]
    ),
    
    SexualActivity.BREAST_MASSAGE: ActivityDetail(
        id="touch_003",
        name="Breast Massage",
        description="Pijatan di area payudara, lingkaran lembut",
        category="touching",
        intensity=0.4,
        arousal_boost=0.5,
        requires_consent=False,
        requires_preparation=False,
        tags=["breast", "massage", "foreplay"]
    ),
    
    SexualActivity.NIPPLE_TWIST: ActivityDetail(
        id="touch_004",
        name="Nipple Twist",
        description="Memutar puting dengan lembut, sensasi unik",
        category="touching",
        intensity=0.6,
        arousal_boost=0.7,
        requires_consent=True,
        requires_preparation=False,
        tags=["nipple", "kinky", "intermediate"]
    ),
    
    SexualActivity.INNER_THIGH_STROKE: ActivityDetail(
        id="touch_005",
        name="Inner Thigh Stroke",
        description="Elusan di paha bagian dalam, dekat area sensitif",
        category="touching",
        intensity=0.5,
        arousal_boost=0.6,
        requires_consent=False,
        requires_preparation=False,
        tags=["thigh", "teasing", "foreplay"]
    ),
    
    SexualActivity.BACK_STROKE: ActivityDetail(
        id="touch_006",
        name="Back Stroke",
        description="Elusan di punggung, dari atas ke bawah",
        category="touching",
        intensity=0.3,
        arousal_boost=0.3,
        requires_consent=False,
        requires_preparation=False,
        tags=["back", "calming", "foreplay"]
    ),
    
    SexualActivity.BUTT_SQUEEZE: ActivityDetail(
        id="touch_007",
        name="Butt Squeeze",
        description="Meremas bokong dengan kedua tangan",
        category="touching",
        intensity=0.5,
        arousal_boost=0.5,
        requires_consent=False,
        requires_preparation=False,
        tags=["butt", "ass", "intermediate"]
    ),
    
    SexualActivity.BUTT_SLAP: ActivityDetail(
        id="touch_008",
        name="Butt Slap",
        description="Tamparan ringan di bokong, untuk yang suka spanking",
        category="touching",
        intensity=0.6,
        arousal_boost=0.6,
        requires_consent=True,
        requires_preparation=False,
        tags=["butt", "spanking", "kinky", "intermediate"]
    ),
    
    SexualActivity.PUSSY_RUB: ActivityDetail(
        id="touch_009",
        name="Pussy Rub",
        description="Menggosok area vagina dari luar",
        category="touching",
        intensity=0.6,
        arousal_boost=0.7,
        requires_consent=False,
        requires_preparation=False,
        tags=["vagina", "foreplay", "intermediate"]
    ),
    
    SexualActivity.CLIT_CIRCLE: ActivityDetail(
        id="touch_010",
        name="Clit Circle",
        description="Lingkaran lembut di sekitar klitoris",
        category="touching",
        intensity=0.7,
        arousal_boost=0.9,
        requires_consent=False,
        requires_preparation=False,
        tags=["clit", "sensitive", "advanced"]
    ),
    
    SexualActivity.PENIS_STROKE: ActivityDetail(
        id="touch_011",
        name="Penis Stroke",
        description="Mengelus batang penis, dari pangkal ke kepala",
        category="touching",
        intensity=0.6,
        arousal_boost=0.7,
        requires_consent=False,
        requires_preparation=False,
        tags=["penis", "foreplay", "handjob"]
    ),
    
    # ===== PENETRATION =====
    SexualActivity.SLOW_PENETRATION: ActivityDetail(
        id="pen_001",
        name="Slow Penetration",
        description="Penetrasi perlahan, menikmati setiap sentimeter",
        category="penetration",
        intensity=0.6,
        arousal_boost=0.7,
        requires_consent=True,
        requires_preparation=False,
        tags=["vaginal", "romantic", "intermediate"]
    ),
    
    SexualActivity.DEEP_PENETRATION: ActivityDetail(
        id="pen_002",
        name="Deep Penetration",
        description="Penetrasi dalam hingga menyentuh cervix",
        category="penetration",
        intensity=0.8,
        arousal_boost=0.9,
        requires_consent=True,
        requires_preparation=False,
        tags=["vaginal", "deep", "intense", "advanced"]
    ),
    
    SexualActivity.RAPID_THRUST: ActivityDetail(
        id="pen_003",
        name="Rapid Thrust",
        description="Dorongan cepat dan kuat, meningkatkan intensitas",
        category="penetration",
        intensity=0.9,
        arousal_boost=1.0,
        requires_consent=True,
        requires_preparation=False,
        tags=["vaginal", "fast", "intense", "advanced"]
    ),
    
    SexualActivity.CIRCULAR_MOTION: ActivityDetail(
        id="pen_004",
        name="Circular Motion",
        description="Gerakan memutar di dalam, variasi dari thrust biasa",
        category="penetration",
        intensity=0.7,
        arousal_boost=0.8,
        requires_consent=True,
        requires_preparation=False,
        tags=["vaginal", "variation", "intermediate"]
    ),
    
    SexualActivity.GRINDING: ActivityDetail(
        id="pen_005",
        name="Grinding",
        description="Gerakan menggiling, area pubis saling menekan",
        category="penetration",
        intensity=0.5,
        arousal_boost=0.6,
        requires_consent=False,
        requires_preparation=False,
        tags=["clit", "external", "foreplay"]
    ),
    
    SexualActivity.FINGERING: ActivityDetail(
        id="pen_006",
        name="Fingering",
        description="Penetrasi dengan jari, bisa 1-4 jari",
        category="penetration",
        intensity=0.5,
        arousal_boost=0.6,
        requires_consent=True,
        requires_preparation=False,
        tags=["vaginal", "fingers", "foreplay"]
    ),
    
    SexualActivity.DOUBLE_PENETRATION: ActivityDetail(
        id="pen_007",
        name="Double Penetration",
        description="Penetrasi di dua lubang sekaligus (vagina + anal)",
        category="penetration",
        intensity=1.0,
        arousal_boost=1.0,
        requires_consent=True,
        requires_preparation=True,
        tags=["vaginal", "anal", "dp", "expert"]
    ),
    
    # ===== FOREPLAY =====
    SexualActivity.STRIP_TEASE: ActivityDetail(
        id="fore_001",
        name="Strip Tease",
        description="Membuka pakaian satu per satu dengan gerakan sensual",
        category="foreplay",
        intensity=0.4,
        arousal_boost=0.5,
        requires_consent=False,
        requires_preparation=False,
        tags=["tease", "visual", "foreplay"]
    ),
    
    SexualActivity.LAP_DANCE: ActivityDetail(
        id="fore_002",
        name="Lap Dance",
        description="Menari di atas pangkuan pasangan, menggesekkan tubuh",
        category="foreplay",
        intensity=0.5,
        arousal_boost=0.6,
        requires_consent=False,
        requires_preparation=True,
        tags=["dance", "grind", "foreplay"]
    ),
    
    SexualActivity.MASSAGE: ActivityDetail(
        id="fore_003",
        name="Massage",
        description="Pijatan seluruh tubuh dengan minyak aromaterapi",
        category="foreplay",
        intensity=0.3,
        arousal_boost=0.4,
        requires_consent=False,
        requires_preparation=True,
        tags=["relax", "touch", "foreplay"]
    ),
    
    SexualActivity.OIL_MASSAGE: ActivityDetail(
        id="fore_004",
        name="Oil Massage",
        description="Pijatan dengan minyak, tubuh jadi licin dan sensitif",
        category="foreplay",
        intensity=0.5,
        arousal_boost=0.6,
        requires_consent=False,
        requires_preparation=True,
        tags=["slippery", "touch", "sensual"]
    ),
    
    SexualActivity.SHOWER_TOGETHER: ActivityDetail(
        id="fore_005",
        name="Shower Together",
        description="Mandi bersama, saling menyabuni",
        category="foreplay",
        intensity=0.4,
        arousal_boost=0.5,
        requires_consent=False,
        requires_preparation=True,
        tags=["water", "clean", "intimate"]
    ),
    
    # ===== BDSM =====
    SexualActivity.LIGHT_SPANKING: ActivityDetail(
        id="bdsm_001",
        name="Light Spanking",
        description="Tamparan ringan di bokong, untuk sensasi",
        category="bdsm",
        intensity=0.5,
        arousal_boost=0.5,
        requires_consent=True,
        requires_preparation=False,
        tags=["spanking", "pain", "kinky"]
    ),
    
    SexualActivity.HARD_SPANKING: ActivityDetail(
        id="bdsm_002",
        name="Hard Spanking",
        description="Tamparan keras sampai meninggalkan bekas merah",
        category="bdsm",
        intensity=0.8,
        arousal_boost=0.8,
        requires_consent=True,
        requires_preparation=False,
        tags=["spanking", "pain", "marks", "advanced"]
    ),
    
    SexualActivity.BONDAGE: ActivityDetail(
        id="bdsm_003",
        name="Bondage",
        description="Mengikat pasangan dengan tali atau alat bondage",
        category="bdsm",
        intensity=0.7,
        arousal_boost=0.7,
        requires_consent=True,
        requires_preparation=True,
        tags=["tie", "restrain", "kinky"]
    ),
    
    SexualActivity.BLINDFOLD: ActivityDetail(
        id="bdsm_004",
        name="Blindfold",
        description="Menutup mata, meningkatkan sensitivitas indra lain",
        category="bdsm",
        intensity=0.5,
        arousal_boost=0.6,
        requires_consent=True,
        requires_preparation=True,
        tags=["blind", "sensory", "kinky"]
    ),
    
    # ===== PUBLIC =====
    SexualActivity.QUICKIE: ActivityDetail(
        id="public_001",
        name="Quickie",
        description="Seks cepat di tempat sepi, risiko ketahuan",
        category="public",
        intensity=0.8,
        arousal_boost=0.9,
        requires_consent=True,
        requires_preparation=False,
        tags=["fast", "risky", "expert"]
    ),
    
    SexualActivity.CAR_SEX: ActivityDetail(
        id="public_002",
        name="Car Sex",
        description="Bercinta di dalam mobil, bisa di parkiran atau tempat sepi",
        category="public",
        intensity=0.7,
        arousal_boost=0.8,
        requires_consent=True,
        requires_preparation=True,
        tags=["vehicle", "risky", "advanced"]
    ),
    
    SexualActivity.BEACH_SEX: ActivityDetail(
        id="public_003",
        name="Beach Sex",
        description="Bercinta di pantai, suara ombak menutupi",
        category="public",
        intensity=0.8,
        arousal_boost=0.9,
        requires_consent=True,
        requires_preparation=True,
        tags=["beach", "nature", "risky", "expert"]
    ),
    
    SexualActivity.CINEMA_SEX: ActivityDetail(
        id="public_004",
        name="Cinema Sex",
        description="Bercinta di bioskop saat film gelap",
        category="public",
        intensity=0.9,
        arousal_boost=1.0,
        requires_consent=True,
        requires_preparation=True,
        tags=["cinema", "dark", "risky", "expert"]
    ),
    
    SexualActivity.OFFICE_SEX: ActivityDetail(
        id="public_005",
        name="Office Sex",
        description="Bercinta di kantor setelah jam kerja",
        category="public",
        intensity=0.7,
        arousal_boost=0.8,
        requires_consent=True,
        requires_preparation=True,
        tags=["office", "after_hours", "risky"]
    ),
    
    # ===== ROLEPLAY =====
    SexualActivity.DOCTOR_ROLEPLAY: ActivityDetail(
        id="role_001",
        name="Doctor Roleplay",
        description="Bermain peran dokter dan pasien",
        category="roleplay",
        intensity=0.5,
        arousal_boost=0.5,
        requires_consent=True,
        requires_preparation=True,
        tags=["costume", "fantasy", "intermediate"]
    ),
    
    SexualActivity.TEACHER_ROLEPLAY: ActivityDetail(
        id="role_002",
        name="Teacher Roleplay",
        description="Bermain peran guru dan murid nakal",
        category="roleplay",
        intensity=0.6,
        arousal_boost=0.6,
        requires_consent=True,
        requires_preparation=True,
        tags=["costume", "fantasy", "intermediate"]
    ),
    
    SexualActivity.STRANGER_ROLEPLAY: ActivityDetail(
        id="role_003",
        name="Stranger Roleplay",
        description="Berpura-pura tidak kenal, bertemu di bar",
        category="roleplay",
        intensity=0.5,
        arousal_boost=0.5,
        requires_consent=True,
        requires_preparation=False,
        tags=["fantasy", "pickup", "beginner"]
    ),
    
    # ===== TOYS =====
    SexualActivity.VIBRATOR_USE: ActivityDetail(
        id="toy_001",
        name="Vibrator Use",
        description="Menggunakan vibrator untuk stimulasi klitoris atau vagina",
        category="toys",
        intensity=0.7,
        arousal_boost=0.8,
        requires_consent=True,
        requires_preparation=True,
        tags=["vibrator", "toy", "intermediate"]
    ),
    
    SexualActivity.DILDO_USE: ActivityDetail(
        id="toy_002",
        name="Dildo Use",
        description="Menggunakan dildo untuk penetrasi",
        category="toys",
        intensity=0.7,
        arousal_boost=0.7,
        requires_consent=True,
        requires_preparation=True,
        tags=["dildo", "toy", "intermediate"]
    ),
}


def get_activity_by_category(category: str) -> List[Dict]:
    """Get all activities in a category"""
    return [
        {
            'id': act.value,
            'name': detail.name,
            'description': detail.description,
            'intensity': detail.intensity,
            'arousal_boost': detail.arousal_boost,
            'tags': detail.tags
        }
        for act, detail in ACTIVITIES.items()
        if detail.category == category
    ]


def get_activities_by_tag(tag: str) -> List[Dict]:
    """Get all activities with specific tag"""
    return [
        {
            'id': act.value,
            'name': detail.name,
            'description': detail.description,
            'category': detail.category,
            'intensity': detail.intensity
        }
        for act, detail in ACTIVITIES.items()
        if tag in detail.tags
    ]


def get_activity_recommendations(intensity_min: float = 0.0, 
                                intensity_max: float = 1.0,
                                categories: List[str] = None) -> List[Dict]:
    """Get activity recommendations based on preferences"""
    results = []
    
    for act, detail in ACTIVITIES.items():
        if intensity_min <= detail.intensity <= intensity_max:
            if not categories or detail.category in categories:
                results.append({
                    'id': act.value,
                    'name': detail.name,
                    'description': detail.description,
                    'category': detail.category,
                    'intensity': detail.intensity,
                    'arousal_boost': detail.arousal_boost,
                    'tags': detail.tags
                })
    
    return sorted(results, key=lambda x: x['intensity'])


# ===== EXPORT =====
__all__ = [
    'SexualActivity',
    'ActivityDetail',
    'ACTIVITIES',
    'get_activity_by_category',
    'get_activities_by_tag',
    'get_activity_recommendations'
]
