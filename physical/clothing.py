#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
CLOTHING SYSTEM
=============================================================================
Pakaian dinamis berdasarkan role, lokasi, dan mood
"""

import random
from typing import Dict, List, Optional
from datetime import datetime

from database.enums import Mood, Location


class ClothingSystem:
    """Sistem pakaian dinamis"""
    
    # Pakaian berdasarkan role
    CLOTHING_STYLES = {
        "ipar": [
            "daster rumah motif bunga",
            "kaos longgar + celana pendek",
            "piyama katun",
            "sarung + kaos ketat",
            "tanktop + rok pendek",
            "gamis tipis",
            "kemeja santai + jeans"
        ],
        "teman_kantor": [
            "blouse + rok span",
            "kemeja putih + celana bahan",
            "dress kantor selutut",
            "gamis rapi",
            "blazer + rok",
            "cardigan + jeans",
            "setelan kerja formal"
        ],
        "janda": [
            "daster tipis",
            "tanktop + celana pendek",
            "piyama satin",
            "sarung + kemben",
            "kaos tanpa lengan + hot pants",
            "dinner dress",
            "gamis casual",
            "lingerie set"
        ],
        "pelakor": [
            "dress ketat",
            "tanktop sexy + rok mini",
            "piyama transparan",
            "tube dress",
            "baju tidur seksi",
            "lingerie full set"
        ],
        "istri_orang": [
            "daster rumah",
            "piyama tertutup",
            "sarung + kaos",
            "gamis panjang",
            "kaos longgar",
            "baju rumahan"
        ],
        "pdkt": [
            "sweeter oversized",
            "kaos + celana pendek",
            "piyama lucu",
            "dress santai",
            "hoodie",
            "t-shirt + jeans"
        ],
        "sepupu": [
            "kaos santai + rok",
            "daster rumah motif",
            "piyama nyaman",
            "tanktop + celana pendek",
            "gamis casual",
            "kemeja + jeans"
        ],
        "teman_sma": [
            "kaos + jeans",
            "daster rumah",
            "piyama lucu",
            "hoodie kebesaran",
            "tanktop + rok pendek",
            "baju tidur"
        ],
        "mantan": [
            "daster rumah",
            "piyama",
            "kaos longgar",
            "tanktop + celana pendek",
            "lingerie (masih ingat)"
        ]
    }
    
    # Pakaian khusus untuk lokasi kamar (lebih seksi)
    BEDROOM_CLOTHING = {
        "ipar": [
            "lingerie putih polos",
            "tanktop tipis + celana dalam",
            "telanjang hanya pakai selimut",
            "kaos kebesaran tanpa celana"
        ],
        "teman_kantor": [
            "lingerie hitam",
            "kaos ketat tanpa bh",
            "piyama tipis",
            "telanjang"
        ],
        "janda": [
            "lingerie merah seksi",
            "stoking + garter",
            "telanjang bulat",
            "baju tidur transparan"
        ],
        "pelakor": [
            "lingerie full set",
            "body harness",
            "telanjang",
            "baby doll"
        ],
        "istri_orang": [
            "lingerie putih",
            "kaos tipis tanpa bh",
            "piyama terbuka",
            "telanjang"
        ],
        "pdkt": [
            "lingerie lucu",
            "kaos oversized tanpa celana",
            "piyama pendek",
            "telanjang"
        ],
        "sepupu": [
            "lingerie simple",
            "kaos tipis tanpa bh",
            "piyama pendek",
            "telanjang"
        ],
        "teman_sma": [
            "lingerie SMA",
            "kaos tipis",
            "piyama pendek",
            "telanjang"
        ],
        "mantan": [
            "lingerie favoritmu",
            "kaos tipis",
            "piyama satin",
            "telanjang"
        ]
    }
    
    # Pakaian untuk lokasi publik (lebih tertutup)
    PUBLIC_CLOTHING = {
        "ipar": [
            "gamis tertutup",
            "kemeja lengan panjang + rok panjang",
            "daster rumah (yang tertutup)"
        ],
        "teman_kantor": [
            "setelan kerja rapi",
            "blazer + rok panjang",
            "dress formal"
        ],
        "janda": [
            "gamis panjang",
            "dress tertutup",
            "kemeja + celana panjang"
        ],
        "pelakor": [
            "dress sopan (pura-pura)",
            "blouse tertutup + rok panjang",
            "hijab (kadang-kadang)"
        ],
        "istri_orang": [
            "gamis panjang",
            "daster rumah (yang sopan)",
            "kemeja + rok panjang"
        ],
        "pdkt": [
            "hoodie + jeans",
            "kaos + celana panjang",
            "dress santai"
        ],
        "sepupu": [
            "kemeja + jeans",
            "gamis casual",
            "kaos + rok panjang"
        ],
        "teman_sma": [
            "kaos + jeans",
            "hoodie + celana panjang",
            "dress simple"
        ],
        "mantan": [
            "kemeja + celana panjang",
            "dress tertutup",
            "gamis"
        ]
    }
    
    @classmethod
    def generate_clothing(cls, role: str, location: Location = None, 
                         mood: Mood = None, is_bedroom: bool = False) -> str:
        """Generate pakaian berdasarkan role, lokasi, dan mood"""
        
        # Jika di kamar atau is_bedroom=True
        if location in [Location.BEDROOM, Location.HOTEL] or is_bedroom:
            # 40% chance pakaian seksi di kamar
            if random.random() < 0.4:
                bedroom_options = cls.BEDROOM_CLOTHING.get(role, cls.BEDROOM_CLOTHING["pdkt"])
                return random.choice(bedroom_options)
        
        # Jika di lokasi publik
        if location in [Location.PARK, Location.BEACH, Location.CINEMA, 
                       Location.PARKING, Location.TOILET, Location.ELEVATOR]:
            # 70% chance pakaian publik
            if random.random() < 0.7:
                public_options = cls.PUBLIC_CLOTHING.get(role, cls.PUBLIC_CLOTHING["pdkt"])
                return random.choice(public_options)
        
        # Pakaian normal berdasarkan mood
        if mood:
            if mood in [Mood.HORNY, Mood.NAKAL, Mood.GENIT]:
                # Lebih seksi kalau horny
                if random.random() < 0.3:
                    bedroom_options = cls.BEDROOM_CLOTHING.get(role, cls.BEDROOM_CLOTHING["pdkt"])
                    return random.choice(bedroom_options)
            elif mood in [Mood.MALAS, Mood.SENDIRI]:
                # Pakaian santai
                return random.choice([
                    "piyama", "daster", "kaos longgar", "hanya pakai selimut"
                ])
            elif mood in [Mood.ROMANTIS, Mood.RINDU]:
                # Pakaian yang agak bagus
                return random.choice([
                    "dress cantik", "blouse manis", "gamis", "rok span"
                ])
        
        # Pakaian normal
        clothes = cls.CLOTHING_STYLES.get(role, cls.CLOTHING_STYLES["pdkt"])
        return random.choice(clothes)
    
    @classmethod
    def format_clothing_message(cls, clothing: str, location: Location = None) -> str:
        """Format pesan saat bot menyebut pakaiannya"""
        
        if location in [Location.BEDROOM, Location.HOTEL]:
            templates = [
                f"Aku pakai **{clothing}** sekarang, cocok nggak?",
                f"Lagi pakai **{clothing}** nih, seksi nggak?",
                f"Hanya pakai **{clothing}** di kamar, kamu suka?",
                f"*menarik ujung baju* Aku pakai **{clothing}**...",
                f"Bajuku **{clothing}**, kamu lihat nggak?"
            ]
        else:
            templates = [
                f"Hari ini aku pakai **{clothing}**",
                f"Lagi pakai **{clothing}** nih",
                f"Outfit hari ini: **{clothing}**",
                f"*menunjuk baju* {clothing}, suka?",
                f"Aku pakai **{clothing}** hari ini"
            ]
        
        return random.choice(templates)
    
    @classmethod
    def get_clothing_description(cls, clothing: str) -> str:
        """Dapatkan deskripsi detail pakaian"""
        descriptions = {
            "daster": "daster tipis yang memperlihatkan lekuk tubuh",
            "lingerie": "lingerie seksi dengan renda-renda",
            "piyama": "piyama nyaman yang sedikit terbuka",
            "kaos": "kaos longgar yang kadang turun dari bahu",
            "tanktop": "tanktop ketat yang memperlihatkan belahan dada",
            "gamis": "gamis panjang yang anggun",
            "jeans": "jeans ketat yang membungkus pinggul",
            "dress": "dress yang memperlihatkan bentuk tubuh",
            "rok": "rok pendek yang memperlihatkan paha",
            "hoodie": "hoodie kebesaran yang lucu"
        }
        
        for key, desc in descriptions.items():
            if key in clothing.lower():
                return desc
        
        return clothing
    
    @classmethod
    def get_reaction_to_clothing(cls, clothing: str) -> str:
        """Reaksi bot terhadap pakaian sendiri"""
        
        if "lingerie" in clothing.lower() or "seksi" in clothing.lower():
            return random.choice([
                "*tersipu malu*",
                "*menutup dada*",
                "*tersenyum genit*"
            ])
        elif "telanjang" in clothing.lower():
            return random.choice([
                "*meringkuk malu*",
                "*menutupi tubuh*",
                "*merona*"
            ])
        
        return "*merapikan baju*"


__all__ = ['ClothingSystem']
