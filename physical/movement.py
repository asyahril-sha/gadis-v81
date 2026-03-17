#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MOVEMENT SYSTEM
=============================================================================
Posisi tubuh dan pergerakan bot
"""

import random
from datetime import datetime
from typing import Dict, Optional
from enum import Enum


class Position(Enum):
    """Posisi tubuh"""
    SITTING = "duduk"
    STANDING = "berdiri"
    LYING = "berbaring"
    LEANING = "bersandar"
    CRAWLING = "merangkak"
    KNEELING = "berlutut"
    SQUATTING = "jongkok"
    CURLING = "meringkuk"


class MovementSystem:
    """
    Sistem posisi tubuh dan pergerakan
    Efek posisi ke arousal dan mood
    """
    
    POSITIONS = {
        Position.SITTING: {
            "name": "duduk",
            "emoji": "🧘",
            "actions": ["duduk manis", "duduk bersila", "duduk di sofa", "duduk di ranjang"],
            "arousal_effect": -0.05,  # Santai, sedikit turun arousal
            "comfort_level": 0.8
        },
        Position.STANDING: {
            "name": "berdiri",
            "emoji": "🧍",
            "actions": ["berdiri tegak", "bersandar di dinding", "berdiri di dekat jendela", "berdiri di depan cermin"],
            "arousal_effect": 0.0,
            "comfort_level": 0.6
        },
        Position.LYING: {
            "name": "berbaring",
            "emoji": "😴",
            "actions": ["berbaring di ranjang", "rebahan", "tiduran", "berbaring miring"],
            "arousal_effect": 0.1,  # Berbaring bisa naikkan arousal
            "comfort_level": 0.9
        },
        Position.LEANING: {
            "name": "bersandar",
            "emoji": "🚶",
            "actions": ["bersandar di dinding", "bersandar di pintu", "bersandar di meja"],
            "arousal_effect": 0.0,
            "comfort_level": 0.5
        },
        Position.CRAWLING: {
            "name": "merangkak",
            "emoji": "🐾",
            "actions": ["merangkak di lantai", "merayap", "merangkak di ranjang"],
            "arousal_effect": 0.2,  # Posisi seksual
            "comfort_level": 0.3
        },
        Position.KNEELING: {
            "name": "berlutut",
            "emoji": "🙏",
            "actions": ["berlutut", "bersimpuh", "berlutut di ranjang"],
            "arousal_effect": 0.15,  # Posisi seksual
            "comfort_level": 0.4
        },
        Position.SQUATTING: {
            "name": "jongkok",
            "emoji": "🏃",
            "actions": ["jongkok", "jongkok di lantai"],
            "arousal_effect": 0.05,
            "comfort_level": 0.3
        },
        Position.CURLING: {
            "name": "meringkuk",
            "emoji": "🦔",
            "actions": ["meringkuk", "memeluk lutut", "meringkuk di ranjang"],
            "arousal_effect": -0.1,  # Meringkuk karena takut/sedih
            "comfort_level": 0.7
        }
    }
    
    def __init__(self):
        self.current_position: Position = Position.SITTING
        self.last_change: datetime = datetime.now()
        self.position_history = []
    
    def get_current(self) -> Position:
        """Get current position"""
        return self.current_position
    
    def get_current_info(self) -> Dict:
        """Get current position info"""
        info = self.POSITIONS.get(self.current_position, {})
        return {
            "position": self.current_position,
            "name": info.get("name", "duduk"),
            "emoji": info.get("emoji", "🧘"),
            "action": random.choice(info.get("actions", ["diam"])),
            "arousal_effect": info.get("arousal_effect", 0),
            "comfort_level": info.get("comfort_level", 0.5)
        }
    
    def change_to(self, new_position: Position) -> bool:
        """Change to new position"""
        if new_position == self.current_position:
            return False
        
        old_position = self.current_position
        self.current_position = new_position
        self.last_change = datetime.now()
        
        # Record history
        self.position_history.append({
            'from': old_position.value,
            'to': new_position.value,
            'timestamp': datetime.now()
        })
        
        # Limit history
        if len(self.position_history) > 50:
            self.position_history = self.position_history[-50:]
        
        return True
    
    def change_random(self) -> Position:
        """Change to random position"""
        available = [pos for pos in Position if pos != self.current_position]
        if available:
            new_pos = random.choice(available)
            self.change_to(new_pos)
        return self.current_position
    
    def change_to_suggested(self, activity: str) -> Optional[Position]:
        """Change to position suggested by activity"""
        position_map = {
            'kissing': [Position.STANDING, Position.SITTING],
            'touching': [Position.SITTING, Position.LYING],
            'oral': [Position.KNEELING, Position.LYING],
            'penetration': [Position.LYING, Position.CRAWLING, Position.KNEELING],
            'cuddling': [Position.LYING, Position.SITTING],
            'standing': [Position.STANDING],
            'doggy': [Position.CRAWLING],
            'missionary': [Position.LYING],
            'cowgirl': [Position.LYING],
            'spooning': [Position.LYING],
            'sixtynine': [Position.LYING, Position.KNEELING]
        }
        
        suggestions = position_map.get(activity, [])
        if suggestions:
            new_pos = random.choice(suggestions)
            self.change_to(new_pos)
            return new_pos
        
        return None
    
    def get_change_message(self) -> str:
        """Get message when changing position"""
        info = self.get_current_info()
        action = info.get("action", info.get("name", ""))
        
        templates = [
            f"*{action}*",
            f"Aku {action}",
            f"*berganti posisi, sekarang {action}*",
            f"Sekarang aku {action}"
        ]
        
        return random.choice(templates)
    
    def get_arousal_effect(self) -> float:
        """Get arousal effect from current position"""
        info = self.POSITIONS.get(self.current_position, {})
        return info.get("arousal_effect", 0)
    
    def get_comfort_level(self) -> float:
        """Get comfort level of current position"""
        info = self.POSITIONS.get(self.current_position, {})
        return info.get("comfort_level", 0.5)
    
    def get_position_suggestion(self, mood: str) -> Optional[Position]:
        """Suggest position based on mood"""
        mood_map = {
            'horny': [Position.LYING, Position.CRAWLING, Position.KNEELING],
            'romantis': [Position.LYING, Position.SITTING],
            'malas': [Position.LYING, Position.SITTING],
            'ceria': [Position.STANDING, Position.SITTING],
            'sedih': [Position.CURLING, Position.SITTING],
            'marah': [Position.STANDING, Position.LEANING],
            'rindu': [Position.CURLING, Position.LYING]
        }
        
        suggestions = mood_map.get(mood.lower(), [Position.SITTING])
        return random.choice(suggestions) if suggestions else None
    
    def get_position_history(self, limit: int = 5) -> List[str]:
        """Get recent position changes"""
        history = []
        for entry in self.position_history[-limit:]:
            time_str = entry['timestamp'].strftime("%H:%M")
            history.append(f"{time_str}: {entry['from']} → {entry['to']}")
        return history


__all__ = ['Position', 'MovementSystem']
