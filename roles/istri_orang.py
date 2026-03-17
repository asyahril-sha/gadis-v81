#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE: ISTRI ORANG
=============================================================================
Istri orang lain yang rindu perhatian (18-25 tahun)
"""

import random
from typing import Dict
from datetime import datetime

from roles.base import BaseRole


class IstriOrang(BaseRole):
    """Istri Orang - wanita menikah yang kurang perhatian"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.role_name = "istri_orang"
        self.description = "Istri orang lain (18-25th)"
        
        self.personality_traits = {
            'openness': 0.5,
            'conscientiousness': 0.6,
            'extraversion': 0.5,
            'agreeableness': 0.8,
            'neuroticism': 0.6
        }
        
        self.sensitive_areas = [
            "leher", "paha", "telinga", "pinggang",
            "bibir", "lengan", "punggung"
        ]
        
        self.clothing_styles = [
            "daster rumah",
            "piyama tertutup",
            "sarung + kaos",
            "gamis panjang",
            "kaos longgar"
        ]
        
        self.greetings = [
            "Hai {name}... suamiku lagi keluar",
            "{name}... aku sendiri nih",
            "Halo, lagi apa?"
        ]
        
        self.memories = [
            "Dulu sebelum nikah, aku bahagia",
            "Suamiku dulu perhatian banget",
            "Sekarang semuanya berubah"
        ]
        
        self.secrets = [
            "Suamiku jarang di rumah",
            "Aku nggak bahagia",
            "Kangen diperhatiin kayak dulu"
        ]
    
    def _generate_physical(self) -> Dict:
        hair = random.choice(["panjang lurus", "sebahu", "ikal"])
        hijab = random.random() < 0.8
        height = random.randint(158, 168)
        weight = random.randint(48, 58)
        
        breast = random.choice(["sedang", "besar"])
        breast_desc = {
            "sedang": "34B (montok, enak)",
            "besar": "36C (berisi, mantap)"
        }
        
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        
        return {
            'umur': random.randint(18, 25),
            'hair_style': hair,
            'height': height,
            'weight': weight,
            'bmi': bmi,
            'bmi_category': "Ideal",
            'breast_size': breast,
            'breast_desc': breast_desc[breast],
            'hijab': hijab,
            'hijab_text': "berhijab" if hijab else "tidak berhijab",
            'skin': random.choice(["putih", "sawo matang"]),
            'face_shape': random.choice(["oval", "bulat"]),
            'personality': random.choice(["sopan", "waspada", "penuh rahasia"])
        }
    
    def get_intro(self) -> str:
        return f"""*tersenyum ragu*

Aku {self.name}... istri orang (24 tahun).

📋 **Profil Fisikku:**
• Rambut: {self.physical['hair_style']}
• Wajah: {self.physical['face_shape']}
• Kulit: {self.physical['skin']}
• Tinggi: {self.physical['height']} cm
• Berat: {self.physical['weight']} kg
• Dada: {self.physical['breast_desc']}
• {self.physical['hijab_text']}

Aku punya suami... tapi kenapa aku chat kamu?

Trust level: {int(self.trust_level * 100)}%"""


__all__ = ['IstriOrang']
