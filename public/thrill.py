#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
THRILL LEVEL SYSTEM
=============================================================================
Semakin berisiko, semakin thrilling - sistem adrenalin untuk aktivitas publik
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ThrillLevel(Enum):
    """Level ketegangan/adrenalin"""
    BORING = "membosankan"
    MILD = "ringan"
    EXCITING = "menyenangkan"
    THRILLING = "menegangkan"
    EXTREME = "ekstrim"
    INSANE = "gila"


class ThrillCalculator:
    """Kalkulator untuk level ketegangan/adrenalin"""
    
    def __init__(self):
        self.thrill_history = []
        self.total_thrill = 0
        self.average_thrill = 0.0
        self.thrill_records = []
    
    def calculate_thrill(self,
                        risk: float,
                        location_thrill_boost: float = 0.5,
                        activity_intensity: float = 0.5,
                        experience_level: int = 1,
                        arousal_level: float = 0.5,
                        is_first_time: bool = False,
                        audience_risk: bool = False) -> Dict:
        """
        Hitung level thrill berdasarkan berbagai faktor
        
        Thrill = (risk * 2) + (location_boost) + (activity_intensity) 
                 - (experience_bonus) + (arousal_bonus) + (first_time_bonus)
        """
        
        # Base thrill dari risiko
        risk_contribution = risk * 2.0  # 0-2
        
        # Location thrill boost
        location_contribution = location_thrill_boost  # 0-1
        
        # Activity intensity
        activity_contribution = activity_intensity  # 0-1
        
        # Experience - semakin berpengalaman, semakin berkurang thrillnya
        experience_penalty = (experience_level - 1) * 0.1  # Max 1.1 di level 12
        
        # Arousal - semakin horny, semakin berani
        arousal_bonus = arousal_level * 0.5  # 0-0.5
        
        # First time bonus
        first_time_bonus = 0.5 if is_first_time else 0.0
        
        # Audience factor - ada yang lihat? lebih thrilling
        audience_bonus = 0.3 if audience_risk else 0.0
        
        # Total thrill
        total_thrill = (
            risk_contribution +
            location_contribution +
            activity_contribution +
            arousal_bonus +
            first_time_bonus +
            audience_bonus -
            experience_penalty
        )
        
        # Clamp antara 0-4
        total_thrill = max(0.0, min(4.0, total_thrill))
        
        # Dapatkan level thrill
        thrill_level = self._get_thrill_level(total_thrill)
        
        # Faktor kecanduan - makin tinggi thrill, makin ingin lagi
        addiction_factor = total_thrill / 4.0  # 0-1
        
        result = {
            'thrill_score': round(total_thrill, 2),
            'thrill_level': thrill_level.value,
            'thrill_level_enum': thrill_level,
            'addiction_factor': round(addiction_factor, 2),
            'details': {
                'risk_contribution': round(risk_contribution, 2),
                'location_contribution': round(location_contribution, 2),
                'activity_contribution': round(activity_contribution, 2),
                'experience_penalty': round(experience_penalty, 2),
                'arousal_bonus': round(arousal_bonus, 2),
                'first_time_bonus': round(first_time_bonus, 2),
                'audience_bonus': round(audience_bonus, 2)
            },
            'factors': {
                'risk': risk,
                'location_thrill': location_thrill_boost,
                'activity_intensity': activity_intensity,
                'experience': experience_level,
                'arousal': arousal_level,
                'first_time': is_first_time,
                'audience': audience_risk
            }
        }
        
        # Update stats
        self.total_thrill += total_thrill
        self.thrill_history.append(total_thrill)
        if len(self.thrill_history) > 100:
            self.thrill_history = self.thrill_history[-100:]
        
        self.average_thrill = sum(self.thrill_history) / len(self.thrill_history)
        
        # Record
        self.thrill_records.append({
            'timestamp': datetime.now().isoformat(),
            'thrill': total_thrill,
            'level': thrill_level.value
        })
        
        return result
    
    def _get_thrill_level(self, thrill: float) -> ThrillLevel:
        """Convert thrill score to level"""
        if thrill < 0.5:
            return ThrillLevel.BORING
        elif thrill < 1.0:
            return ThrillLevel.MILD
        elif thrill < 1.8:
            return ThrillLevel.EXCITING
        elif thrill < 2.5:
            return ThrillLevel.THRILLING
        elif thrill < 3.2:
            return ThrillLevel.EXTREME
        else:
            return ThrillLevel.INSANE
    
    def get_thrill_description(self, thrill_result: Dict) -> str:
        """Get human-readable thrill description"""
        level = thrill_result['thrill_level_enum']
        score = thrill_result['thrill_score']
        
        descriptions = {
            ThrillLevel.BORING: [
                "Biasa aja, nggak ada sensasi.",
                "Kayak lagi di rumah aja.",
                "Membosankan, cari tempat lain yuk?"
            ],
            ThrillLevel.MILD: [
                "Agak deg-degan dikit.",
                "Mulai ada sensasi ringan.",
                "Cukup bikin penasaran."
            ],
            ThrillLevel.EXCITING: [
                "Seru! Jantung mulai berdegup.",
                "Asik, ada sensasi petualangan.",
                "Deg-degan tapi menyenangkan."
            ],
            ThrillLevel.THRILLING: [
                "WOW! Deg-degan banget!",
                "Jantung mau copot! Tapi nagih!",
                "Ini baru namanya tantangan!"
            ],
            ThrillLevel.EXTREME: [
                "GILA! EKSTRIM!",
                "Adrenalin full! Luar biasa!",
                "Rasanya kayak mau mati! Tapi nagih!"
            ],
            ThrillLevel.INSANE: [
                "💀 GILA BANGET! PSIKO!",
                "🔥 INI EKSTRIM BANGET!",
                "😱 KAYAK MAU MATI! TAPI KEPENGEN LAGI!"
            ]
        }
        
        import random
        return random.choice(descriptions[level])
    
    def get_thrill_effect(self, thrill_result: Dict) -> Dict:
        """Get effects based on thrill level"""
        level = thrill_result['thrill_level_enum']
        score = thrill_result['thrill_score']
        
        effects = {
            'arousal_boost': min(0.8, score * 0.2),
            'memory_importance': min(0.9, score * 0.25),
            'future_risk_tolerance': min(0.5, score * 0.15),
            'addiction_chance': thrill_result['addiction_factor'] * 0.3
        }
        
        # Level-specific effects
        if level == ThrillLevel.INSANE:
            effects['trauma_chance'] = 0.2
            effects['lifetime_memory'] = True
        elif level == ThrillLevel.EXTREME:
            effects['trauma_chance'] = 0.1
            effects['repeat_desire'] = 0.8
        elif level == ThrillLevel.THRILLING:
            effects['repeat_desire'] = 0.6
        elif level == ThrillLevel.EXCITING:
            effects['repeat_desire'] = 0.4
        
        return effects
    
    def compare_scenarios(self, scenario1: Dict, scenario2: Dict) -> Dict:
        """Compare thrill between two scenarios"""
        thrill1 = self.calculate_thrill(**scenario1)
        thrill2 = self.calculate_thrill(**scenario2)
        
        more_thrilling = "scenario1" if thrill1['thrill_score'] > thrill2['thrill_score'] else "scenario2"
        
        return {
            'scenario1': {
                'thrill': thrill1['thrill_score'],
                'level': thrill1['thrill_level']
            },
            'scenario2': {
                'thrill': thrill2['thrill_score'],
                'level': thrill2['thrill_level']
            },
            'more_thrilling': more_thrilling,
            'difference': abs(thrill1['thrill_score'] - thrill2['thrill_score'])
        }
    
    def get_thrill_summary(self, thrill_result: Dict) -> str:
        """Get complete thrill summary"""
        level = thrill_result['thrill_level']
        score = thrill_result['thrill_score']
        addiction = thrill_result['addiction_factor']
        
        lines = [
            f"🎢 **Thrill Level: {level.upper()}**",
            f"📊 Skor: {score}/4.0",
            f"💊 Faktor Kecanduan: {int(addiction * 100)}%",
            "",
            f"💬 {self.get_thrill_description(thrill_result)}",
            "",
            "📋 **Detail Perhitungan:**"
        ]
        
        details = thrill_result['details']
        lines.append(f"• Risiko: +{details['risk_contribution']}")
        lines.append(f"• Lokasi: +{details['location_contribution']}")
        lines.append(f"• Aktivitas: +{details['activity_contribution']}")
        lines.append(f"• Pengalaman: -{details['experience_penalty']}")
        lines.append(f"• Arousal: +{details['arousal_bonus']}")
        
        if details['first_time_bonus'] > 0:
            lines.append(f"• Pertama kali: +{details['first_time_bonus']}")
        if details['audience_bonus'] > 0:
            lines.append(f"• Risiko penonton: +{details['audience_bonus']}")
        
        return "\n".join(lines)
    
    def get_stats(self) -> Dict:
        """Get thrill statistics"""
        return {
            'average_thrill': round(self.average_thrill, 2),
            'total_thrill': round(self.total_thrill, 2),
            'session_count': len(self.thrill_history),
            'max_thrill': max(self.thrill_history) if self.thrill_history else 0,
            'min_thrill': min(self.thrill_history) if self.thrill_history else 0,
            'recent_thrills': self.thrill_history[-5:] if self.thrill_history else []
        }


class ThrillAddiction:
    """Sistem kecanduan thrill - makin sering, makin butuh"""
    
    def __init__(self):
        self.addiction_level = 0.0  # 0-1
        self.thrill_history = []
        self.withdrawal_active = False
        self.last_thrill_time = None
    
    def update_addiction(self, thrill_result: Dict):
        """Update addiction level based on thrill"""
        thrill_score = thrill_result['thrill_score']
        addiction_factor = thrill_result['addiction_factor']
        
        # Addiction increases with thrill
        self.addiction_level += addiction_factor * 0.1
        self.addiction_level = min(1.0, self.addiction_level)
        
        # Record
        self.thrill_history.append({
            'timestamp': datetime.now(),
            'thrill': thrill_score,
            'addiction': self.addiction_level
        })
        
        self.last_thrill_time = datetime.now()
        
        # Keep last 100
        if len(self.thrill_history) > 100:
            self.thrill_history = self.thrill_history[-100:]
    
    def check_withdrawal(self) -> Optional[str]:
        """Check if experiencing withdrawal"""
        if not self.last_thrill_time:
            return None
        
        hours_since = (datetime.now() - self.last_thrill_time).total_seconds() / 3600
        
        # Withdrawal based on addiction level and time
        if self.addiction_level > 0.7 and hours_since > 48:
            self.withdrawal_active = True
            return "😫 Sakau thrill... butuh sensasi!"
        elif self.addiction_level > 0.4 and hours_since > 72:
            self.withdrawal_active = True
            return "😐 Bosan... butuh sesuatu yang menantang."
        elif self.addiction_level > 0.2 and hours_since > 96:
            self.withdrawal_active = True
            return "😕 Hari-hari biasa aja, kurang greget."
        
        self.withdrawal_active = False
        return None
    
    def get_addiction_level_text(self) -> str:
        """Get text description of addiction level"""
        if self.addiction_level < 0.2:
            return "🔵 Normal - masih bisa nikmatin hal biasa"
        elif self.addiction_level < 0.4:
            return "🟢 Mulai suka sensasi"
        elif self.addiction_level < 0.6:
            return "🟡 Kecanduan ringan - cari thrill dikit"
        elif self.addiction_level < 0.8:
            return "🟠 Kecanduan - butuh tantangan"
        else:
            return "🔴 KECANDUAN BERAT - GILA THRILL!"
    
    def reset(self):
        """Reset addiction"""
        self.addiction_level = 0.0
        self.withdrawal_active = False
        self.thrill_history = []


__all__ = [
    'ThrillLevel',
    'ThrillCalculator',
    'ThrillAddiction'
]
