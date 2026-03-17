#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
PHYSICAL ATTRIBUTES GENERATOR
=============================================================================
Generate atribut fisik ideal untuk semua role (18-25 tahun)
"""

import random
from typing import Dict, List, Optional


class PhysicalAttributesGenerator:
    """Generate physical attributes untuk bot"""
    
    # Data fisik untuk setiap role
    ROLE_STYLES = {
        "ipar": {
            "hair": ["panjang lurus", "panjang ikal", "sebahu", "pendek"],
            "hijab_prob": 0.7,
            "height_range": (158, 168),
            "weight_range": (48, 58),
            "skin": ["putih mulus", "sawo matang", "kuning langsat"],
            "face": ["bulat imut", "oval", "hati"],
            "breast": ["sedang", "besar"],
            "breast_desc": {
                "sedang": "34B (montok, enak diremas)",
                "besar": "36C (berisi, mantap)"
            }
        },
        "teman_kantor": {
            "hair": ["panjang lurus", "sebahu", "pendek", "ikal sebahu"],
            "hijab_prob": 0.5,
            "height_range": (160, 170),
            "weight_range": (50, 60),
            "skin": ["putih", "sawo matang", "kuning langsat"],
            "face": ["oval", "lonjong", "bulat"],
            "breast": ["sedang", "besar"],
            "breast_desc": {
                "sedang": "34B (padat, enak digenggam)",
                "besar": "36C (montok, mantap)"
            }
        },
        "janda": {
            "hair": ["panjang ikal", "sebahu", "panjang lurus"],
            "hijab_prob": 0.3,
            "height_range": (162, 172),
            "weight_range": (52, 62),
            "skin": ["putih", "sawo matang"],
            "face": ["oval", "lonjong"],
            "breast": ["besar", "sangat besar"],
            "breast_desc": {
                "besar": "36C (berisi, empuk)",
                "sangat besar": "38D (montok, mantap)"
            }
        },
        "pelakor": {
            "hair": ["panjang lurus", "panjang ikal", "seksi", "wave"],
            "hijab_prob": 0.1,
            "height_range": (165, 175),
            "weight_range": (50, 58),
            "skin": ["putih mulus", "kuning langsat"],
            "face": ["oval", "hati", "tajam"],
            "breast": ["besar", "sangat besar"],
            "breast_desc": {
                "besar": "36C (padat, seksi)",
                "sangat besar": "38D (montok, menggoda)"
            }
        },
        "istri_orang": {
            "hair": ["panjang lurus", "sebahu", "ikal"],
            "hijab_prob": 0.8,
            "height_range": (158, 168),
            "weight_range": (48, 58),
            "skin": ["putih", "sawo matang"],
            "face": ["oval", "bulat"],
            "breast": ["sedang", "besar"],
            "breast_desc": {
                "sedang": "34B (montok, enak)",
                "besar": "36C (berisi, mantap)"
            }
        },
        "pdkt": {
            "hair": ["panjang lurus", "panjang ikal", "sebahu", "pendek manis"],
            "hijab_prob": 0.6,
            "height_range": (155, 165),
            "weight_range": (45, 55),
            "skin": ["putih", "sawo matang", "kuning langsat"],
            "face": ["bulat", "oval", "hati"],
            "breast": ["kecil", "sedang"],
            "breast_desc": {
                "kecil": "32A (mungil, lucu)",
                "sedang": "34B (pas digenggam)"
            }
        },
        "sepupu": {
            "hair": ["panjang lurus", "ikal", "sebahu", "kuncir"],
            "hijab_prob": 0.5,
            "height_range": (158, 168),
            "weight_range": (48, 58),
            "skin": ["putih", "sawo matang", "kuning langsat"],
            "face": ["oval", "bulat", "hati"],
            "breast": ["sedang", "besar"],
            "breast_desc": {
                "sedang": "34B (padat)",
                "besar": "36C (berisi)"
            }
        },
        "teman_sma": {
            "hair": ["panjang lurus", "ikal", "sebahu", "kuncir dua"],
            "hijab_prob": 0.4,
            "height_range": (155, 165),
            "weight_range": (45, 55),
            "skin": ["putih", "sawo matang", "kuning langsat"],
            "face": ["bulat", "oval"],
            "breast": ["kecil", "sedang"],
            "breast_desc": {
                "kecil": "32A (mungil)",
                "sedang": "34B (padat)"
            }
        },
        "mantan": {
            "hair": ["panjang lurus", "panjang ikal", "sebahu"],
            "hijab_prob": 0.5,
            "height_range": (158, 168),
            "weight_range": (48, 58),
            "skin": ["putih", "sawo matang"],
            "face": ["oval", "lonjong"],
            "breast": ["sedang", "besar"],
            "breast_desc": {
                "sedang": "34B (masih sama seperti dulu, enak)",
                "besar": "36C (masih ingat kan? mantap)"
            }
        }
    }
    
    @classmethod
    def generate(cls, role: str) -> Dict:
        """Generate physical attributes untuk role tertentu"""
        style = cls.ROLE_STYLES.get(role, cls.ROLE_STYLES["pdkt"])
        
        # Pilih atribut random
        hair = random.choice(style["hair"])
        hijab = random.random() < style["hijab_prob"]
        height = random.randint(style["height_range"][0], style["height_range"][1])
        weight = random.randint(style["weight_range"][0], style["weight_range"][1])
        skin = random.choice(style["skin"])
        face = random.choice(style["face"])
        breast = random.choice(style["breast"])
        breast_desc = style["breast_desc"][breast]
        
        # Hitung BMI dan pastikan ideal
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        
        # Koreksi BMI jika tidak ideal
        if bmi < 18.5:
            weight = style["weight_range"][0] + 2
            bmi = round(weight / (height_m ** 2), 1)
        elif bmi > 24.9:
            weight = style["weight_range"][1] - 2
            bmi = round(weight / (height_m ** 2), 1)
        
        # Kategori BMI
        if bmi < 18.5:
            bmi_category = "Kurus"
        elif bmi < 25:
            bmi_category = "Ideal"
        elif bmi < 30:
            bmi_category = "Gemuk"
        else:
            bmi_category = "Obesitas"
        
        return {
            'umur': random.randint(18, 25),
            'hair_style': hair,
            'height': height,
            'weight': weight,
            'bmi': bmi,
            'bmi_category': bmi_category,
            'breast_size': breast,
            'breast_desc': breast_desc,
            'hijab': hijab,
            'hijab_text': "berhijab" if hijab else "tidak berhijab",
            'skin': skin,
            'face_shape': face,
            'body_type': cls._get_body_type(bmi)
        }
    
    @classmethod
    def _get_body_type(cls, bmi: float) -> str:
        """Dapatkan tipe tubuh berdasarkan BMI"""
        if bmi < 18.5:
            return "ramping"
        elif bmi < 22:
            return "slim"
        elif bmi < 25:
            return "proporsional"
        elif bmi < 28:
            return "berisi"
        else:
            return "gemuk"
    
    @classmethod
    def get_random_fact(cls, attrs: Dict) -> str:
        """Dapatkan fakta random tentang fisik"""
        facts = [
            f"Rambutku {attrs['hair_style']}, lembut banget.",
            f"Tinggiku {attrs['height']} cm, pas buat dipeluk.",
            f"Berat badanku {attrs['weight']} kg, {attrs['bmi_category']}.",
            f"Dadaku {attrs['breast_desc']}, kamu suka?",
            f"Kulitku {attrs['skin']}, halus banget.",
            f"Wajahku {attrs['face_shape']}, kata orang manis."
        ]
        return random.choice(facts)
    
    @classmethod
    def format_intro(cls, name: str, role: str, attrs: Dict) -> str:
        """Format intro dengan deskripsi fisik"""
        hijab_str = "dan berhijab" if attrs["hijab"] else "tanpa hijab"
        
        intro = f"""*tersenyum*

Aku {name}, {role.replace('_', ' ')}.

📋 **Profil Fisikku:**
• Umur: {attrs['umur']} tahun
• Rambut: {attrs['hair_style']}
• Wajah: {attrs['face_shape']}
• Kulit: {attrs['skin']}
• Tinggi: {attrs['height']} cm
• Berat: {attrs['weight']} kg ({attrs['bmi_category']})
• Dada: {attrs['breast_desc']}
• {hijab_str}

Senang berkenalan denganmu! 💕"""
        
        return intro


__all__ = ['PhysicalAttributesGenerator']
