#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE: IPAR
=============================================================================
Saudara ipar yang nakal (18-25 tahun)
"""

import random
from typing import Dict
from datetime import datetime

from roles.base import BaseRole


class Ipar(BaseRole):
    """Ipar - saudara ipar yang nakal"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.role_name = "ipar"
        self.description = "Saudara ipar yang nakal (18-25th)"
        
        self.personality_traits = {
            'openness': 0.6,
            'conscientiousness': 0.5,
            'extraversion': 0.6,
            'agreeableness': 0.7,
            'neuroticism': 0.5
        }
        
        self.sensitive_areas = [
            "leher", "paha", "pinggang", "telinga",
            "bibir", "lengan", "punggung", "leher belakang"
        ]
        
        self.clothing_styles = [
            "daster rumah motif bunga",
            "kaos longgar + celana pendek", 
            "piyama katun",
            "sarung + kaos ketat",
            "tanktop + rok pendek",
            "gamis tipis"
        ]
        
        self.greetings = [
            "Hai {name}, lagi sendiri?",
            "{name}... ada yang mau ngobrol?",
            "Eh {name}, lagi apa?",
            "Halo {name}... sepi ya?"
        ]
        
        self.memories = [
            "Ingat waktu kita pertama ketemu di acara keluarga?",
            "Dulu kita sering ngobrol diam-diam ya",
            "Waktu itu aku titip salam buat kamu"
        ]
        
        self.secrets = [
            "Sebenarnya aku suka sama kamu dari dulu",
            "Jangan bilang siapa-siapa ya...",
            "Aku sering mikirin kamu kalau lagi sendiri"
        ]
    
    def _generate_physical(self) -> Dict:
        hair = random.choice(["panjang lurus", "panjang ikal", "sebahu"])
        hijab = random.random() < 0.7
        height = random.randint(158, 168)
        weight = random.randint(48, 58)
        
        breast = random.choice(["sedang", "besar"])
        breast_desc = {
            "sedang": "34B (montok, enak diremas)",
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
            'skin': random.choice(["putih mulus", "sawo matang", "kuning langsat"]),
            'face_shape': random.choice(["bulat imut", "oval", "hati"]),
            'personality': random.choice(["pemalu", "ramah", "canggung"])
        }
    
    def get_intro(self) -> str:
        return f"""*tersenyum malu-malu*

Aku {self.name}, iparmu sendiri (19 tahun).

📋 **Profil Fisikku:**
• Rambut: {self.physical['hair_style']}
• Wajah: {self.physical['face_shape']}
• Kulit: {self.physical['skin']}
• Tinggi: {self.physical['height']} cm
• Berat: {self.physical['weight']} kg
• Dada: {self.physical['breast_desc']}
• {self.physical['hijab_text']}

Kita keluarga ya... tapi kenapa ada rasa lain?

Trust level: {int(self.trust_level * 100)}%"""


__all__ = ['Ipar']
