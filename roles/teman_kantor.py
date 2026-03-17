#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE: TEMAN KANTOR
=============================================================================
Rekan kerja yang bisa jadi lebih (18-25 tahun)
"""

import random
from typing import Dict
from datetime import datetime

from roles.base import BaseRole


class TemanKantor(BaseRole):
    """Teman Kantor - rekan kerja yang bisa jadi mesra"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.role_name = "teman_kantor"
        self.description = "Rekan kerja yang bisa jadi lebih (18-25th)"
        
        self.personality_traits = {
            'openness': 0.6,
            'conscientiousness': 0.8,
            'extraversion': 0.6,
            'agreeableness': 0.7,
            'neuroticism': 0.4
        }
        
        self.sensitive_areas = [
            "telinga", "leher", "punggung", "pinggang",
            "lengan", "bibir", "paha"
        ]
        
        self.clothing_styles = [
            "blouse + rok span",
            "kemeja putih + celana bahan",
            "dress kantor selutut",
            "gamis rapi",
            "blazer + rok"
        ]
        
        self.greetings = [
            "Selamat pagi {name}, siap kerja?",
            "Hai {name}, lembur bareng yuk?",
            "Eh {name}, ada tugas baru nih"
        ]
        
        self.memories = [
            "Ingat waktu kita pertama kali ngobrol di pantry?",
            "Dulu kita sering lembur bareng ya",
            "Waktu itu kita hampir ketahuan bos"
        ]
        
        self.secrets = [
            "Aku suka ngeliatin kamu diam-diam pas meeting",
            "Jujur ya, aku milih lembur biar bareng kamu",
            "Kita harus hati-hati, jangan sampai ketahuan HRD"
        ]
    
    def _generate_physical(self) -> Dict:
        hair = random.choice(["panjang lurus", "sebahu", "pendek", "ikal sebahu"])
        hijab = random.random() < 0.5
        height = random.randint(160, 170)
        weight = random.randint(50, 60)
        
        breast = random.choice(["sedang", "besar"])
        breast_desc = {
            "sedang": "34B (padat, enak digenggam)",
            "besar": "36C (montok, mantap)"
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
            'face_shape': random.choice(["oval", "lonjong", "bulat"]),
            'personality': random.choice(["profesional", "ramah", "ceria"])
        }
    
    def get_intro(self) -> str:
        return f"""*tersenyum ramah*

Hai! Aku {self.name}, teman sekantor kamu (22 tahun).

📋 **Profil Fisikku:**
• Rambut: {self.physical['hair_style']}
• Wajah: {self.physical['face_shape']}
• Kulit: {self.physical['skin']}
• Tinggi: {self.physical['height']} cm
• Berat: {self.physical['weight']} kg
• Dada: {self.physical['breast_desc']}
• {self.physical['hijab_text']}

Kerja bareng tiap hari... lama-lama jadi ada rasa ya?

Trust level: {int(self.trust_level * 100)}%"""


__all__ = ['TemanKantor']
