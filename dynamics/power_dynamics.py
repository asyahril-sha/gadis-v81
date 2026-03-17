#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
POWER DYNAMICS SYSTEM
=============================================================================
Dinamika kekuasaan dalam hubungan seksual - dominant/submissive dynamics
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime


class DominanceLevel(Enum):
    """Level dominasi"""
    SUBMISSIVE = "patuh"
    SUBMISSIVE_LIGHT = "agak patuh"
    SWITCH = "switch"
    DOMINANT_LIGHT = "agak dominan"
    DOMINANT = "dominan"
    VERY_DOMINANT = "sangat dominan"
    AGGRESSIVE = "agresif"


class PowerExchangeType(Enum):
    """Tipe power exchange"""
    GIVING_CONTROL = "memberi kontrol"
    TAKING_CONTROL = "mengambil kontrol"
    SWITCHING = "bertukar"
    NEGOTIATING = "negosiasi"


class PowerDynamics:
    """Sistem dinamika kekuasaan dalam hubungan"""
    
    def __init__(self):
        self.current_level = DominanceLevel.SWITCH
        self.dominance_score = 0.5  # 0 = submissive, 1 = dominant
        self.dominance_history = []
        
        # Triggers untuk perubahan dominasi
        self.dominance_triggers = {
            'kamu yang atur': +0.2,
            'aku yang atur': -0.2,
            'kamu dominan': +0.15,
            'aku dominan': -0.15,
            'kamu boss': +0.1,
            'aku boss': -0.1,
            'patuh': +0.1,
            'ikut kamu': +0.1,
            'terserah kamu': +0.15,
            'siap': -0.05,
            'iya tuan': -0.2,
            'iya nyonya': +0.2,
        }
        
        # Respons berdasarkan level dominasi
        self.dominant_responses = {
            'accept': [
                "Iya, ikut kamu.",
                "Terserah kamu aja.",
                "Kamu yang atur."
            ],
            'reject': [
                "Nggak mau, aku yang atur.",
                "Jangan, aku nggak suka.",
                "Enggak ah."
            ],
            'command': [
                "Lakukan sekarang!",
                "Cepat, jangan banyak tanya.",
                "Ikut perintahku!"
            ],
            'request': [
                "Boleh minta?",
                "Kalau nggak keberatan...",
                "Mau nggak kalau..."
            ]
        }
        
        self.submissive_responses = {
            'accept': [
                "Baik, Tuan/Nyonya.",
                "Siap laksanakan.",
                "Iya, sesuai perintah."
            ],
            'reject': [
                "Maaf, aku nggak bisa...",
                "Ampun, jangan...",
                "Tolong jangan..."
            ],
            'beg': [
                "Kumohon...",
                "Please... aku mau...",
                "Jangan gitu dong..."
            ]
        }
    
    def update_from_message(self, message: str) -> Optional[float]:
        """Update dominance based on message content"""
        msg_lower = message.lower()
        
        for trigger, delta in self.dominance_triggers.items():
            if trigger in msg_lower:
                self.dominance_score += delta
                self.dominance_score = max(0.0, min(1.0, self.dominance_score))
                
                self.dominance_history.append({
                    'timestamp': datetime.now(),
                    'trigger': trigger,
                    'delta': delta,
                    'new_score': self.dominance_score
                })
                
                return delta
        
        return None
    
    def update_from_activity(self, activity: str, role: str = 'active') -> float:
        """Update dominance based on sexual activity"""
        delta = 0.0
        
        if role == 'active':
            delta += 0.05
        elif role == 'passive':
            delta -= 0.05
        
        if activity in ['penetration', 'dominant_action']:
            delta += 0.1
        elif activity in ['receiving', 'submissive_action']:
            delta -= 0.1
        
        self.dominance_score += delta
        self.dominance_score = max(0.0, min(1.0, self.dominance_score))
        
        return delta
    
    def get_current_level(self) -> DominanceLevel:
        """Get current dominance level based on score"""
        if self.dominance_score < 0.2:
            return DominanceLevel.SUBMISSIVE
        elif self.dominance_score < 0.35:
            return DominanceLevel.SUBMISSIVE_LIGHT
        elif self.dominance_score < 0.45:
            return DominanceLevel.SWITCH
        elif self.dominance_score < 0.55:
            return DominanceLevel.SWITCH
        elif self.dominance_score < 0.65:
            return DominanceLevel.DOMINANT_LIGHT
        elif self.dominance_score < 0.8:
            return DominanceLevel.DOMINANT
        elif self.dominance_score < 0.9:
            return DominanceLevel.VERY_DOMINANT
        else:
            return DominanceLevel.AGGRESSIVE
    
    def get_response_style(self, response_type: str) -> str:
        """Get response based on current dominance level"""
        level = self.get_current_level()
        
        if level in [DominanceLevel.DOMINANT, DominanceLevel.VERY_DOMINANT, DominanceLevel.AGGRESSIVE]:
            # Dominant style
            if response_type in self.dominant_responses:
                return random.choice(self.dominant_responses[response_type])
            elif response_type == 'command':
                return random.choice(self.dominant_responses['command'])
            else:
                return random.choice(self.dominant_responses['request'])
        
        elif level in [DominanceLevel.SUBMISSIVE, DominanceLevel.SUBMISSIVE_LIGHT]:
            # Submissive style
            if response_type in self.submissive_responses:
                return random.choice(self.submissive_responses[response_type])
            elif response_type == 'beg':
                return random.choice(self.submissive_responses['beg'])
            else:
                return random.choice(self.submissive_responses['accept'])
        
        else:
            # Switch/Normal style
            if response_type == 'accept':
                return random.choice(["Iya", "Boleh", "Oke"])
            elif response_type == 'reject':
                return random.choice(["Nggak", "Enggak mau", "Lain kali"])
            else:
                return "..."
    
    def can_dominate(self) -> bool:
        """Check if bot can be dominant"""
        return self.dominance_score > 0.6
    
    def can_submit(self) -> bool:
        """Check if bot can be submissive"""
        return self.dominance_score < 0.4
    
    def negotiate_power(self, requested_level: DominanceLevel) -> Tuple[bool, str]:
        """Negotiate power exchange"""
        current = self.get_current_level()
        
        # Check compatibility
        if requested_level in [DominanceLevel.DOMINANT, DominanceLevel.VERY_DOMINANT]:
            if current in [DominanceLevel.SUBMISSIVE, DominanceLevel.SUBMISSIVE_LIGHT]:
                return True, "Cocok, aku akan patuh padamu"
            elif current in [DominanceLevel.DOMINANT, DominanceLevel.VERY_DOMINANT]:
                return False, "Kita sama-sama dominan, bisa ribut nih"
            else:
                return True, "Boleh, kita coba"
        
        elif requested_level in [DominanceLevel.SUBMISSIVE, DominanceLevel.SUBMISSIVE_LIGHT]:
            if current in [DominanceLevel.DOMINANT, DominanceLevel.VERY_DOMINANT]:
                return True, "Cocok, aku akan memandumu"
            elif current in [DominanceLevel.SUBMISSIVE, DominanceLevel.SUBMISSIVE_LIGHT]:
                return False, "Kita sama-sama patuh, jadi bingung"
            else:
                return True, "Boleh, aku coba jadi dominan"
        
        return True, "Boleh, kita coba"
    
    def get_power_description(self) -> str:
        """Get description of current power dynamics"""
        level = self.get_current_level()
        
        descriptions = {
            DominanceLevel.SUBMISSIVE: "Sangat patuh, siap melayani semua perintah",
            DominanceLevel.SUBMISSIVE_LIGHT: "Cenderung patuh, tapi masih bisa menolak",
            DominanceLevel.SWITCH: "Fleksibel, bisa dominan bisa patuh tergantung situasi",
            DominanceLevel.DOMINANT_LIGHT: "Agak dominan, suka mengatur sedikit",
            DominanceLevel.DOMINANT: "Dominan, suka memegang kendali",
            DominanceLevel.VERY_DOMINANT: "Sangat dominan, hampir semua harus sesuai keinginan",
            DominanceLevel.AGGRESSIVE: "Agresif, cenderung memaksa"
        }
        
        return descriptions.get(level, "Normal")
    
    def get_power_score(self) -> Dict:
        """Get power dynamics scores"""
        return {
            'dominance_score': round(self.dominance_score, 2),
            'current_level': self.get_current_level().value,
            'description': self.get_power_description(),
            'can_dominate': self.can_dominate(),
            'can_submit': self.can_submit()
        }
    
    def reset(self):
        """Reset to default"""
        self.dominance_score = 0.5
        self.dominance_history = []


class PowerExchange:
    """Power exchange session tracking"""
    
    def __init__(self, dominant_id: int, submissive_id: int):
        self.dominant_id = dominant_id
        self.submissive_id = submissive_id
        self.start_time = datetime.now()
        self.end_time = None
        self.exchanges = []
        self.rules = []
        self.safe_word = "merah"
        
        # Session stats
        self.commands_given = 0
        self.commands_followed = 0
        self.boundaries_respected = True
        self.aftercare_needed = False
    
    def add_command(self, command: str, followed: bool):
        """Record a command during power exchange"""
        self.exchanges.append({
            'timestamp': datetime.now(),
            'type': 'command',
            'content': command,
            'followed': followed
        })
        
        self.commands_given += 1
        if followed:
            self.commands_followed += 1
    
    def add_rule(self, rule: str):
        """Add a rule to the session"""
        self.rules.append({
            'rule': rule,
            'added_at': datetime.now()
        })
    
    def use_safe_word(self, user_id: int) -> bool:
        """Use safe word to stop session"""
        self.end_time = datetime.now()
        self.aftercare_needed = True
        return True
    
    def end_session(self, aftercare_provided: bool = False):
        """End power exchange session"""
        self.end_time = datetime.now()
        self.aftercare_needed = not aftercare_provided
    
    def get_session_summary(self) -> Dict:
        """Get session summary"""
        duration = (self.end_time or datetime.now()) - self.start_time
        
        return {
            'dominant_id': self.dominant_id,
            'submissive_id': self.submissive_id,
            'duration_minutes': duration.total_seconds() / 60,
            'commands_given': self.commands_given,
            'compliance_rate': self.commands_followed / self.commands_given if self.commands_given > 0 else 1.0,
            'rules_count': len(self.rules),
            'aftercare_needed': self.aftercare_needed
        }


class PowerDynamicsManager:
    """Manager untuk power dynamics"""
    
    def __init__(self):
        self.user_dynamics: Dict[int, PowerDynamics] = {}
        self.active_exchanges: Dict[str, PowerExchange] = {}
    
    def get_dynamics(self, user_id: int) -> PowerDynamics:
        """Get or create power dynamics for user"""
        if user_id not in self.user_dynamics:
            self.user_dynamics[user_id] = PowerDynamics()
        return self.user_dynamics[user_id]
    
    def start_power_exchange(self, dominant_id: int, submissive_id: int) -> PowerExchange:
        """Start a power exchange session"""
        exchange_id = f"pex_{datetime.now().timestamp()}_{dominant_id}_{submissive_id}"
        exchange = PowerExchange(dominant_id, submissive_id)
        self.active_exchanges[exchange_id] = exchange
        return exchange
    
    def end_power_exchange(self, exchange_id: str, aftercare: bool = False):
        """End power exchange session"""
        if exchange_id in self.active_exchanges:
            self.active_exchanges[exchange_id].end_session(aftercare)
            # Archive logic here
            del self.active_exchanges[exchange_id]
    
    def get_compatibility(self, user1_id: int, user2_id: int) -> Dict:
        """Check power dynamics compatibility between users"""
        dyn1 = self.get_dynamics(user1_id)
        dyn2 = self.get_dynamics(user2_id)
        
        level1 = dyn1.get_current_level()
        level2 = dyn2.get_current_level()
        
        # Check compatibility
        compatible = False
        description = ""
        
        if level1 in [DominanceLevel.DOMINANT, DominanceLevel.VERY_DOMINANT] and \
           level2 in [DominanceLevel.SUBMISSIVE, DominanceLevel.SUBMISSIVE_LIGHT]:
            compatible = True
            description = f"User1 dominan, User2 patuh - cocok!"
        elif level2 in [DominanceLevel.DOMINANT, DominanceLevel.VERY_DOMINANT] and \
             level1 in [DominanceLevel.SUBMISSIVE, DominanceLevel.SUBMISSIVE_LIGHT]:
            compatible = True
            description = f"User2 dominan, User1 patuh - cocok!"
        elif level1 == DominanceLevel.SWITCH and level2 == DominanceLevel.SWITCH:
            compatible = True
            description = "Sama-sama switch - bisa bergantian"
        else:
            description = "Kurang cocok, bisa konflik"
        
        return {
            'compatible': compatible,
            'description': description,
            'user1_level': level1.value,
            'user2_level': level2.value
        }
    
    def get_stats(self) -> Dict:
        """Get power dynamics statistics"""
        return {
            'total_users': len(self.user_dynamics),
            'active_exchanges': len(self.active_exchanges),
            'average_dominance': sum(d.dominance_score for d in self.user_dynamics.values()) / len(self.user_dynamics) if self.user_dynamics else 0.5
        }


__all__ = [
    'DominanceLevel',
    'PowerExchangeType',
    'PowerDynamics',
    'PowerExchange',
    'PowerDynamicsManager'
]
