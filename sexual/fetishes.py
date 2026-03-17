#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
FETISH SYSTEM
=============================================================================
Mendukung berbagai fetish dan preferensi khusus
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter
from datetime import datetime


class FetishCategory(Enum):
    """Kategori fetish"""
    BONDAGE = "bondage"
    DOMINATION = "domination"
    SUBMISSION = "submission"
    ROLEPLAY = "roleplay"
    FOOT = "foot"
    LEG = "leg"
    BREAST = "breast"
    BUTT = "butt"
    HAIR = "hair"
    VOICE = "voice"
    SCENT = "scent"
    LATEX = "latex"
    LEATHER = "leather"
    UNIFORM = "uniform"
    PREGNANCY = "pregnancy"
    LACTATION = "lactation"
    AGE_PLAY = "age_play"
    PET_PLAY = "pet_play"
    CNC = "cnc"  # Consensual Non-Consent
    EXHIBITIONISM = "exhibitionism"
    VOYEURISM = "voyeurism"
    PUBLIC = "public"
    WATTER = "water"  # Watersports
    SCAT = "scat"  # Scat play (warning)
    BLOOD = "blood"  # Blood play
    NEEDLES = "needles"  # Needle play
    FIRE = "fire"  # Fire play
    ELECTRO = "electro"  # Electro stimulation


class FetishIntensity(Enum):
    """Tingkat intensitas fetish"""
    LIGHT = "light"      # Ringan, pemula
    MEDIUM = "medium"    # Sedang
    HEAVY = "heavy"      # Berat
    EXTREME = "extreme"  # Ekstrim


class Fetish:
    """
    Representasi sebuah fetish
    """
    
    def __init__(self, 
                 name: str,
                 category: FetishCategory,
                 description: str,
                 intensity: FetishIntensity = FetishIntensity.MEDIUM,
                 requires_consent: bool = True,
                 requires_safety: bool = False,
                 requires_training: bool = False,
                 tags: List[str] = None):
        
        self.name = name
        self.category = category
        self.description = description
        self.intensity = intensity
        self.requires_consent = requires_consent
        self.requires_safety = requires_safety
        self.requires_training = requires_training
        self.tags = tags or []
        
        self.id = f"fetish_{category.value}_{name.lower().replace(' ', '_')}"
    
    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'intensity': self.intensity.value,
            'requires_consent': self.requires_consent,
            'requires_safety': self.requires_safety,
            'requires_training': self.requires_training,
            'tags': self.tags
        }


# ===== FETISH DATABASE =====

FETISHES = {
    # Bondage
    'rope_bondage': Fetish(
        name="Rope Bondage",
        category=FetishCategory.BONDAGE,
        description="Mengikat pasangan dengan tali",
        intensity=FetishIntensity.MEDIUM,
        requires_safety=True,
        requires_training=True,
        tags=['shibari', 'kinbaku', 'ties']
    ),
    'cuffs': Fetish(
        name="Handcuffs",
        category=FetishCategory.BONDAGE,
        description="Menggunakan borgol",
        intensity=FetishIntensity.LIGHT,
        tags=['metal', 'leather']
    ),
    'spread_eagle': Fetish(
        name="Spread Eagle",
        category=FetishCategory.BONDAGE,
        description="Terikat meregang",
        intensity=FetishIntensity.MEDIUM,
        tags=['stretching']
    ),
    'suspension': Fetish(
        name="Suspension",
        category=FetishCategory.BONDAGE,
        description="Menggantung di udara",
        intensity=FetishIntensity.EXTREME,
        requires_safety=True,
        requires_training=True,
        tags=['hanging', 'airy']
    ),
    
    # Domination
    'domination': Fetish(
        name="Domination",
        category=FetishCategory.DOMINATION,
        description="Menguasai pasangan",
        intensity=FetishIntensity.MEDIUM,
        tags=['dominant', 'master', 'mistress']
    ),
    'humiliation': Fetish(
        name="Humiliation",
        category=FetishCategory.DOMINATION,
        description="Mempermalukan pasangan",
        intensity=FetishIntensity.HEAVY,
        requires_consent=True,
        tags=['degradation', 'embarrassment']
    ),
    'objectification': Fetish(
        name="Objectification",
        category=FetishCategory.DOMINATION,
        description="Memperlakukan seperti benda",
        intensity=FetishIntensity.HEAVY,
        tags=['furniture', 'statue']
    ),
    
    # Submission
    'submission': Fetish(
        name="Submission",
        category=FetishCategory.SUBMISSION,
        description="Patuh pada pasangan",
        intensity=FetishIntensity.MEDIUM,
        tags=['submissive', 'slave']
    ),
    'service': Fetish(
        name="Service",
        category=FetishCategory.SUBMISSION,
        description="Melayani pasangan",
        intensity=FetishIntensity.LIGHT,
        tags=['servant', 'maid']
    ),
    
    # Roleplay
    'teacher_student': Fetish(
        name="Teacher Student",
        category=FetishCategory.ROLEPLAY,
        description="Bermain peran guru dan murid",
        intensity=FetishIntensity.LIGHT,
        tags=['school', 'education']
    ),
    'doctor_patient': Fetish(
        name="Doctor Patient",
        category=FetishCategory.ROLEPLAY,
        description="Bermain peran dokter dan pasien",
        intensity=FetishIntensity.LIGHT,
        tags=['medical', 'examination']
    ),
    'police_criminal': Fetish(
        name="Police Criminal",
        category=FetishCategory.ROLEPLAY,
        description="Bermain peran polisi dan penjahat",
        intensity=FetishIntensity.MEDIUM,
        tags=['arrest', 'interrogation']
    ),
    'boss_secretary': Fetish(
        name="Boss Secretary",
        category=FetishCategory.ROLEPLAY,
        description="Bermain peran bos dan sekretaris",
        intensity=FetishIntensity.LIGHT,
        tags=['office', 'work']
    ),
    
    # Body parts
    'foot_fetish': Fetish(
        name="Foot Fetish",
        category=FetishCategory.FOOT,
        description="Tertarik pada kaki",
        intensity=FetishIntensity.LIGHT,
        tags=['feet', 'toes', 'soles']
    ),
    'leg_fetish': Fetish(
        name="Leg Fetish",
        category=FetishCategory.LEG,
        description="Tertarik pada paha dan betis",
        intensity=FetishIntensity.LIGHT,
        tags=['thighs', 'calves']
    ),
    'breast_fetish': Fetish(
        name="Breast Fetish",
        category=FetishCategory.BREAST,
        description="Tertarik pada payudara",
        intensity=FetishIntensity.LIGHT,
        tags=['boobs', 'chest']
    ),
    'butt_fetish': Fetish(
        name="Butt Fetish",
        category=FetishCategory.BUTT,
        description="Tertarik pada bokong",
        intensity=FetishIntensity.LIGHT,
        tags=['ass', 'booty']
    ),
    'hair_fetish': Fetish(
        name="Hair Fetish",
        category=FetishCategory.HAIR,
        description="Tertarik pada rambut",
        intensity=FetishIntensity.LIGHT,
        tags=['long hair', 'ponytail']
    ),
    
    # Sensory
    'voice_fetish': Fetish(
        name="Voice Fetish",
        category=FetishCategory.VOICE,
        description="Terangsang oleh suara",
        intensity=FetishIntensity.LIGHT,
        tags=['moans', 'whispers']
    ),
    'scent_fetish': Fetish(
        name="Scent Fetish",
        category=FetishCategory.SCENT,
        description="Terangsang oleh aroma",
        intensity=FetishIntensity.LIGHT,
        tags=['pheromones', 'perfume']
    ),
    
    # Materials
    'latex_fetish': Fetish(
        name="Latex Fetish",
        category=FetishCategory.LATEX,
        description="Terangsang oleh pakaian lateks",
        intensity=FetishIntensity.MEDIUM,
        tags=['rubber', 'shiny']
    ),
    'leather_fetish': Fetish(
        name="Leather Fetish",
        category=FetishCategory.LEATHER,
        description="Terangsang oleh pakaian kulit",
        intensity=FetishIntensity.MEDIUM,
        tags=['leather jacket', 'boots']
    ),
    'uniform_fetish': Fetish(
        name="Uniform Fetish",
        category=FetishCategory.UNIFORM,
        description="Terangsang oleh seragam",
        intensity=FetishIntensity.LIGHT,
        tags=['military', 'school', 'nurse']
    ),
    
    # Pregnancy
    'pregnancy_fetish': Fetish(
        name="Pregnancy Fetish",
        category=FetishCategory.PREGNANCY,
        description="Terangsang oleh kehamilan",
        intensity=FetishIntensity.MEDIUM,
        tags=['pregnant', 'belly']
    ),
    'lactation_fetish': Fetish(
        name="Lactation Fetish",
        category=FetishCategory.LACTATION,
        description="Terangsang oleh air susu",
        intensity=FetishIntensity.MEDIUM,
        tags=['breast milk', 'nursing']
    ),
    
    # Play
    'age_play': Fetish(
        name="Age Play",
        category=FetishCategory.AGE_PLAY,
        description="Bermain peran usia berbeda",
        intensity=FetishIntensity.MEDIUM,
        requires_consent=True,
        tags=['daddy', 'mommy', 'little']
    ),
    'pet_play': Fetish(
        name="Pet Play",
        category=FetishCategory.PET_PLAY,
        description="Bermain peran hewan peliharaan",
        intensity=FetishIntensity.MEDIUM,
        tags=['puppy', 'kitten', 'pony']
    ),
    
    # CNC
    'cnc': Fetish(
        name="CNC",
        category=FetishCategory.CNC,
        description="Consensual Non-Consent (pura-pura dipaksa)",
        intensity=FetishIntensity.HEAVY,
        requires_consent=True,
        requires_safety=True,
        tags=['struggle', 'forced']
    ),
    
    # Public
    'exhibitionism': Fetish(
        name="Exhibitionism",
        category=FetishCategory.EXHIBITIONISM,
        description="Terangsang saat dilihat orang",
        intensity=FetishIntensity.MEDIUM,
        tags=['flashing', 'public']
    ),
    'voyeurism': Fetish(
        name="Voyeurism",
        category=FetishCategory.VOYEURISM,
        description="Terangsang melihat orang",
        intensity=FetishIntensity.MEDIUM,
        tags=['watching', 'peeping']
    ),
    'public_sex': Fetish(
        name="Public Sex",
        category=FetishCategory.PUBLIC,
        description="Berhubungan di tempat umum",
        intensity=FetishIntensity.HEAVY,
        tags=['risky', 'outdoor']
    ),
    
    # Extreme (with warnings)
    'watersports': Fetish(
        name="Watersports",
        category=FetishCategory.WATTER,
        description="Bermain dengan urine",
        intensity=FetishIntensity.EXTREME,
        requires_consent=True,
        tags=['piss', 'golden shower']
    ),
    'scat': Fetish(
        name="Scat",
        category=FetishCategory.SCAT,
        description="Bermain dengan feses ⚠️",
        intensity=FetishIntensity.EXTREME,
        requires_consent=True,
        requires_safety=True,
        tags=['toilet']
    ),
    'blood_play': Fetish(
        name="Blood Play",
        category=FetishCategory.BLOOD,
        description="Bermain dengan darah ⚠️",
        intensity=FetishIntensity.EXTREME,
        requires_consent=True,
        requires_safety=True,
        tags=['knife', 'cut']
    ),
    'needle_play': Fetish(
        name="Needle Play",
        category=FetishCategory.NEEDLES,
        description="Bermain dengan jarum ⚠️",
        intensity=FetishIntensity.EXTREME,
        requires_consent=True,
        requires_safety=True,
        requires_training=True,
        tags=['piercing', 'acupuncture']
    ),
    'fire_play': Fetish(
        name="Fire Play",
        category=FetishCategory.FIRE,
        description="Bermain dengan api ⚠️",
        intensity=FetishIntensity.EXTREME,
        requires_consent=True,
        requires_safety=True,
        requires_training=True,
        tags=['flame', 'burn']
    ),
    'electro': Fetish(
        name="Electro",
        category=FetishCategory.ELECTRO,
        description="Stimulasi listrik ⚠️",
        intensity=FetishIntensity.EXTREME,
        requires_consent=True,
        requires_safety=True,
        requires_training=True,
        tags=['tens', 'estim']
    ),
}


class UserFetishProfile:
    """Fetish profile untuk user"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.interested_fetishes: Set[str] = set()  # Fetish IDs
        self.experienced_fetishes: Set[str] = set()  # Sudah pernah coba
        self.favorite_fetishes: Set[str] = set()  # Favorit
        self.hard_limits: Set[str] = set()  # Yang tidak mau
        self.curious_about: Set[str] = set()  # Ingin coba
        
        self.fetish_history = []  # History eksplorasi
        self.last_explored = {}
        
        self.fetish_score = defaultdict(float)  # Skor preferensi per fetish
    
    def add_interest(self, fetish_id: str):
        """Tambah ketertarikan"""
        if fetish_id in FETISHES:
            self.interested_fetishes.add(fetish_id)
            self.fetish_score[fetish_id] += 0.3
    
    def add_experience(self, fetish_id: str, rating: int = None):
        """Tambah pengalaman"""
        if fetish_id in FETISHES:
            self.experienced_fetishes.add(fetish_id)
            self.last_explored[fetish_id] = datetime.now()
            
            if rating and rating >= 4:
                self.favorite_fetishes.add(fetish_id)
                self.fetish_score[fetish_id] += 0.5
            elif rating:
                self.fetish_score[fetish_id] += 0.1 * rating
            
            self.fetish_history.append({
                'fetish_id': fetish_id,
                'timestamp': datetime.now().isoformat(),
                'rating': rating
            })
    
    def add_hard_limit(self, fetish_id: str):
        """Tambah hard limit"""
        self.hard_limits.add(fetish_id)
        self.fetish_score[fetish_id] = 0
    
    def add_curious(self, fetish_id: str):
        """Tambah ingin coba"""
        self.curious_about.add(fetish_id)
    
    def get_recommendations(self, limit: int = 5) -> List[Dict]:
        """Dapatkan rekomendasi fetish"""
        # Berdasarkan ketertarikan yang sudah ada
        base_interests = self.interested_fetishes | self.favorite_fetishes
        
        recommendations = []
        for fid, fetish in FETISHES.items():
            if fid in self.experienced_fetishes or fid in self.hard_limits:
                continue
            
            # Hitung skor rekomendasi
            score = 0
            
            # Berdasarkan kategori yang sama dengan interest
            for interest in base_interests:
                if interest in FETISHES:
                    if FETISHES[interest].category == fetish.category:
                        score += 0.3
            
            # Berdasarkan intensitas
            if fetish.intensity.value in ['light', 'medium']:
                score += 0.2
            
            if score > 0.5:
                recommendations.append({
                    'id': fid,
                    'name': fetish.name,
                    'category': fetish.category.value,
                    'description': fetish.description,
                    'score': round(score, 2)
                })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)[:limit]
    
    def get_compatibility(self, other_profile: 'UserFetishProfile') -> float:
        """Hitung kecocokan fetish dengan user lain"""
        if not other_profile:
            return 0.0
        
        my_fetishes = self.favorite_fetishes | self.interested_fetishes
        other_fetishes = other_profile.favorite_fetishes | other_profile.interested_fetishes
        
        if not my_fetishes or not other_fetishes:
            return 0.5
        
        # Hitung overlap
        common = my_fetishes & other_fetishes
        
        # Hindari hard limits
        my_limits = self.hard_limits
        other_limits = other_profile.hard_limits
        
        # Jika ada di hard limits, kurangi skor
        penalty = 0
        for fetish in common:
            if fetish in my_limits or fetish in other_limits:
                penalty += 0.2
        
        total_possible = len(my_fetishes | other_fetishes)
        if total_possible == 0:
            return 0.5
        
        base_score = len(common) / total_possible
        final_score = max(0, base_score - penalty)
        
        return round(final_score, 2)
    
 def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            'user_id': self.user_id,
            'interested_fetishes': list(self.interested_fetishes),
            'experienced_fetishes': list(self.experienced_fetishes),
            'favorite_fetishes': list(self.favorite_fetishes),
            'hard_limits': list(self.hard_limits),
            'curious_about': list(self.curious_about),
            'fetish_score': dict(self.fetish_score),
            'fetish_history': self.fetish_history,
            'last_explored': {k: v.isoformat() for k, v in self.last_explored.items()}
        }


class FetishManager:
    """Manager untuk fetish system"""
    
    def __init__(self):
        self.user_profiles: Dict[int, UserFetishProfile] = {}
    
    def get_profile(self, user_id: int) -> UserFetishProfile:
        """Get or create profile for user"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserFetishProfile(user_id)
        return self.user_profiles[user_id]
    
    def get_fetish_by_category(self, category: FetishCategory) -> List[Fetish]:
        """Get all fetishes in category"""
        return [f for f in FETISHES.values() if f.category == category]
    
    def search_fetishes(self, query: str) -> List[Fetish]:
        """Search fetishes by name or tags"""
        query = query.lower()
        results = []
        
        for fetish in FETISHES.values():
            if query in fetish.name.lower() or any(query in t.lower() for t in fetish.tags):
                results.append(fetish)
        
        return results
    
    def get_popular_fetishes(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most popular fetishes across all users"""
        counter = Counter()
        
        for profile in self.user_profiles.values():
            counter.update(profile.interested_fetishes)
            counter.update(profile.favorite_fetishes)
        
        return counter.most_common(limit)
    
    def get_safe_for_work(self) -> List[Fetish]:
        """Get fetishes that are safe for general conversation"""
        safe_intensities = [FetishIntensity.LIGHT, FetishIntensity.MEDIUM]
        safe_categories = [
            FetishCategory.ROLEPLAY,
            FetishCategory.FOOT,
            FetishCategory.LEG,
            FetishCategory.HAIR,
            FetishCategory.VOICE,
            FetishCategory.SCENT
        ]
        
        return [
            f for f in FETISHES.values()
            if f.intensity in safe_intensities or f.category in safe_categories
        ]
    
    def get_extreme_fetishes(self) -> List[Fetish]:
        """Get extreme fetishes (with warnings)"""
        return [
            f for f in FETISHES.values()
            if f.intensity == FetishIntensity.EXTREME
        ]


__all__ = [
    'FetishCategory',
    'FetishIntensity',
    'Fetish',
    'FETISHES',
    'UserFetishProfile',
    'FetishManager'
]
