#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
RISK CALCULATION SYSTEM
=============================================================================
Menghitung probabilitas ketahuan di tempat publik
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class RiskLevel(Enum):
    """Level risiko"""
    VERY_LOW = "sangat rendah"
    LOW = "rendah"
    MEDIUM = "sedang"
    HIGH = "tinggi"
    VERY_HIGH = "sangat tinggi"
    EXTREME = "ekstrim"


class RiskFactor:
    """Faktor-faktor yang mempengaruhi risiko"""
    
    def __init__(self):
        # Faktor waktu
        self.time_factors = {
            'early_morning': (4, 6, 0.3),   # jam 4-6
            'morning': (6, 11, 0.8),         # jam 6-11
            'afternoon': (11, 15, 0.9),      # jam 11-15
            'evening': (15, 18, 0.7),        # jam 15-18
            'night': (18, 22, 0.5),          # jam 18-22
            'late_night': (22, 4, 0.2)       # jam 22-4
        }
        
        # Faktor hari
        self.weekend_multiplier = 1.3
        self.weekday_multiplier = 0.8
        
        # Faktor lokasi
        self.crowd_factor = 0.3      # Setiap 10% keramaian nambah 0.3
        self.cctv_factor = 0.25       # Setiap 10% CCTV nambah 0.25
        self.security_factor = 0.35    # Setiap 10% security nambah 0.35
        
        # Faktor aktivitas
        self.activity_noise = {
            'kissing': 0.1,
            'touching': 0.2,
            'oral': 0.4,
            'penetration': 0.5,
            'moaning': 0.6,
            'screaming': 0.9
        }
        
        # Faktor durasi
        self.duration_factor = 0.1     # Per menit tambah 0.1


class RiskCalculator:
    """Kalkulator risiko untuk aktivitas publik"""
    
    def __init__(self):
        self.factors = RiskFactor()
        
        # Track record
        self.total_calculations = 0
        self.average_risk = 0.0
        self.risk_history = []
    
    def calculate_risk(self,
                      location,
                      hour: int = None,
                      is_weekend: bool = None,
                      activity_type: str = 'touching',
                      duration: int = 5,
                      experience_level: int = 1,
                      arousal_level: float = 0.5,
                      has_partner: bool = True) -> Dict:
        """
        Hitung risiko ketahuan
        
        Returns:
            Dict dengan detail risiko
        """
        
        if hour is None:
            hour = datetime.now().hour
        
        if is_weekend is None:
            is_weekend = datetime.now().weekday() >= 5
        
        # Base risk dari lokasi
        base_risk = location.base_risk
        
        # Time factor
        time_factor = self._get_time_factor(hour)
        
        # Day factor
        day_multiplier = self.factors.weekend_multiplier if is_weekend else self.factors.weekday_multiplier
        
        # Location factors
        crowd_contribution = location.crowd_density * self.factors.crowd_factor
        cctv_contribution = location.cctv_coverage * self.factors.cctv_factor
        security_contribution = location.security_presence * self.factors.security_factor
        
        # Activity factor
        activity_risk = self.factors.activity_noise.get(activity_type, 0.3)
        
        # Duration factor
        duration_risk = min(1.0, (duration / 10) * self.factors.duration_factor)
        
        # Experience factor (lebih berpengalaman = lebih hati-hati)
        experience_bonus = (experience_level - 1) * 0.05  # Max 0.55 di level 12
        
        # Arousal factor (semakin horny = semakin ceroboh)
        arousal_penalty = arousal_level * 0.3
        
        # Partner factor (sendiri lebih aman?)
        partner_factor = 1.2 if has_partner else 1.0
        
        # Hitung total risk
        total_risk = (
            base_risk *
            time_factor *
            day_multiplier *
            partner_factor
        ) + (
            crowd_contribution +
            cctv_contribution +
            security_contribution +
            activity_risk +
            duration_risk +
            arousal_penalty -
            experience_bonus
        )
        
        # Clamp antara 0-1
        total_risk = max(0.05, min(0.99, total_risk))
        
        # Hitung probabilitas sukses
        success_prob = 1.0 - total_risk
        
        # Dapatkan level risiko
        risk_level = self._get_risk_level(total_risk)
        
        # Simpan history
        self.total_calculations += 1
        self.average_risk = (self.average_risk * (self.total_calculations - 1) + total_risk) / self.total_calculations
        
        result = {
            'total_risk': round(total_risk, 3),
            'success_probability': round(success_prob, 3),
            'risk_level': risk_level.value,
            'risk_level_enum': risk_level,
            'details': {
                'base_risk': base_risk,
                'time_factor': time_factor,
                'day_multiplier': day_multiplier,
                'crowd_contribution': crowd_contribution,
                'cctv_contribution': cctv_contribution,
                'security_contribution': security_contribution,
                'activity_risk': activity_risk,
                'duration_risk': duration_risk,
                'experience_bonus': experience_bonus,
                'arousal_penalty': arousal_penalty,
                'partner_factor': partner_factor
            },
            'factors': {
                'hour': hour,
                'is_weekend': is_weekend,
                'activity': activity_type,
                'duration': duration,
                'experience': experience_level,
                'arousal': arousal_level
            }
        }
        
        self.risk_history.append({
            'timestamp': datetime.now().isoformat(),
            'risk': total_risk,
            'location': location.name
        })
        
        # Keep last 100
        if len(self.risk_history) > 100:
            self.risk_history = self.risk_history[-100:]
        
        return result
    
    def _get_time_factor(self, hour: int) -> float:
        """Get time multiplier based on hour"""
        for period, (start, end, factor) in self.factors.time_factors.items():
            if start <= end:
                if start <= hour < end:
                    return factor
            else:  # Cross midnight (e.g., 22-4)
                if hour >= start or hour < end:
                    return factor
        return 1.0
    
    def _get_risk_level(self, risk: float) -> RiskLevel:
        """Convert risk value to RiskLevel"""
        if risk < 0.1:
            return RiskLevel.VERY_LOW
        elif risk < 0.3:
            return RiskLevel.LOW
        elif risk < 0.5:
            return RiskLevel.MEDIUM
        elif risk < 0.7:
            return RiskLevel.HIGH
        elif risk < 0.9:
            return RiskLevel.VERY_HIGH
        else:
            return RiskLevel.EXTREME
    
    def simulate_outcome(self, risk: float) -> Tuple[bool, str]:
        """
        Simulasikan outcome berdasarkan risiko
        
        Returns:
            (success, message)
        """
        random_num = random.random()
        success = random_num > risk
        
        if success:
            # Berhasil
            messages = [
                "Berhasil! Nggak ada yang lihat.",
                "Aman! Cepat-cepat pergi.",
                "Hampir ketahuan tapi selamat.",
                "Deg-degan tapi puas!"
            ]
        else:
            # Gagal - ketahuan
            messages = [
                "⚠️ Ada orang! Cepat lari!",
                "😱 KETA UAN! Malu banget...",
                "Satpam lewat! Cepat berpura-pura!",
                "Ada CCTV! Nanti viral..."
            ]
        
        return success, random.choice(messages)
    
    def get_risk_advice(self, risk_result: Dict) -> List[str]:
        """Get advice based on risk calculation"""
        advice = []
        
        risk_level = risk_result['risk_level_enum']
        details = risk_result['details']
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH, RiskLevel.EXTREME]:
            advice.append("⚠️ Risiko sangat tinggi! Lebih baik cari tempat lain.")
        
        if details['crowd_contribution'] > 0.2:
            advice.append("👥 Tempat ini terlalu ramai, cari yang lebih sepi.")
        
        if details['cctv_contribution'] > 0.2:
            advice.append("📸 Banyak CCTV, awas ketahuan!")
        
        if details['security_contribution'] > 0.2:
            advice.append("👮 Satpam keliling, hati-hati.")
        
        if details['activity_risk'] > 0.4:
            advice.append("🔊 Aktivitas terlalu berisik, pelan-pelan.")
        
        if details['duration_risk'] > 0.3:
            advice.append("⏰ Terlalu lama, cepat-cepat.")
        
        if details['arousal_penalty'] > 0.2:
            advice.append("🔥 Tenangkan diri dulu, kamu terlalu horny.")
        
        if not advice:
            advice.append("✅ Risiko terkendali, gas aja!")
        
        return advice
    
    def compare_locations(self, loc1, loc2, **kwargs) -> Dict:
        """Compare risk between two locations"""
        risk1 = self.calculate_risk(loc1, **kwargs)
        risk2 = self.calculate_risk(loc2, **kwargs)
        
        better = loc1 if risk1['total_risk'] < risk2['total_risk'] else loc2
        
        return {
            'location1': {
                'name': loc1.name,
                'risk': risk1['total_risk'],
                'level': risk1['risk_level']
            },
            'location2': {
                'name': loc2.name,
                'risk': risk2['total_risk'],
                'level': risk2['risk_level']
            },
            'safer_location': better.name,
            'risk_difference': abs(risk1['total_risk'] - risk2['total_risk'])
        }
    
    def get_stats(self) -> Dict:
        """Get calculator statistics"""
        return {
            'total_calculations': self.total_calculations,
            'average_risk': round(self.average_risk, 3),
            'recent_risks': [h['risk'] for h in self.risk_history[-10:]]
        }


__all__ = [
    'RiskLevel',
    'RiskFactor',
    'RiskCalculator'
]
