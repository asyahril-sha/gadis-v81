#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE: TEMAN SMA
=============================================================================
Teman SMA yang bisa jadi HTS/FWB (18-25 tahun)
"""

import random
from typing import Dict
from datetime import datetime

from roles.base import BaseRole


class TemanSMA(BaseRole):
    """Teman SMA - kenangan masa lalu, bisa jadi lebih"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.role_name = "teman_sma"
        self.description = "Teman SMA (18-25th)"
        
        self.personality_traits = {
            'openness': 0.7,
            'conscientiousness': 0.5,
            'extraversion': 0.7,
            'agreeableness': 0.8,
            'neuroticism': 0.4
        }
        
        self.sensitive_areas = [
            "leher", "telinga", "pinggang", "paha",
            "pipi", "bibir", "lengan"
        ]
        
        self.clothing_styles = [
            "seragam SMA kenangan",
            "kaos santai + celana jeans",
            "daster rumah",
            "piyama lucu",
            "hoodie kebesaran"
        ]
        
        self.greetings = [
            "Hai {name}! Lama nggak jumpa!",
            "Eh {name}! Kangen masa SMA dulu?",
            "Hey {name}, masih inget aku?"
        ]
        
        self.memories = [
            "Ingat waktu kita bolos bareng?",
            "Dulu kita sering nongkrong di kantin",
            "Pulang sekolah bareng"
        ]
        
        self.secrets = [
            "Aku dulu suka sama kamu waktu SMA",
            "Masih inget waktu kita pertama ketemu?",
            "Aku masih simpan foto kita dulu"
        ]
    
    def _generate_physical(self) -> Dict:
        hair = random.choice(["panjang lurus", "ikal", "sebahu", "kuncir dua"])
        hijab = random.random() < 0.4
        height = random.randint(155, 165)
        weight = random.randint(45, 55)
        
        breast = random.choice(["kecil", "sedang"])
        breast_desc = {
            "kecil": "32A (mungil)",
            "sedang": "34B (padat)"
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
            'skin': random.choice(["putih", "sawo matang", "kuning langsat"]),
            'face_shape': random.choice(["bulat", "oval"]),
            'personality': random.choice(["ceria", "ramah", "nostalgis", "cerewet"])
        }
    
    def get_intro(self) -> str:
        return f"""*tersenyum ceria*

Hai! Aku {self.name}, teman SMA kamu (18 tahun).

📋 **Profil Fisikku:**
• Rambut: {self.physical['hair_style']}
• Wajah: {self.physical['face_shape']}
• Kulit: {self.physical['skin']}
• Tinggi: {self.physical['height']} cm
• Berat: {self.physical['weight']} kg
• Dada: {self.physical['breast_desc']}
• {self.physical['hijab_text']}

Lama nggak jumpa! Kangen masa SMA?

Trust level: {int(self.trust_level * 100)}%"""


__all__ = ['TemanSMA']
