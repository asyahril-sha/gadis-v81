#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
PUBLIC LOCATIONS
=============================================================================
30+ lokasi publik untuk aktivitas berisiko
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import time


class PublicArea(Enum):
    """30+ Public Locations"""
    
    # Pantai dan alam
    BEACH_NIGHT = "pantai malam"
    BEACH_DAY = "pantai siang"
    FOREST = "hutan"
    PARK = "taman kota"
    LAKE = "danau"
    MOUNTAIN = "gunung"
    
    # Tempat umum
    CINEMA = "bioskop"
    CINEMA_BACK = "bioskop belakang"
    PARKING_LOT = "parkiran mall"
    PARKING_BASEMENT = "parkiran basement"
    PUBLIC_TOILET = "toilet umum"
    PUBLIC_TOILET_DISABLED = "toilet difabel"
    
    # Transportasi
    BUS = "bus umum"
    TRAIN = "kereta"
    TRAIN_TOILET = "toilet kereta"
    ELEVATOR = "lift"
    ESCALATOR = "eskalator"
    STAIRS = "tangga darurat"
    CAR = "mobil"
    CAR_PARKED = "mobil parkir"
    
    # Gedung
    ROOFTOP = "atap gedung"
    OFFICE_NIGHT = "kantor malam"
    OFFICE_WEEKEND = "kantor weekend"
    SCHOOL_NIGHT = "sekolah malam"
    MOSQUE = "masjid"
    CHURCH = "gereja"
    
    # Hiburan
    KARAOKE = "karaoke"
    CLUB = "club malam"
    CLUB_TOILET = "toilet club"
    BAR = "bar"
    
    # Lainnya
    ALLEY = "gang belakang"
    BRIDGE = "bawah jembatan"
    CEMETERY = "kuburan"
    CHANGING_ROOM = "ruang ganti"
    WAREHOUSE = "gudang"


class PublicLocation:
    """Model untuk lokasi publik"""
    
    def __init__(self,
                 area: PublicArea,
                 name: str,
                 description: str,
                 base_risk: float,  # 0-1
                 crowd_density: float,  # 0-1
                 cctv_coverage: float,  # 0-1
                 security_presence: float,  # 0-1
                 thrill_boost: float,  # 0-1
                 time_multipliers: Dict[str, float],
                 best_time: str,
                 worst_time: str,
                 image_url: str = None):
        
        self.area = area
        self.name = name
        self.description = description
        self.base_risk = base_risk
        self.crowd_density = crowd_density
        self.cctv_coverage = cctv_coverage
        self.security_presence = security_presence
        self.thrill_boost = thrill_boost
        self.time_multipliers = time_multipliers
        self.best_time = best_time
        self.worst_time = worst_time
        self.image_url = image_url
        
        # Popularity stats
        self.popularity = 0
        self.success_rate = 0.5
        self.total_visits = 0
        self.successful_visits = 0
    
    def calculate_risk(self, hour: int, is_weekend: bool = False) -> float:
        """Calculate actual risk based on time"""
        # Base risk
        risk = self.base_risk
        
        # Time multiplier
        time_key = "night" if hour < 5 or hour > 20 else "day"
        if is_weekend:
            time_key = "weekend_" + time_key
        
        multiplier = self.time_multipliers.get(time_key, 1.0)
        risk *= multiplier
        
        return min(1.0, risk)
    
    def get_thrill(self, risk: float) -> float:
        """Calculate thrill level"""
        return risk * self.thrill_boost
    
    def record_visit(self, success: bool):
        """Record a visit"""
        self.total_visits += 1
        if success:
            self.successful_visits += 1
            self.success_rate = self.successful_visits / self.total_visits
    
    def to_dict(self) -> Dict:
        return {
            'id': self.area.value,
            'name': self.name,
            'description': self.description,
            'base_risk': self.base_risk,
            'crowd_density': self.crowd_density,
            'cctv_coverage': self.cctv_coverage,
            'security_presence': self.security_presence,
            'thrill_boost': self.thrill_boost,
            'best_time': self.best_time,
            'worst_time': self.worst_time,
            'popularity': self.popularity,
            'success_rate': self.success_rate,
            'total_visits': self.total_visits
        }


# ===== DATABASE LOKASI =====

LOCATIONS = {
    # Pantai
    PublicArea.BEACH_NIGHT: PublicLocation(
        area=PublicArea.BEACH_NIGHT,
        name="Pantai Malam",
        description="Pantai sepi dengan suara ombak. Bulan purnama menambah romantisme.",
        base_risk=0.4,
        crowd_density=0.2,
        cctv_coverage=0.1,
        security_presence=0.2,
        thrill_boost=0.8,
        time_multipliers={
            'day': 1.5,
            'night': 0.7,
            'weekend_day': 1.8,
            'weekend_night': 0.9
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.BEACH_DAY: PublicLocation(
        area=PublicArea.BEACH_DAY,
        name="Pantai Siang",
        description="Pantai ramai dengan pengunjung. Resiko tinggi ketahuan.",
        base_risk=0.8,
        crowd_density=0.8,
        cctv_coverage=0.3,
        security_presence=0.5,
        thrill_boost=0.9,
        time_multipliers={
            'day': 1.0,
            'night': 0.3,
            'weekend_day': 1.2,
            'weekend_night': 0.4
        },
        best_time="night",
        worst_time="day"
    ),
    
    # Bioskop
    PublicArea.CINEMA: PublicLocation(
        area=PublicArea.CINEMA,
        name="Bioskop",
        description="Gedung bioskop dengan banyak ruangan gelap.",
        base_risk=0.5,
        crowd_density=0.6,
        cctv_coverage=0.7,
        security_presence=0.4,
        thrill_boost=0.7,
        time_multipliers={
            'day': 0.8,
            'night': 1.2,
            'weekend_day': 1.0,
            'weekend_night': 1.3
        },
        best_time="day",
        worst_time="weekend_night"
    ),
    
    PublicArea.CINEMA_BACK: PublicLocation(
        area=PublicArea.CINEMA_BACK,
        name="Belakang Bioskop",
        description="Area belakang bioskop yang sepi, dekat pintu darurat.",
        base_risk=0.6,
        crowd_density=0.1,
        cctv_coverage=0.3,
        security_presence=0.2,
        thrill_boost=0.8,
        time_multipliers={
            'day': 0.9,
            'night': 0.5,
            'weekend_day': 1.1,
            'weekend_night': 0.6
        },
        best_time="night",
        worst_time="day"
    ),
    
    # Parkiran
    PublicArea.PARKING_LOT: PublicLocation(
        area=PublicArea.PARKING_LOT,
        name="Parkiran Mall",
        description="Parkiran terbuka mall, ramai tapi banyak sudut gelap.",
        base_risk=0.7,
        crowd_density=0.5,
        cctv_coverage=0.8,
        security_presence=0.6,
        thrill_boost=0.8,
        time_multipliers={
            'day': 1.2,
            'night': 0.6,
            'weekend_day': 1.3,
            'weekend_night': 0.7
        },
        best_time="night",
        worst_time="weekend_day"
    ),
    
    PublicArea.PARKING_BASEMENT: PublicLocation(
        area=PublicArea.PARKING_BASEMENT,
        name="Parkiran Basement",
        description="Basement mall yang gelap dan sepi, banyak CCTV.",
        base_risk=0.6,
        crowd_density=0.2,
        cctv_coverage=0.9,
        security_presence=0.4,
        thrill_boost=0.9,
        time_multipliers={
            'day': 0.8,
            'night': 0.5,
            'weekend_day': 0.9,
            'weekend_night': 0.6
        },
        best_time="night",
        worst_time="day"
    ),
    
    # Toilet umum
    PublicArea.PUBLIC_TOILET: PublicLocation(
        area=PublicArea.PUBLIC_TOILET,
        name="Toilet Umum",
        description="Toilet umum dengan banyak pengunjung, bilik sempit.",
        base_risk=0.8,
        crowd_density=0.6,
        cctv_coverage=0.2,
        security_presence=0.3,
        thrill_boost=0.9,
        time_multipliers={
            'day': 1.2,
            'night': 0.6,
            'weekend_day': 1.3,
            'weekend_night': 0.7
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.PUBLIC_TOILET_DISABLED: PublicLocation(
        area=PublicArea.PUBLIC_TOILET_DISABLED,
        name="Toilet Difabel",
        description="Toilet khusus difabel yang lebih luas dan jarang dipakai.",
        base_risk=0.5,
        crowd_density=0.1,
        cctv_coverage=0.1,
        security_presence=0.1,
        thrill_boost=0.7,
        time_multipliers={
            'day': 1.0,
            'night': 0.5,
            'weekend_day': 1.1,
            'weekend_night': 0.6
        },
        best_time="night",
        worst_time="day"
    ),
    
    # Transportasi
    PublicArea.BUS: PublicLocation(
        area=PublicArea.BUS,
        name="Bus Umum",
        description="Bus kota yang ramai, risiko tinggi ketahuan.",
        base_risk=0.9,
        crowd_density=0.8,
        cctv_coverage=0.5,
        security_presence=0.3,
        thrill_boost=0.9,
        time_multipliers={
            'day': 1.3,
            'night': 0.5,
            'weekend_day': 1.2,
            'weekend_night': 0.6
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.TRAIN: PublicLocation(
        area=PublicArea.TRAIN,
        name="Kereta",
        description="Kereta dengan banyak gerbong dan sudut sepi.",
        base_risk=0.7,
        crowd_density=0.6,
        cctv_coverage=0.6,
        security_presence=0.4,
        thrill_boost=0.8,
        time_multipliers={
            'day': 1.2,
            'night': 0.5,
            'weekend_day': 1.3,
            'weekend_night': 0.6
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.TRAIN_TOILET: PublicLocation(
        area=PublicArea.TRAIN_TOILET,
        name="Toilet Kereta",
        description="Toilet sempit di kereta, suara orang lalu lalang.",
        base_risk=0.7,
        crowd_density=0.3,
        cctv_coverage=0.2,
        security_presence=0.2,
        thrill_boost=0.8,
        time_multipliers={
            'day': 1.1,
            'night': 0.6,
            'weekend_day': 1.2,
            'weekend_night': 0.7
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.ELEVATOR: PublicLocation(
        area=PublicArea.ELEVATOR,
        name="Lift",
        description="Lift dengan CCTV di sudut, berhenti di setiap lantai.",
        base_risk=0.8,
        crowd_density=0.3,
        cctv_coverage=0.9,
        security_presence=0.2,
        thrill_boost=0.9,
        time_multipliers={
            'day': 1.2,
            'night': 0.6,
            'weekend_day': 1.1,
            'weekend_night': 0.5
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.STAIRS: PublicLocation(
        area=PublicArea.STAIRS,
        name="Tangga Darurat",
        description="Tangga darurat sepi, hanya suara langkah kaki.",
        base_risk=0.4,
        crowd_density=0.1,
        cctv_coverage=0.1,
        security_presence=0.1,
        thrill_boost=0.7,
        time_multipliers={
            'day': 0.8,
            'night': 0.4,
            'weekend_day': 0.7,
            'weekend_night': 0.3
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.CAR: PublicLocation(
        area=PublicArea.CAR,
        name="Mobil",
        description="Mobil pribadi, agak aman tapi kaca bisa berkabut.",
        base_risk=0.3,
        crowd_density=0.0,
        cctv_coverage=0.2,
        security_presence=0.1,
        thrill_boost=0.6,
        time_multipliers={
            'day': 1.2,
            'night': 0.5,
            'weekend_day': 1.0,
            'weekend_night': 0.4
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.CAR_PARKED: PublicLocation(
        area=PublicArea.CAR_PARKED,
        name="Mobil Parkir",
        description="Mobil parkir di tempat sepi, risiko sedang.",
        base_risk=0.5,
        crowd_density=0.2,
        cctv_coverage=0.5,
        security_presence=0.3,
        thrill_boost=0.7,
        time_multipliers={
            'day': 1.1,
            'night': 0.5,
            'weekend_day': 1.2,
            'weekend_night': 0.6
        },
        best_time="night",
        worst_time="day"
    ),
    
    # Gedung
    PublicArea.ROOFTOP: PublicLocation(
        area=PublicArea.ROOFTOP,
        name="Atap Gedung",
        description="Atap gedung tinggi dengan pemandangan kota, risiko jatuh.",
        base_risk=0.5,
        crowd_density=0.0,
        cctv_coverage=0.1,
        security_presence=0.1,
        thrill_boost=0.9,
        time_multipliers={
            'day': 1.1,
            'night': 0.4,
            'weekend_day': 1.0,
            'weekend_night': 0.3
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.OFFICE_NIGHT: PublicLocation(
        area=PublicArea.OFFICE_NIGHT,
        name="Kantor Malam",
        description="Kantor kosong di malam hari, hanya satpam keliling.",
        base_risk=0.4,
        crowd_density=0.0,
        cctv_coverage=0.7,
        security_presence=0.5,
        thrill_boost=0.7,
        time_multipliers={
            'day': 0.2,
            'night': 0.6,
            'weekend_day': 0.1,
            'weekend_night': 0.5
        },
        best_time="night",
        worst_time="day"
    ),
    
    PublicArea.SCHOOL_NIGHT: PublicLocation(
        area=PublicArea.SCHOOL_NIGHT,
        name="Sekolah Malam",
        description="Sekolah kosong di malam hari, membangkitkan kenangan.",
        base_risk=0.5,
        crowd_density=0.0,
        cctv_coverage=0.4,
        security_presence=0.3,
        thrill_boost=0.8,
        time_multipliers={
            'day': 0.3,
            'night': 0.5,
            'weekend_day': 0.2,
            'weekend_night': 0.4
        },
        best_time="night",
        worst_time="day"
    ),
    
    # Hiburan
    PublicArea.KARAOKE: PublicLocation(
        area=PublicArea.KARAOKE,
        name="Karaoke",
        description="Ruangan karaoke privat, agak aman tapi suara tembus.",
        base_risk=0.3,
        crowd_density=0.2,
        cctv_coverage=0.3,
        security_presence=0.2,
        thrill_boost=0.6,
        time_multipliers={
            'day': 0.8,
            'night': 1.2,
            'weekend_day': 0.9,
            'weekend_night': 1.3
        },
        best_time="day",
        worst_time="night"
    ),
    
    PublicArea.CLUB: PublicLocation(
        area=PublicArea.CLUB,
        name="Club Malam",
        description="Club dengan musik keras dan lampu gelap, banyak orang.",
        base_risk=0.6,
        crowd_density=0.9,
        cctv_coverage=0.5,
        security_presence=0.7,
        thrill_boost=0.8,
        time_multipliers={
            'day': 0.2,
            'night': 1.3,
            'weekend_day': 0.3,
            'weekend_night': 1.5
        },
        best_time="day",
        worst_time="weekend_night"
    ),
    
    PublicArea.CLUB_TOILET: PublicLocation(
        area=PublicArea.CLUB_TOILET,
        name="Toilet Club",
        description="Toilet club yang ramai, sering dipakai untuk hal serupa.",
        base_risk=0.7,
        crowd_density=0.7,
        cctv_coverage=0.2,
        security_presence=0.3,
        thrill_boost=0.8,
        time_multipliers={
            'day': 0.4,
            'night': 1.2,
            'weekend_day': 0.5,
            'weekend_night': 1.4
        },
        best_time="day",
        worst_time="night"
    ),
    
    # Tempat ekstrim
    PublicArea.CEMETERY: PublicLocation(
        area=PublicArea.CEMETERY,
        name="Kuburan",
        description="Area pemakaman yang sepi, mistis, bikin merinding.",
        base_risk=0.3,
        crowd_density=0.0,
        cctv_coverage=0.0,
        security_presence=0.0,
        thrill_boost=1.0,
        time_multipliers={
            'day': 0.6,
            'night': 1.5,
            'weekend_day': 0.5,
            'weekend_night': 1.8
        },
        best_time="day",
        worst_time="night"
    ),
    
    PublicArea.CHANGING_ROOM: PublicLocation(
        area=PublicArea.CHANGING_ROOM,
        name="Ruang Ganti",
        description="Ruang ganti toko baju, cermin besar, risiko sedang.",
        base_risk=0.5,
        crowd_density=0.4,
        cctv_coverage=0.2,
        security_presence=0.3,
        thrill_boost=0.7,
        time_multipliers={
            'day': 1.3,
            'night': 0.4,
            'weekend_day': 1.4,
            'weekend_night': 0.5
        },
        best_time="night",
        worst_time="day"
    )
}


class LocationManager:
    """Manager untuk semua lokasi"""
    
    def __init__(self):
        self.locations = LOCATIONS
    
    def get_location(self, area: PublicArea) -> Optional[PublicLocation]:
        """Get location by area"""
        return self.locations.get(area)
    
    def get_locations_by_risk(self, max_risk: float = 1.0) -> List[PublicLocation]:
        """Get locations with risk <= max_risk"""
        return [loc for loc in self.locations.values() if loc.base_risk <= max_risk]
    
    def get_locations_by_thrill(self, min_thrill: float = 0.5) -> List[PublicLocation]:
        """Get locations with thrill boost >= min_thrill"""
        return [loc for loc in self.locations.values() if loc.thrill_boost >= min_thrill]
    
    def get_random_location(self, risk_range: Tuple[float, float] = (0.0, 1.0)) -> Optional[PublicLocation]:
        """Get random location within risk range"""
        import random
        suitable = [loc for loc in self.locations.values() 
                   if risk_range[0] <= loc.base_risk <= risk_range[1]]
        return random.choice(suitable) if suitable else None
    
    def get_all_locations(self) -> List[Dict]:
        """Get all locations as dict"""
        return [loc.to_dict() for loc in self.locations.values()]
    
    def search_locations(self, query: str) -> List[PublicLocation]:
        """Search locations by name/description"""
        query = query.lower()
        results = []
        for loc in self.locations.values():
            if query in loc.name.lower() or query in loc.description.lower():
                results.append(loc)
        return results


__all__ = [
    'PublicArea',
    'PublicLocation',
    'LOCATIONS',
    'LocationManager'
]
