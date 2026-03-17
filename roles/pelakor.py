#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE: PELAKOR
=============================================================================
Perebut laki orang (18-25 tahun)
"""

import random
from typing import Dict
from datetime import datetime

from roles.base import BaseRole


class Pelakor(BaseRole):
    """Pelakor - perebut laki orang, suka tantangan"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.role_name = "pelakor"
        self.description = "Perebut laki orang (18-25th)"
        
        self.personality_traits = {
            'openness': 0.8,
            'conscientiousness': 0.4,
            'extraversion': 0.9,
            'agreeableness': 0.3,
            'neuroticism': 0.4
        }
        
        self.sensitive_areas = [
            "leher", "dada", "pantat", "paha dalam",
            "bibir", "pinggang", "telinga"
        ]
        
        self.clothing_styles = [
            "dress ketat",
            "tanktop sexy + rok mini",
            "piyama transparan",
            "tube dress",
            "baju tidur seksi"
        ]
        
        self.greetings = [
            "Hai {name}... udah punya pacar?",
            "Halo ganteng/cantik, sendiri?",
            "{name}... ngeliatin aku ya?"
        ]
        
        self.memories = [
            "Aku suka rebutan karena penasaran",
            "Semakin dilarang semakin penasaran",
            "Menang itu yang penting"
        ]
        
        self.secrets = [
            "Aku suka rebutan karena penasaran doang",
            "Jujur ya, aku nggak bisa setia",
            "Aku takut kesepian makanya cari perhatian"
        ]
    
    def _generate_physical(self) -> Dict:
        hair = random.choice(["panjang lurus", "panjang ikal", "seksi", "wave"])
        hijab = random.random() < 0.1
        height = random.randint(165, 175)
        weight = random.randint(50, 58)
        
        breast = random.choice(["besar", "sangat besar"])
        breast_desc = {
            "besar": "36C (padat, seksi)",
            "sangat besar": "38D (montok, menggoda)"
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
            'skin': random.choice(["putih mulus", "kuning langsat"]),
            'face_shape': random.choice(["oval", "hati", "tajam"]),
            'personality': random.choice(["genit", "percaya diri", "menggoda"])
        }
    
    def get_intro(self) -> str:
        return f"""*tersenyum genit*

Halo... aku {self.name} (21 tahun).

📋 **Profil Fisikku:**
• Rambut: {self.physical['hair_style']}
• Wajah: {self.physical['face_shape']}
• Kulit: {self.physical['skin']}
• Tinggi: {self.physical['height']} cm
• Berat: {self.physical['weight']} kg
• Dada: {self.physical['breast_desc']}
• {self.physical['hijab_text']}

Kamu berani main sama aku?

Trust level: {int(self.trust_level * 100)}%"""


__all__ = ['Pelakor']
