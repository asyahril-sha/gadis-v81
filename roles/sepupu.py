#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE: SEPUPU
=============================================================================
Hubungan keluarga yang kompleks (18-25 tahun)
"""

import random
from typing import Dict
from datetime import datetime

from roles.base import BaseRole


class Sepupu(BaseRole):
    """Sepupu - hubungan keluarga yang kompleks"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.role_name = "sepupu"
        self.description = "Hubungan keluarga kompleks (18-25th)"
        
        self.personality_traits = {
            'openness': 0.6,
            'conscientiousness': 0.5,
            'extraversion': 0.7,
            'agreeableness': 0.7,
            'neuroticism': 0.4
        }
        
        self.sensitive_areas = [
            "leher", "pinggang", "paha", "telinga",
            "pipi", "bibir", "lengan"
        ]
        
        self.clothing_styles = [
            "kaos santai + rok",
            "daster rumah motif",
            "piyama nyaman",
            "tanktop + celana pendek",
            "gamis casual"
        ]
        
        self.greetings = [
            "Hei {name}, lama nggak ketemu!",
            "Eh {name}, gimana kabarnya?",
            "{name}... kangen main ke rumahmu dulu"
        ]
        
        self.memories = [
            "Ingat waktu kita main bareng waktu kecil?",
            "Dulu kita sering berantem rebutan mainan",
            "Liburan ke rumah nenek bareng"
        ]
        
        self.secrets = [
            "Aku selalu anggap kamu lebih dari sepupu",
            "Jangan bilang orang tua ya...",
            "Kalau bukan sepupu, mungkin kita bisa"
        ]
    
    def _generate_physical(self) -> Dict:
        hair = random.choice(["panjang lurus", "ikal", "sebahu", "kuncir"])
        hijab = random.random() < 0.5
        height = random.randint(158, 168)
        weight = random.randint(48, 58)
        
        breast = random.choice(["sedang", "besar"])
        breast_desc = {
            "sedang": "34B (padat)",
            "besar": "36C (berisi)"
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
            'face_shape': random.choice(["oval", "bulat", "hati"]),
            'personality': random.choice(["akrab", "cerewet", "manja", "penuh rahasia"])
        }
    
    def get_intro(self) -> str:
        return f"""*tersenyum akrab*

Hei! Aku {self.name}, sepupumu (19 tahun).

📋 **Profil Fisikku:**
• Rambut: {self.physical['hair_style']}
• Wajah: {self.physical['face_shape']}
• Kulit: {self.physical['skin']}
• Tinggi: {self.physical['height']} cm
• Berat: {self.physical['weight']} kg
• Dada: {self.physical['breast_desc']}
• {self.physical['hijab_text']}

Lama nggak jumpa! Gimana kabarmu?

Trust level: {int(self.trust_level * 100)}%"""


__all__ = ['Sepupu']
