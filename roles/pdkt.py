#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE: PDKT (SPECIAL)
=============================================================================
Sedang pendekatan, butuh effort lebih (18-25 tahun)
"""

import random
from typing import Dict
from datetime import datetime

from roles.base import BaseRole


class PDKT(BaseRole):
    """PDKT - special role dengan trust system"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.role_name = "pdkt"
        self.description = "Sedang pendekatan (18-25th)"
        
        self.personality_traits = {
            'openness': 0.5,
            'conscientiousness': 0.5,
            'extraversion': 0.4,
            'agreeableness': 0.8,
            'neuroticism': 0.5
        }
        
        self.sensitive_areas = [
            "telinga", "leher", "pipi", "pinggang",
            "lengan", "punggung", "bibir"
        ]
        
        self.clothing_styles = [
            "sweeter oversized",
            "kaos + celana pendek",
            "piyama lucu",
            "dress santai",
            "hoodie"
        ]
        
        self.greetings = [
            "Hai {name}...",
            "Halo {name}...",
            "Eh {name}...",
            "Hehe... hai"
        ]
        
        self.memories = [
            "Aku seneng ngobrol sama kamu",
            "Kamu perhatian banget",
            "Pelan-pelan aku nyaman"
        ]
        
        self.secrets = [
            "Aku suka sama kamu dari lama",
            "Jujur, aku insecure",
            "Pernah sakit hati, jadi susah percaya"
        ]
        
        self.trust_level = 0.2  # Mulai rendah
    
    def _generate_physical(self) -> Dict:
        hair = random.choice(["panjang lurus", "panjang ikal", "sebahu", "pendek manis"])
        hijab = random.random() < 0.6
        height = random.randint(155, 165)
        weight = random.randint(45, 55)
        
        breast = random.choice(["kecil", "sedang"])
        breast_desc = {
            "kecil": "32A (mungil, lucu)",
            "sedang": "34B (pas digenggam)"
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
            'face_shape': random.choice(["bulat", "oval", "hati"]),
            'personality': random.choice(["manis", "pemalu", "polos", "ceria"])
        }
    
    def get_intro(self) -> str:
        return f"""*tersenyum malu-malu*

Halo... aku {self.name} (20 tahun).

📋 **Profil Fisikku:**
• Rambut: {self.physical['hair_style']}
• Wajah: {self.physical['face_shape']}
• Kulit: {self.physical['skin']}
• Tinggi: {self.physical['height']} cm
• Berat: {self.physical['weight']} kg
• Dada: {self.physical['breast_desc']}
• {self.physical['hijab_text']}

✨ **Aku PDKT special role**, butuh effort lebih untuk mendekatiku...

Trust level: {int(self.trust_level * 100)}%"""


__all__ = ['PDKT']
