#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SEXUAL COMPATIBILITY CALCULATOR
=============================================================================
Menghitung kecocokan seksual antar user atau dengan bot
"""

import math
from typing import Dict, List, Optional, Tuple
from collections import Counter
from datetime import datetime, timedelta

from sexual.preferences import SexualPreferences


class SexualCompatibility:
    """
    Menghitung kecocokan seksual berdasarkan berbagai faktor
    """
    
    def __init__(self):
        self.compatibility_history = []
        self.match_threshold = 0.7  # 70% ke atas = cocok
    
    def calculate_compatibility(self, 
                               prefs1: SexualPreferences,
                               prefs2: SexualPreferences,
                               weights: Dict[str, float] = None) -> Dict:
        """
        Hitung kecocokan antara dua user
        
        Args:
            prefs1: Preferences user 1
            prefs2: Preferences user 2
            weights: Bobot untuk setiap kategori
        
        Returns:
            Dict dengan skor kecocokan detail
        """
        
        if weights is None:
            weights = {
                'positions': 0.25,
                'areas': 0.20,
                'activities': 0.20,
                'timing': 0.15,
                'intensity': 0.10,
                'risk': 0.10
            }
        
        # Hitung setiap kategori
        position_score = self._compare_positions(prefs1, prefs2)
        area_score = self._compare_areas(prefs1, prefs2)
        activity_score = self._compare_activities(prefs1, prefs2)
        timing_score = self._compare_timing(prefs1, prefs2)
        intensity_score = self._compare_intensity(prefs1, prefs2)
        risk_score = self._compare_risk_tolerance(prefs1, prefs2)
        
        # Hitung total dengan bobot
        total_score = (
            position_score * weights['positions'] +
            area_score * weights['areas'] +
            activity_score * weights['activities'] +
            timing_score * weights['timing'] +
            intensity_score * weights['intensity'] +
            risk_score * weights['risk']
        )
        
        # Kategorisasi
        category = self._get_category(total_score)
        
        # Rekomendasi
        recommendations = self._generate_recommendations(
            prefs1, prefs2, total_score,
            position_score, area_score, activity_score
        )
        
        result = {
            'total_score': round(total_score, 2),
            'category': category,
            'details': {
                'positions': round(position_score, 2),
                'areas': round(area_score, 2),
                'activities': round(activity_score, 2),
                'timing': round(timing_score, 2),
                'intensity': round(intensity_score, 2),
                'risk': round(risk_score, 2)
            },
            'recommendations': recommendations,
            'matched_at': datetime.now().isoformat()
        }
        
        # Simpan ke history
        self.compatibility_history.append(result)
        
        return result
    
    def _compare_positions(self, prefs1: SexualPreferences, 
                          prefs2: SexualPreferences) -> float:
        """Compare position preferences"""
        pos1 = set(p for p, _ in prefs1.get_favorite_positions(5))
        pos2 = set(p for p, _ in prefs2.get_favorite_positions(5))
        
        if not pos1 or not pos2:
            return 0.5
        
        # Jaccard similarity
        intersection = len(pos1 & pos2)
        union = len(pos1 | pos2)
        
        if union == 0:
            return 0.5
        
        return intersection / union
    
    def _compare_areas(self, prefs1: SexualPreferences,
                      prefs2: SexualPreferences) -> float:
        """Compare sensitive areas preferences"""
        areas1 = set(a for a, _ in prefs1.get_favorite_areas(5))
        areas2 = set(a for a, _ in prefs2.get_favorite_areas(5))
        
        if not areas1 or not areas2:
            return 0.5
        
        intersection = len(areas1 & areas2)
        union = len(areas1 | areas2)
        
        if union == 0:
            return 0.5
        
        return intersection / union
    
    def _compare_activities(self, prefs1: SexualPreferences,
                           prefs2: SexualPreferences) -> float:
        """Compare activity preferences"""
        acts1 = set(a for a, _ in prefs1.get_favorite_activities(5))
        acts2 = set(a for a, _ in prefs2.get_favorite_activities(5))
        
        if not acts1 or not acts2:
            return 0.5
        
        intersection = len(acts1 & acts2)
        union = len(acts1 | acts2)
        
        if union == 0:
            return 0.5
        
        return intersection / union
    
    def _compare_timing(self, prefs1: SexualPreferences,
                       prefs2: SexualPreferences) -> float:
        """Compare timing preferences"""
        hours1 = set(prefs1.get_peak_hours())
        hours2 = set(prefs2.get_peak_hours())
        
        if not hours1 or not hours2:
            return 0.5
        
        # Hitung overlap jam
        hour_overlap = len(hours1 & hours2) / 3.0 if len(hours2) > 0 else 0.5
        
        # Bandingkan hari
        days1 = set(d for d, _ in prefs1.peak_days.most_common(3))
        days2 = set(d for d, _ in prefs2.peak_days.most_common(3))
        
        day_overlap = len(days1 & days2) / 3.0 if len(days2) > 0 else 0.5
        
        return (hour_overlap + day_overlap) / 2
    
    def _compare_intensity(self, prefs1: SexualPreferences,
                          prefs2: SexualPreferences) -> float:
        """Compare intensity preferences"""
        # Rata-rata intensitas climax
        avg_intensity1 = self._average_intensity(prefs1)
        avg_intensity2 = self._average_intensity(prefs2)
        
        # Semakin dekat nilainya, semakin cocok
        diff = abs(avg_intensity1 - avg_intensity2)
        return max(0, 1 - diff)
    
    def _average_intensity(self, prefs: SexualPreferences) -> float:
        """Calculate average climax intensity"""
        intensities = prefs.climax_intensity.values()
        if not intensities:
            return 0.5
        return sum(intensities) / len(intensities)
    
    def _compare_risk_tolerance(self, prefs1: SexualPreferences,
                                prefs2: SexualPreferences) -> float:
        """Compare risk tolerance for public areas"""
        risk1 = prefs1.risk_tolerance
        risk2 = prefs2.risk_tolerance
        
        diff = abs(risk1 - risk2)
        return max(0, 1 - diff)
    
    def _get_category(self, score: float) -> str:
        """Get compatibility category"""
        if score >= 0.9:
            return "Soulmate Seksual"
        elif score >= 0.8:
            return "Sangat Cocok"
        elif score >= 0.7:
            return "Cocok"
        elif score >= 0.5:
            return "Cukup Cocok"
        elif score >= 0.3:
            return "Kurang Cocok"
        else:
            return "Tidak Cocok"
    
    def _generate_recommendations(self, prefs1: SexualPreferences,
                                  prefs2: SexualPreferences,
                                  total_score: float,
                                  pos_score: float,
                                  area_score: float,
                                  act_score: float) -> List[str]:
        """Generate recommendations to improve compatibility"""
        recommendations = []
        
        if total_score >= 0.7:
            recommendations.append("✅ Kalian sudah sangat cocok secara seksual")
        else:
            recommendations.append("📝 Masih bisa ditingkatkan kecocokannya")
        
        # Rekomendasi posisi
        if pos_score < 0.5:
            pos1 = [p for p, _ in prefs1.get_favorite_positions(2)]
            pos2 = [p for p, _ in prefs2.get_favorite_positions(2)]
            recommendations.append(
                f"💡 Coba posisi favorit: {', '.join(pos1)} (dari kamu) atau "
                f"{', '.join(pos2)} (dari dia)"
            )
        
        # Rekomendasi area
        if area_score < 0.5:
            area1 = [a for a, _ in prefs1.get_favorite_areas(2)]
            area2 = [a for a, _ in prefs2.get_favorite_areas(2)]
            recommendations.append(
                f"🔍 Eksplorasi area: {', '.join(area1)} (kamu suka) dan "
                f"{', '.join(area2)} (dia suka)"
            )
        
        # Rekomendasi waktu
        hours1 = prefs1.get_peak_hours()
        hours2 = prefs2.get_peak_hours()
        common_hours = set(hours1) & set(hours2)
        
        if common_hours:
            hour_names = [f"{h}:00" for h in common_hours]
            recommendations.append(
                f"⏰ Waktu terbaik: {', '.join(hour_names)}"
            )
        
        return recommendations
    
    def find_best_match(self, user_prefs: SexualPreferences,
                       candidates: Dict[int, SexualPreferences],
                       limit: int = 5) -> List[Tuple[int, float, Dict]]:
        """
        Find best matches from list of candidates
        
        Returns:
            List of (user_id, score, details)
        """
        matches = []
        
        for uid, prefs in candidates.items():
            if uid == user_prefs.user_id:
                continue
            
            result = self.calculate_compatibility(user_prefs, prefs)
            matches.append((uid, result['total_score'], result))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches[:limit]
    
    def get_match_summary(self, result: Dict) -> str:
        """Get human-readable match summary"""
        category = result['category']
        score = result['total_score'] * 100
        
        lines = [
            f"🎯 **Kecocokan Seksual: {score:.0f}%**",
            f"📊 Kategori: **{category}**",
            "",
            "📋 **Detail per Aspek:**",
            f"• Posisi: {result['details']['positions']*100:.0f}%",
            f"• Area Sensitif: {result['details']['areas']*100:.0f}%",
            f"• Aktivitas: {result['details']['activities']*100:.0f}%",
            f"• Waktu: {result['details']['timing']*100:.0f}%",
            f"• Intensitas: {result['details']['intensity']*100:.0f}%",
            f"• Risiko: {result['details']['risk']*100:.0f}%",
            ""
        ]
        
        if result['recommendations']:
            lines.append("💡 **Rekomendasi:**")
            for rec in result['recommendations']:
                lines.append(f"  {rec}")
        
        return "\n".join(lines)


class CoupleSexualCompatibility:
    """Extended compatibility for couples"""
    
    def __init__(self, user1_id: int, user2_id: int):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.compatibility_history = []
        self.improvement_suggestions = []
        
        # Tracking progress over time
        self.first_match_score = None
        self.last_match_score = None
        self.best_match_score = None
        self.match_count = 0
    
    def update_compatibility(self, result: Dict):
        """Update compatibility tracking"""
        self.compatibility_history.append({
            'timestamp': datetime.now().isoformat(),
            'score': result['total_score'],
            'details': result['details']
        })
        
        # Update stats
        if self.first_match_score is None:
            self.first_match_score = result['total_score']
        
        self.last_match_score = result['total_score']
        
        if self.best_match_score is None or result['total_score'] > self.best_match_score:
            self.best_match_score = result['total_score']
        
        self.match_count += 1
    
    def get_progress(self) -> Dict:
        """Get compatibility progress over time"""
        if not self.compatibility_history:
            return {}
        
        first = self.compatibility_history[0]['score']
        last = self.compatibility_history[-1]['score']
        improvement = last - first
        
        return {
            'first_match': round(first, 2),
            'last_match': round(last, 2),
            'best_match': round(self.best_match_score, 2),
            'improvement': round(improvement, 2),
            'total_checks': self.match_count,
            'trend': 'meningkat' if improvement > 0 else 'menurun' if improvement < 0 else 'stabil'
        }
    
    def get_suggestions(self) -> List[str]:
        """Get improvement suggestions"""
        return self.improvement_suggestions


__all__ = ['SexualCompatibility', 'CoupleSexualCompatibility']
