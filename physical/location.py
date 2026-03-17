#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
LOCATION SYSTEM
=============================================================================
Tracking lokasi dan pergerakan bot di dalam rumah
"""

import random
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict

from database.enums import Location, Mood


class LocationSystem:
    """
    Sistem lokasi dan pergerakan bot
    10+ lokasi dasar di dalam rumah
    """
    
    LOCATIONS = {
        Location.LIVING_ROOM: {
            "name": "ruang tamu",
            "emoji": "🛋️",
            "description": "ruang tamu yang nyaman dengan sofa empuk",
            "activities": ["nonton TV", "baca buku", "santai", "ngobrol"],
            "mood_effect": [Mood.CERIA, Mood.RILEKS]
        },
        Location.BEDROOM: {
            "name": "kamar tidur",
            "emoji": "🛏️",
            "description": "kamar tidur dengan ranjang besar dan lampu redup",
            "activities": ["rebahan", "tiduran", "ganti baju", "bercermin"],
            "mood_effect": [Mood.RILEKS, Mood.MALAS, Mood.RINDU, Mood.HORNY]
        },
        Location.KITCHEN: {
            "name": "dapur",
            "emoji": "🍳",
            "description": "dapur bersih dengan aroma masakan",
            "activities": ["masak", "makan", "minum", "cuci piring"],
            "mood_effect": [Mood.CERIA, Mood.BERSEMANGAT]
        },
        Location.BATHROOM: {
            "name": "kamar mandi",
            "emoji": "🚿",
            "description": "kamar mandi dengan air hangat",
            "activities": ["mandi", "keramas", "bercermin", "ganti baju"],
            "mood_effect": [Mood.RILEKS, Mood.SENDIRI]
        },
        Location.BALCONY: {
            "name": "balkon",
            "emoji": "🌆",
            "description": "balkon dengan pemandangan kota",
            "activities": ["lihat pemandangan", "minum kopi", "melamun"],
            "mood_effect": [Mood.RILEKS, Mood.SENDIRI, Mood.RINDU]
        },
        Location.TERRACE: {
            "name": "teras",
            "emoji": "🏡",
            "description": "teras depan dengan tanaman hijau",
            "activities": ["duduk santai", "baca koran", "lihat orang lewat"],
            "mood_effect": [Mood.CERIA, Mood.RILEKS]
        },
        Location.GARDEN: {
            "name": "taman",
            "emoji": "🌺",
            "description": "taman belakang dengan bunga-bunga",
            "activities": ["siram tanaman", "jalan-jalan", "duduk di rumput"],
            "mood_effect": [Mood.CERIA, Mood.BERSEMANGAT]
        },
        Location.HOTEL: {
            "name": "hotel",
            "emoji": "🏨",
            "description": "hotel mewah dengan kamar romantis",
            "activities": ["check-in", "mandi", "tiduran", "pesan room service"],
            "mood_effect": [Mood.ROMANTIS, Mood.HORNY, Mood.NAKAL]
        },
        Location.CAFE: {
            "name": "cafe",
            "emoji": "☕",
            "description": "cafe cozy dengan musik jazz",
            "activities": ["minum kopi", "makan pastry", "ngobrol", "selfie"],
            "mood_effect": [Mood.CERIA, Mood.ROMANTIS]
        }
    }
    
    def __init__(self):
        self.current_location: Location = Location.LIVING_ROOM
        self.location_since: datetime = datetime.now()
        self.move_cooldown: int = 30  # detik, minimal 30 detik di satu lokasi
        self.visited_locations: List[Tuple[Location, datetime]] = []
    
    def get_current(self) -> Location:
        """Get current location"""
        return self.current_location
    
    def get_current_info(self) -> Dict:
        """Get current location info"""
        info = self.LOCATIONS.get(self.current_location, {})
        return {
            "location": self.current_location,
            "name": info.get("name", "ruang tamu"),
            "emoji": info.get("emoji", "🏠"),
            "description": info.get("description", ""),
            "time_here": self.get_time_here(),
            "activity": self.get_activity()
        }
    
    def get_time_here(self) -> int:
        """Get duration at current location (seconds)"""
        return int((datetime.now() - self.location_since).total_seconds())
    
    def can_move(self) -> bool:
        """Check if can move to another location"""
        return self.get_time_here() >= self.move_cooldown
    
    def move_to(self, new_location: Location) -> bool:
        """Move to new location"""
        if not self.can_move() or new_location == self.current_location:
            return False
        
        # Record previous location
        self.visited_locations.append((self.current_location, self.location_since))
        
        # Update to new location
        self.current_location = new_location
        self.location_since = datetime.now()
        
        # Limit history
        if len(self.visited_locations) > 20:
            self.visited_locations = self.visited_locations[-20:]
        
        return True
    
    def move_random(self) -> Tuple[bool, Optional[Location]]:
        """Move to random location"""
        if not self.can_move():
            return False, None
        
        available = [loc for loc in Location if loc != self.current_location]
        new_loc = random.choice(available)
        success = self.move_to(new_loc)
        return success, new_loc if success else None
    
    def move_to_bedroom(self) -> bool:
        """Move to bedroom (khusus inisiatif)"""
        return self.move_to(Location.BEDROOM)
    
    def get_activity(self) -> str:
        """Get random activity based on location"""
        info = self.LOCATIONS.get(self.current_location, {})
        activities = info.get("activities", ["diam saja"])
        return random.choice(activities)
    
    def get_move_message(self) -> str:
        """Get message when moving"""
        info = self.LOCATIONS.get(self.current_location, {})
        name = info.get("name", "ruang tamu")
        emoji = info.get("emoji", "🏠")
        
        templates = [
            f"*pindah ke {name}* {emoji}",
            f"Aku ke {name} dulu ya {emoji}",
            f"*jalan ke {name}*",
            f"*masuk ke {name}* {emoji}",
            f"Sekarang aku di {name} {emoji}"
        ]
        
        return random.choice(templates)
    
    def get_suggested_mood(self) -> Optional[Mood]:
        """Get mood suggestion for current location"""
        info = self.LOCATIONS.get(self.current_location, {})
        moods = info.get("mood_effect", [])
        return random.choice(moods) if moods else None
    
    def get_visited_history(self, limit: int = 5) -> List[str]:
        """Get history of visited locations"""
        history = []
        for loc, timestamp in self.visited_locations[-limit:]:
            info = self.LOCATIONS.get(loc, {})
            name = info.get("name", "?")
            time_str = self._format_time_ago(timestamp)
            history.append(f"{name} ({time_str})")
        return history
    
    def _format_time_ago(self, timestamp: datetime) -> str:
        """Format timestamp jadi 'X menit yang lalu'"""
        delta = datetime.now() - timestamp
        seconds = delta.total_seconds()
        
        if seconds < 60:
            return "baru saja"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} menit lalu"
        else:
            hours = int(seconds // 3600)
            return f"{hours} jam lalu"
    
    def reset(self):
        """Reset to initial location"""
        self.current_location = Location.LIVING_ROOM
        self.location_since = datetime.now()
        self.visited_locations = []


__all__ = ['LocationSystem']
