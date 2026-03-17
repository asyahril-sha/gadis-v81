#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEX TOYS INTEGRATION
=============================================================================
Daftar dan interaksi dengan sex toys
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
from collections import defaultdict


class ToyCategory(Enum):
    """Kategori sex toys"""
    VIBRATOR = "vibrator"
    DILDO = "dildo"
    ANAL = "anal"
    BDSM = "bdsm"
    COUPLE = "couple"
    LUBRICANT = "lubricant"
    OTHER = "other"


class ToyMaterial(Enum):
    """Material sex toys"""
    SILICONE = "silicone"
    GLASS = "glass"
    METAL = "metal"
    PLASTIC = "plastic"
    RUBBER = "rubber"
    WOOD = "wood"
    LEATHER = "leather"


class ToyPower(Enum):
    """Sumber tenaga"""
    BATTERY = "battery"
    RECHARGEABLE = "rechargeable"
    MANUAL = "manual"
    PLUGIN = "plugin"


class SexToy:
    """Model untuk sex toy"""
    
    def __init__(self, 
                 toy_id: str,
                 name: str,
                 category: ToyCategory,
                 description: str,
                 material: ToyMaterial = ToyMaterial.SILICONE,
                 power_source: ToyPower = ToyPower.MANUAL,
                 intensity_levels: int = 3,
                 waterproof: bool = False,
                 noise_level: float = 0.5,  # 0-1
                 price_range: str = "$$",
                 image_url: str = None):
        
        self.toy_id = toy_id
        self.name = name
        self.category = category
        self.description = description
        self.material = material
        self.power_source = power_source
        self.intensity_levels = intensity_levels
        self.waterproof = waterproof
        self.noise_level = noise_level
        self.price_range = price_range
        self.image_url = image_url
        
        # Stats
        self.popularity = 0
        self.rating = 0.0
        self.review_count = 0
        
        # Usage tracking
        self.times_used = 0
        self.last_used = None
        self.average_duration = 0
        
        # Compatibility
        self.compatible_positions = []
        self.recommended_with = []
    
    def to_dict(self) -> Dict:
        return {
            'toy_id': self.toy_id,
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'material': self.material.value,
            'power_source': self.power_source.value,
            'intensity_levels': self.intensity_levels,
            'waterproof': self.waterproof,
            'noise_level': self.noise_level,
            'price_range': self.price_range,
            'image_url': self.image_url,
            'popularity': self.popularity,
            'rating': self.rating,
            'review_count': self.review_count
        }


class ToyUsage:
    """Tracking penggunaan toy"""
    
    def __init__(self, toy_id: str, user_id: int):
        self.toy_id = toy_id
        self.user_id = user_id
        self.times_used = 0
        self.total_duration = 0
        self.last_used = None
        self.favorite_intensity = 1
        self.ratings = []
        
        # Stats per session
        self.sessions = []
    
    def add_session(self, duration: int, intensity: int, climax: bool = False, notes: str = ""):
        """Add usage session"""
        session = {
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'intensity': intensity,
            'climax': climax,
            'notes': notes
        }
        
        self.sessions.append(session)
        self.times_used += 1
        self.total_duration += duration
        self.last_used = datetime.now()
        
        # Update favorite intensity
        if intensity > self.favorite_intensity:
            self.favorite_intensity = intensity
        
        # Keep only last 50 sessions
        if len(self.sessions) > 50:
            self.sessions = self.sessions[-50:]
    
    def add_rating(self, rating: int, review: str = ""):
        """Add rating for toy"""
        self.ratings.append({
            'timestamp': datetime.now().isoformat(),
            'rating': rating,
            'review': review
        })
    
    def get_average_duration(self) -> float:
        """Get average session duration"""
        if self.times_used == 0:
            return 0
        return self.total_duration / self.times_used
    
    def get_average_rating(self) -> float:
        """Get average rating"""
        if not self.ratings:
            return 0
        return sum(r['rating'] for r in self.ratings) / len(self.ratings)
    
    def to_dict(self) -> Dict:
        return {
            'toy_id': self.toy_id,
            'user_id': self.user_id,
            'times_used': self.times_used,
            'total_duration': self.total_duration,
            'avg_duration': self.get_average_duration(),
            'favorite_intensity': self.favorite_intensity,
            'avg_rating': self.get_average_rating(),
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'recent_sessions': self.sessions[-5:]  # Last 5 sessions
        }


class ToyCollection:
    """Koleksi toys untuk user"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.toys: Dict[str, ToyUsage] = {}  # toy_id -> ToyUsage
        self.wishlist: List[str] = []  # toy_id wishlist
        
        # Stats
        self.total_toys = 0
        self.favorite_category = None
        self.most_used_toy = None
    
    def add_toy(self, toy_id: str):
        """Add toy to collection"""
        if toy_id not in self.toys:
            self.toys[toy_id] = ToyUsage(toy_id, self.user_id)
            self.total_toys += 1
    
    def remove_toy(self, toy_id: str):
        """Remove toy from collection"""
        if toy_id in self.toys:
            del self.toys[toy_id]
            self.total_toys -= 1
    
    def add_to_wishlist(self, toy_id: str):
        """Add toy to wishlist"""
        if toy_id not in self.wishlist:
            self.wishlist.append(toy_id)
    
    def remove_from_wishlist(self, toy_id: str):
        """Remove toy from wishlist"""
        if toy_id in self.wishlist:
            self.wishlist.remove(toy_id)
    
    def use_toy(self, toy_id: str, duration: int, intensity: int, climax: bool = False, notes: str = ""):
        """Record toy usage"""
        if toy_id not in self.toys:
            self.add_toy(toy_id)
        
        self.toys[toy_id].add_session(duration, intensity, climax, notes)
        
        # Update stats
        self._update_stats()
    
    def rate_toy(self, toy_id: str, rating: int, review: str = ""):
        """Rate a toy"""
        if toy_id in self.toys:
            self.toys[toy_id].add_rating(rating, review)
    
    def _update_stats(self):
        """Update collection statistics"""
        if not self.toys:
            return
        
        # Find most used toy
        self.most_used_toy = max(
            self.toys.items(),
            key=lambda x: x[1].times_used
        )[0]
        
        # Find favorite category (would need toy database)
        pass
    
    def get_recommendations(self, toy_db: Dict[str, SexToy], limit: int = 5) -> List[Dict]:
        """Get toy recommendations based on usage"""
        if not self.toys:
            return []
        
        # Get categories user likes
        used_categories = []
        for toy_id in self.toys:
            if toy_id in toy_db:
                used_categories.append(toy_db[toy_id].category)
        
        if not used_categories:
            return []
        
        # Find most used category
        from collections import Counter
        fav_category = Counter(used_categories).most_common(1)[0][0]
        
        # Recommend similar toys not owned
        recommendations = []
        for toy_id, toy in toy_db.items():
            if toy_id not in self.toys and toy.category == fav_category:
                recommendations.append(toy.to_dict())
        
        return recommendations[:limit]
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'total_toys': self.total_toys,
            'wishlist': self.wishlist,
            'most_used_toy': self.most_used_toy,
            'toys': {tid: usage.to_dict() for tid, usage in self.toys.items()}
        }


# ===== TOY DATABASE =====

TOYS = {
    # Vibrators
    'vib_bullet_001': SexToy(
        toy_id='vib_bullet_001',
        name='Bullet Vibrator',
        category=ToyCategory.VIBRATOR,
        description='Vibrator kecil untuk stimulasi klitoris',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.BATTERY,
        intensity_levels=3,
        waterproof=True,
        noise_level=0.3,
        price_range='$'
    ),
    
    'vib_wand_001': SexToy(
        toy_id='vib_wand_001',
        name='Magic Wand',
        category=ToyCategory.VIBRATOR,
        description='Vibrator besar dengan getaran kuat',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.PLUGIN,
        intensity_levels=4,
        waterproof=False,
        noise_level=0.7,
        price_range='$$$'
    ),
    
    'vib_rabbit_001': SexToy(
        toy_id='vib_rabbit_001',
        name='Rabbit Vibrator',
        category=ToyCategory.VIBRATOR,
        description='Vibrator dengan stimulasi ganda',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.RECHARGEABLE,
        intensity_levels=5,
        waterproof=True,
        noise_level=0.5,
        price_range='$$'
    ),
    
    # Dildos
    'dildo_real_001': SexToy(
        toy_id='dildo_real_001',
        name='Realistic Dildo',
        category=ToyCategory.DILDO,
        description='Dildo dengan tekstur realistis',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=True,
        noise_level=0.1,
        price_range='$$'
    ),
    
    'dildo_glass_001': SexToy(
        toy_id='dildo_glass_001',
        name='Glass Dildo',
        category=ToyCategory.DILDO,
        description='Dildo kaca untuk sensasi dingin/panas',
        material=ToyMaterial.GLASS,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=True,
        noise_level=0.0,
        price_range='$$$'
    ),
    
    # Anal toys
    'anal_plug_001': SexToy(
        toy_id='anal_plug_001',
        name='Starter Butt Plug',
        category=ToyCategory.ANAL,
        description='Butt plug untuk pemula',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=True,
        noise_level=0.1,
        price_range='$'
    ),
    
    'anal_beads_001': SexToy(
        toy_id='anal_beads_001',
        name='Anal Beads',
        category=ToyCategory.ANAL,
        description='Manik-manik untuk stimulasi bertahap',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=True,
        noise_level=0.1,
        price_range='$'
    ),
    
    'anal_prostate_001': SexToy(
        toy_id='anal_prostate_001',
        name='Prostate Massager',
        category=ToyCategory.ANAL,
        description='Massager khusus untuk stimulasi prostat',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.RECHARGEABLE,
        intensity_levels=3,
        waterproof=True,
        noise_level=0.4,
        price_range='$$'
    ),
    
    # BDSM toys
    'bdsm_cuffs_001': SexToy(
        toy_id='bdsm_cuffs_001',
        name='Wrist Cuffs',
        category=ToyCategory.BDSM,
        description='Borgol lembut untuk wrist',
        material=ToyMaterial.LEATHER,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=False,
        noise_level=0.2,
        price_range='$$'
    ),
    
    'bdsm_blindfold_001': SexToy(
        toy_id='bdsm_blindfold_001',
        name='Silk Blindfold',
        category=ToyCategory.BDSM,
        description='Penutup mata sutra',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=False,
        noise_level=0.0,
        price_range='$'
    ),
    
    'bdsm_whip_001': SexToy(
        toy_id='bdsm_whip_001',
        name='Leather Whip',
        category=ToyCategory.BDSM,
        description='Cambuk kulit untuk impact play',
        material=ToyMaterial.LEATHER,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=False,
        noise_level=0.3,
        price_range='$$'
    ),
    
    # Couple toys
    'couple_remote_001': SexToy(
        toy_id='couple_remote_001',
        name='Remote Control Vibrator',
        category=ToyCategory.COUPLE,
        description='Vibrator yang bisa dikontrol remote',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.RECHARGEABLE,
        intensity_levels=4,
        waterproof=True,
        noise_level=0.4,
        price_range='$$$'
    ),
    
    'couple_wearable_001': SexToy(
        toy_id='couple_wearable_001',
        name='Wearable Vibrator',
        category=ToyCategory.COUPLE,
        description='Vibrator yang bisa dipakai saat berhubungan',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.RECHARGEABLE,
        intensity_levels=3,
        waterproof=True,
        noise_level=0.5,
        price_range='$$'
    ),
    
    # Lubricants
    'lube_water_001': SexToy(
        toy_id='lube_water_001',
        name='Water Based Lube',
        category=ToyCategory.LUBRICANT,
        description='Pelumas water-based, cocok untuk semua toys',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=True,
        noise_level=0.0,
        price_range='$'
    ),
    
    'lube_silicone_001': SexToy(
        toy_id='lube_silicone_001',
        name='Silicone Based Lube',
        category=ToyCategory.LUBRICANT,
        description='Pelumas silicone-based, tahan lama',
        material=ToyMaterial.SILICONE,
        power_source=ToyPower.MANUAL,
        intensity_levels=1,
        waterproof=True,
        noise_level=0.0,
        price_range='$$'
    )
}


class ToyManager:
    """Manager untuk semua interaksi toys"""
    
    def __init__(self):
        self.toys = TOYS
        self.collections: Dict[int, ToyCollection] = {}
        self.usage_stats = defaultdict(int)
    
    def get_toy(self, toy_id: str) -> Optional[SexToy]:
        """Get toy by ID"""
        return self.toys.get(toy_id)
    
    def get_toys_by_category(self, category: ToyCategory) -> List[SexToy]:
        """Get toys by category"""
        return [t for t in self.toys.values() if t.category == category]
    
    def get_collection(self, user_id: int) -> ToyCollection:
        """Get or create user collection"""
        if user_id not in self.collections:
            self.collections[user_id] = ToyCollection(user_id)
        return self.collections[user_id]
    
    def use_toy(self, user_id: int, toy_id: str, duration: int, 
                intensity: int = 1, climax: bool = False, notes: str = ""):
        """Record toy usage"""
        collection = self.get_collection(user_id)
        collection.use_toy(toy_id, duration, intensity, climax, notes)
        
        # Update global stats
        self.usage_stats[toy_id] += 1
        
        # Update toy popularity
        if toy_id in self.toys:
            self.toys[toy_id].times_used += 1
            self.toys[toy_id].last_used = datetime.now()
    
    def get_popular_toys(self, limit: int = 5) -> List[Dict]:
        """Get most popular toys globally"""
        popular = sorted(
            self.toys.values(),
            key=lambda x: x.times_used,
            reverse=True
        )[:limit]
        
        return [t.to_dict() for t in popular]
    
    def get_recommendations_for_user(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Get personalized toy recommendations"""
        collection = self.get_collection(user_id)
        return collection.get_recommendations(self.toys, limit)


__all__ = [
    'SexToy',
    'ToyCategory',
    'ToyMaterial',
    'ToyPower',
    'ToyUsage',
    'ToyCollection',
    'ToyManager',
    'TOYS'
]
