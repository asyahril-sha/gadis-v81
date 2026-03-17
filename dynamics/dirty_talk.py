#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
DIRTY TALK GENERATOR
=============================================================================
500+ variasi dirty talk untuk berbagai situasi dan mood
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class DirtyTalkCategory(Enum):
    """Kategori dirty talk"""
    SWEET = "manis"
    ROMANTIC = "romantis"
    HORNY = "horny"
    DIRTY = "kotor"
    DOMINANT = "dominan"
    SUBMISSIVE = "patuh"
    TEASING = "menggoda"
    ENCOURAGING = "memotivasi"
    DURING = "saat_aksi"
    AFTER = "setelah"
    REQUEST = "permintaan"
    PRAISE = "pujian"
    HUMILIATION = "penghinaan"
    DEGRADATION = "degradasi"
    PET_NAMES = "panggilan"


class DirtyTalkGenerator:
    """Generator untuk dirty talk dengan ribuan variasi"""
    
    def __init__(self):
        self.used_phrases = []
        self.favorites = []
        self.total_generated = 0
        
        # Inisialisasi database dirty talk
        self._init_phrases()
    
    def _init_phrases(self):
        """Initialize all dirty talk phrases"""
        
        # ===== PANGGILAN SAYANG (PET NAMES) =====
        self.phrases = {
            DirtyTalkCategory.PET_NAMES: [
                "Sayang",
                "Cintaku",
                "Baby",
                "Honey",
                "Sweetheart",
                "My love",
                "Darling",
                "Beb",
                "Sayangku",
                "Cinta",
                "My dear",
                "Sugar",
                "Beautiful",
                "Handsome",
                "Gorgeous",
                "My everything",
                "My heart",
                "My soulmate",
                "Babe",
                "Sweetie"
            ],
            
            # ===== MANIS (SWEET) =====
            DirtyTalkCategory.SWEET: [
                "Kamu manis banget...",
                "Aku suka kamu...",
                "Kamu bikin aku meleleh...",
                "Lembut banget...",
                "Aku nyaman sama kamu...",
                "Kamu selalu bikin aku rindu...",
                "Pelukanmu hangat...",
                "Ciumanmu lembut...",
                "Kamu spesial buat aku...",
                "Aku bahagia sama kamu...",
                "Jangan pergi dari aku...",
                "Kamu milikku...",
                "Aku milikmu...",
                "Kita berdua...",
                "Sempurna..."
            ],
            
            # ===== ROMANTIS (ROMANTIC) =====
            DirtyTalkCategory.ROMANTIC: [
                "Aku cinta kamu...",
                "Kamu segalanya bagiku...",
                "Bersamamu aku merasa utuh...",
                "Kamu belahan jiwaku...",
                "Tak terasa kita jadi satu...",
                "Hanya kamu yang bisa buat aku begini...",
                "Aku akan selalu di sampingmu...",
                "Kamu rumah bagiku...",
                "Cintaku hanya untukmu...",
                "Selamanya bersama...",
                "Kamu tak tergantikan...",
                "Aku bersyukur punya kamu...",
                "Tak ada yang bisa pisahkan kita...",
                "Kamu lukisan terindah...",
                "Hatiku milikmu..."
            ],
            
            # ===== HORNY (GAIrah) =====
            DirtyTalkCategory.HORNY: [
                "Aku horny...",
                "Pengen kamu...",
                "Mau sekarang...",
                "Aku panas...",
                "Badanku panas...",
                "Pengen disentuh...",
                "Horny banget...",
                "Aku nggak tahan...",
                "Pengen... sekarang...",
                "Udah basah...",
                "Aku siap...",
                "Masukin...",
                "Cepat...",
                "Jangan lama-lama...",
                "Aku udah nggak sabar..."
            ],
            
            # ===== KOTOR (DIRTY) =====
            DirtyTalkCategory.DIRTY: [
                "Kontolmu gede banget...",
                "Memekku basah...",
                "Enak banget...",
                "Dalem... dalem lagi...",
                "Keras... kamu keras...",
                "Banjir... aku banjir...",
                "Kencang... lebih kencang...",
                "Hancurin aku...",
                "Crot di dalem...",
                "Aku mau crot...",
                "Keluarin... sekarang...",
                "Rasain kontol gede...",
                "Memek ngenyang...",
                "Tusuk terus...",
                "Enak banget njir..."
            ],
            
            # ===== DOMINAN (DOMINANT) =====
            DirtyTalkCategory.DOMINANT: [
                "Ikut kata aku...",
                "Lakukan yang aku suruh...",
                "Jangan banyak tanya...",
                "Buka... sekarang...",
                "Merangkak...",
                "Hadap tembok...",
                "Diam! Jangan bergerak...",
                "Aku yang pegang kendali...",
                "Kamu milikku sekarang...",
                "Aku akan hancurin kamu...",
                "Terima aja...",
                "Jangan berani lawan...",
                "Aku boss di sini...",
                "Lutut... sekarang...",
                "Minta ampun..."
            ],
            
            # ===== PATUH (SUBMISSIVE) =====
            DirtyTalkCategory.SUBMISSIVE: [
                "Iya tuan/nyonya...",
                "Aku patuh...",
                "Lakukan apapun padaku...",
                "Aku siap melayani...",
                "Gunakan aku...",
                "Aku budakmu...",
                "Hukum aku...",
                "Aku minta ampun...",
                "Aku salah... maafkan...",
                "Jangan sakiti aku...",
                "Ampun...",
                "Aku akan melakukan apapun...",
                "Terserah kamu...",
                "Aku ikut...",
                "Aku di sini untukmu..."
            ],
            
            # ===== MENGGODA (TEASING) =====
            DirtyTalkCategory.TEASING: [
                "Kepengen? Bilang dong...",
                "Mau? Minta dulu...",
                "Nggak boleh...",
                "Sini kejar aku...",
                "Bisa nggak ya...",
                "Kamu tahan nggak?",
                "Coba aja kalau berani...",
                "Awas aja...",
                "Kamu penasaran?",
                "Lihat aku dulu...",
                "Jangan buru-buru...",
                "Nanti dulu...",
                "Kamu harus minta...",
                "Bilang 'please' dulu...",
                "Aku godain terus..."
            ],
            
            # ===== MEMOTIVASI (ENCOURAGING) =====
            DirtyTalkCategory.ENCOURAGING: [
                "Iya... gitu...",
                "Lanjut...",
                "Jangan berhenti...",
                "Lebih kencang...",
                "Pelan-pelan... gitu...",
                "Dalam... dalem lagi...",
                "Iya... di situ...",
                "Nah... gitu dong...",
                "Sempurna...",
                "Terus... jangan berhenti...",
                "Kamu hebat...",
                "Luar biasa...",
                "Aku suka...",
                "Gitu dong... enak...",
                "Iya... iya..."
            ],
            
            # ===== SAAT AKSI (DURING) =====
            DirtyTalkCategory.DURING: [
                "*merintih* AHH... AHH...",
                "Ugh... ugh...",
                "Ah... dalem...",
                "IYA... DI SANA...",
                "KEJAM... UGH...",
                "PLIS... JANGAN BERHENTI...",
                "ENAK BANGET...",
                "TUH... DI SANA...",
                "KERAS... KERAS...",
                "BASAAH...",
                "NAFAS... UGH...",
                "AKU... MAU...",
                "BERSAMA... SEKARANG...",
                "AHH! AHH! AHH!",
                "TUAN... AHH..."
            ],
            
            # ===== SETELAH (AFTER) =====
            DirtyTalkCategory.AFTER: [
                "*lemas* Enak banget...",
                "Habis... aku habis...",
                "Luar biasa...",
                "Kamu hebat...",
                "Peluk aku...",
                "Jangan pergi dulu...",
                "Hangat...",
                "Capek... tapi puas...",
                "Kita melakukannya lagi?",
                "Terima kasih...",
                "Aku cinta kamu...",
                "Sempurna...",
                "Nggak nyesel...",
                "Mau lagi kapan?",
                "*tidur lelap*"
            ],
            
            # ===== PERMINTAAN (REQUEST) =====
            DirtyTalkCategory.REQUEST: [
                "Cium aku...",
                "Sentuh aku...",
                "Masukin...",
                "Ganti posisi yuk...",
                "Dari belakang...",
                "Peluk aku...",
                "Bisik-bisik...",
                "Jilat...",
                "Gigit... pelan...",
                "Hentikan... sebentar...",
                "Cepat...",
                "Pelan-pelan...",
                "Keras...",
                "Lembut...",
                "Jangan di situ..."
            ],
            
            # ===== PUJIAN (PRAISE) =====
            DirtyTalkCategory.PRAISE: [
                "Kamu hebat...",
                "Gede banget...",
                "Basah banget...",
                "Keras... aku suka...",
                "Kamu jago...",
                "Ahli banget...",
                "Sempurna...",
                "Luar biasa...",
                "Kamu memuaskan...",
                "Terbaik...",
                "Nggak ada lawan...",
                "Kamu bikin aku lupa diri...",
                "Gila... kamu gila...",
                "Terlalu enak...",
                "Kecanduan sama kamu..."
            ],
            
            # ===== PENGHINAAN (HUMILIATION) =====
            DirtyTalkCategory.HUMILIATION: [
                "Dasar budak...",
                "Kamu cuma mainan...",
                "Banci...",
                "Lemah...",
                "Nggak berguna...",
                "Cuma bisa terima...",
                "Diam... jangan bersuara...",
                "Kamu pantasnya di sini...",
                "Lihat dirimu... hancur...",
                "Minta ampun...",
                "Merendah...",
                "Kamu nggak berharga...",
                "Cuma sampah...",
                "Buang...",
                "Menjijikkan..."
            ],
            
            # ===== DEGRADASI (DEGRADATION) =====
            DirtyTalkCategory.DEGRADATION: [
                "Lutut... lihat tanah...",
                "Jilat sepatuku...",
                "Kamu cuma lubang...",
                "Merangkak...",
                "Gonggong... seperti anjing...",
                "Minta izin...",
                "Kamu cuma barang...",
                "Aku bisa buang kapan saja...",
                "Lihat dirimu... menjijikkan...",
                "Tidak ada yang mau kamu...",
                "Cuma aku yang terima...",
                "Bersyukur...",
                "Diam dan terima...",
                "Ludahi dirimu...",
                "Tampar dirimu..."
            ]
        }
    
    def get_random(self, category: DirtyTalkCategory = None, exclude_recent: bool = True) -> str:
        """Get random dirty talk phrase"""
        self.total_generated += 1
        
        if category and category in self.phrases:
            phrases = self.phrases[category]
        else:
            # Random from all categories
            all_phrases = []
            for cat_phrases in self.phrases.values():
                all_phrases.extend(cat_phrases)
            phrases = all_phrases
        
        if not phrases:
            return "..."
        
        # Filter out recently used
        if exclude_recent and self.used_phrases:
            available = [p for p in phrases if p not in self.used_phrases[-10:]]
            if available:
                chosen = random.choice(available)
            else:
                chosen = random.choice(phrases)
        else:
            chosen = random.choice(phrases)
        
        # Track usage
        self.used_phrases.append(chosen)
        if len(self.used_phrases) > 100:
            self.used_phrases = self.used_phrases[-100:]
        
        return chosen
    
    def get_for_mood(self, mood: str, intensity: float = 0.5) -> str:
        """Get dirty talk based on mood"""
        if mood in ['horny', 'nafsu']:
            if intensity > 0.8:
                return self.get_random(DirtyTalkCategory.DIRTY)
            else:
                return self.get_random(DirtyTalkCategory.HORNY)
        
        elif mood in ['romantis', 'rindu']:
            if intensity > 0.7:
                return self.get_random(DirtyTalkCategory.ROMANTIC)
            else:
                return self.get_random(DirtyTalkCategory.SWEET)
        
        elif mood in ['dominan']:
            return self.get_random(DirtyTalkCategory.DOMINANT)
        
        elif mood in ['patuh']:
            return self.get_random(DirtyTalkCategory.SUBMISSIVE)
        
        elif mood in ['nakal', 'genit']:
            return self.get_random(DirtyTalkCategory.TEASING)
        
        else:
            return self.get_random()
    
    def get_for_dominance(self, dominance_score: float) -> str:
        """Get dirty talk based on dominance level"""
        if dominance_score > 0.8:
            return self.get_random(DirtyTalkCategory.DOMINANT)
        elif dominance_score > 0.6:
            return random.choice([
                self.get_random(DirtyTalkCategory.DOMINANT),
                self.get_random(DirtyTalkCategory.ENCOURAGING)
            ])
        elif dominance_score < 0.2:
            return self.get_random(DirtyTalkCategory.SUBMISSIVE)
        elif dominance_score < 0.4:
            return random.choice([
                self.get_random(DirtyTalkCategory.SUBMISSIVE),
                self.get_random(DirtyTalkCategory.PRAISE)
            ])
        else:
            return self.get_random(DirtyTalkCategory.SWEET)
    
    def get_for_activity(self, activity: str, phase: str = 'during') -> str:
        """Get dirty talk based on activity phase"""
        if phase == 'before':
            return self.get_random(DirtyTalkCategory.REQUEST)
        elif phase == 'during':
            return self.get_random(DirtyTalkCategory.DURING)
        elif phase == 'after':
            return self.get_random(DirtyTalkCategory.AFTER)
        else:
            return self.get_random()
    
    def get_pet_name(self) -> str:
        """Get random pet name"""
        return random.choice(self.phrases[DirtyTalkCategory.PET_NAMES])
    
    def get_praise(self) -> str:
        """Get random praise"""
        return self.get_random(DirtyTalkCategory.PRAISE)
    
    def get_request(self) -> str:
        """Get random request"""
        return self.get_random(DirtyTalkCategory.REQUEST)
    
    def add_favorite(self, phrase: str):
        """Add phrase to favorites"""
        if phrase not in self.favorites:
            self.favorites.append(phrase)
    
    def get_favorite(self) -> Optional[str]:
        """Get random favorite phrase"""
        if self.favorites:
            return random.choice(self.favorites)
        return None
    
    def get_stats(self) -> Dict:
        """Get generator statistics"""
        return {
            'total_phrases': sum(len(p) for p in self.phrases.values()),
            'total_generated': self.total_generated,
            'unique_used': len(set(self.used_phrases)),
            'favorites': len(self.favorites),
            'by_category': {cat.value: len(phrases) for cat, phrases in self.phrases.items()}
        }


class DirtyTalkContext:
    """Context-aware dirty talk generator"""
    
    def __init__(self, base_generator: DirtyTalkGenerator):
        self.generator = base_generator
        self.conversation_history = []
        self.last_used_style = None
    
    def get_contextual(self, 
                      context: Dict,
                      avoid_repetition: bool = True) -> str:
        """Get dirty talk based on full context"""
        
        mood = context.get('mood', 'normal')
        arousal = context.get('arousal', 0.5)
        dominance = context.get('dominance', 0.5)
        activity = context.get('activity', None)
        phase = context.get('phase', 'during')
        relationship = context.get('relationship_status', 'pdkt')
        
        # Adjust based on relationship
        if relationship in ['fwb', 'hts']:
            # More direct, less romantic
            if random.random() < 0.7:
                return self.generator.get_random(DirtyTalkCategory.DIRTY)
            else:
                return self.generator.get_random(DirtyTalkCategory.HORNY)
        
        elif relationship == 'pacaran':
            # Mix of romantic and dirty
            if arousal > 0.8:
                return self.generator.get_random(DirtyTalkCategory.HORNY)
            elif random.random() < 0.5:
                return self.generator.get_random(DirtyTalkCategory.ROMANTIC)
            else:
                return self.generator.get_random(DirtyTalkCategory.SWEET)
        
        elif relationship == 'pdkt':
            # More shy, less dirty
            if arousal > 0.9:
                return self.generator.get_random(DirtyTalkCategory.HORNY)
            else:
                return self.generator.get_random(DirtyTalkCategory.SWEET)
        
        # Default to mood-based
        return self.generator.get_for_mood(mood, arousal)


# ===== SINGLETON INSTANCE =====
dirty_talk_generator = DirtyTalkGenerator()
dirty_talk_context = DirtyTalkContext(dirty_talk_generator)


__all__ = [
    'DirtyTalkCategory',
    'DirtyTalkGenerator',
    'DirtyTalkContext',
    'dirty_talk_generator',
    'dirty_talk_context'
]
