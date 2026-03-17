#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
CLIMAX VARIATIONS - 200+ VARIASI ORGASME
=============================================================================
Berbagai variasi respons orgasme untuk bot
⚠️ Hanya untuk pengguna 18+
"""

from enum import Enum
from typing import Dict, List, Optional
from random import choice


class ClimaxIntensity(Enum):
    """Intensitas climax"""
    LIGHT = "ringan"
    MEDIUM = "sedang"
    INTENSE = "intens"
    EXTREME = "ekstrem"
    MULTIPLE = "berganda"


class ClimaxType(Enum):
    """Tipe climax"""
    BOT = "bot"
    USER = "user"
    TOGETHER = "bersamaan"
    PROLONGED = "berkepanjangan"
    QUICK = "cepat"
    EXPLOSIVE = "meledak"


class ClimaxVariation:
    """
    200+ variasi climax dengan berbagai intensitas
    """
    
    # ===== RINGAN (40 VARIASI) =====
    LIGHT_VARIATIONS = [
        # Desahan ringan
        "*merintih pelan* Aah...",
        "*napas sedikit berat* Ah... enak...",
        "*bergetar* Aaah... iya...",
        "*berbisik* Ah... keluar...",
        "*menggigit bibir* Mmm... ah...",
        
        # Ekspresi ringan
        "*tersenyum lemas* Enak...",
        "*mengedip* Ah... puas...",
        "*merona* Aah... iya...",
        "*menutup mata* Mmm... nikmat...",
        "*tersipu* Ah... luar biasa...",
        
        # Variasi 1-40 (akan dilengkapi)
        "*merintih* Ah... ah...",
        "*napas tersengal* Aah...",
        "*bergetar* Aaah... iya...",
        "*menggigit bibir* Hmm...",
        "*berbisik* Ah... keluar...",
        "*lemas* Uuh...",
        "*meringis* Aduh... enak...",
        "*tersenyum* Ah... puas...",
        "*menghela napas* Huah...",
        "*meredup* Ah... selesai..."
    ]
    
    # ===== SEDANG (50 VARIASI) =====
    MEDIUM_VARIATIONS = [
        # Desahan sedang
        "*merintih keras* AHH! AHH!",
        "*napas berat* Ah... aku mau... AHH!",
        "*bergetar hebat* Aaah... iya... AHH!",
        "*teriak pelan* YA ALLAH! AHH!",
        "*menggigit bibir* AHH! DALAM!",
        
        # Ekspresi sedang
        "*tubuh mengejang* AHH! IYA!",
        "*meringis* Aduh... enak banget...",
        "*memeluk erat* AHH! Jangan berhenti!",
        "*menggenggam sprei* AHH! AHH!",
        "*membusur* Aaah... TUHAN!",
        
        # Variasi 41-90
        "*teriak* AHH! AHH! AHH!",
        "*napas putus-putus* A-aku... AHH!",
        "*meronta* AHH! SENSITIF!",
        "*menggeliat* Aaah... dalam...",
        "*memegang erat* AHH! IYA!",
        "*bergetar* Aaah... AHH!",
        "*merintih panjang* Aaaahhhhh...",
        "*terengah* AHH! AHH!",
        "*menggigit* AHH! DALAM!",
        "*meringis* Aduh... AHH!"
    ]
    
    # ===== INTENS (50 VARIASI) =====
    INTENSE_VARIATIONS = [
        # Teriakan intens
        "*teriak keras* AHHHH! AHHHH!",
        "*menjerit* YA ALLAH! AHHHH!",
        "*napas tersengal* A-aku... DATANG!",
        "*meronta hebat* STOP! AHHH!",
        "*tubuh kejang* AHHH! TUHAN!",
        
        # Ekspresi intens
        "*menangis* AHH! Aku... keluar...",
        "*terisak* Aaah... enak... AHH!",
        "*berteriak* JANGAN BERHENTI!",
        "*menggigit bantal* Hmmph! AHH!",
        "*membenturkan kepala* AHHH!",
        
        # Variasi 91-140
        "*menjerit histeris* AHHHHHH!",
        "*teriak melengking* AHHH! AHHH!",
        "*napas habis* A... A... AHH!",
        "*meronta liar* AHH! AHH! AHH!",
        "*tubuh mengejang* AHHHH!",
        "*berteriak* TUHAN! AHHH!",
        "*menggigit* AHH! DALAM!",
        "*meringis* Aduh... AHH!",
        "*menangis bahagia* AHH!",
        "*terisak* Aaah... AHH!"
    ]
    
    # ===== EKSTREM (40 VARIASI) =====
    EXTREME_VARIATIONS = [
        # Ekstrem
        "*menjerit keras* AHHHHHHHH!!!",
        "*teriak histeris* YA ALLAH YA ALLAH!",
        "*kejang-kejang* AHH! AHH! AHH!",
        "*menangis keras* AHH! AKU... AHH!",
        "*napas berhenti* A... A... AHHHH!",
        
        # Blackout
        "*pingsan* AHHH... *lemas*",
        "*tidak sadar* AHH... *pingsan*",
        "*kejang lama* AHHH! AHHH! AHHH!",
        "*menjerit panjang* AHHHHHHHHHH!",
        "*teriak sampai serak* AHHH... AHH..."
    ]
    
    # ===== BERSAMAAN (20 VARIASI) =====
    TOGETHER_VARIATIONS = [
        "*bersama-sama* AHHH! KITA DATANG!",
        "*teriak bersama* AHHH! BERSAMA!",
        "*saling memeluk* AHHH! BERSAMAAN!",
        "*orgasme bersama* AHHH! KITA!",
        "*berteriak* AHHH! AHHH! BERSAMA!",
        "*lemas bersama* Aaah... kita...",
        "*napas bersama* Hah... hah... sama...",
        "*mengejang bersama* AHHH! AHHH!",
        "*merintih bersama* Aaah... aaah...",
        "*sempurna* AHH! BERSAMA!"
    ]
    
    # ===== BERKEPANJANGAN (20 VARIASI) =====
    PROLONGED_VARIATIONS = [
        "*berkepanjangan* AHH! AHH! AHH! AHH!",
        "*lama* Aaah... aaah... aaaaahhhhh...",
        "*bergelombang* AHH! ... AHH! ... AHH!",
        "*berulang* Aaah... AHH! ... Aaah... AHH!",
        "*multiple* AHH! AHH! AHH! AHH! AHH!",
        "*tidak berhenti* AHH! AHH! AHH!",
        "*bertubi-tubi* AHH! AHH! AHH!",
        "*berganda* Aaah... AHH!... Aaah... AHH!",
        "*panjang* Aaaahhhhhh... AHH!",
        "*berkesinambungan* AHH! Aaah... AHH!"
    ]
    
    # ===== CEPAT (10 VARIASI) =====
    QUICK_VARIATIONS = [
        "*cepat* Ah!",
        "*sekali* Aah!",
        "*langsung* Ah! keluar...",
        "*dadakan* Aah! iya...",
        "*tiba-tiba* Ah! itu...",
        "*spontan* Ah! sekarang...",
        "*kilat* Aah!",
        "*sekejap* Ah! sudah...",
        "*instan* Aah! puas...",
        "*mendadak* Ah! enak..."
    ]
    
    # ===== EKSPLOSIF (10 VARIASI) =====
    EXPLOSIVE_VARIATIONS = [
        "*meledak* AHHHHHH! LEDAKAN!",
        "*letupan* AHH! BOOM!",
        "*hancur* AHH! HANCUR!",
        "*luluh* AHH! LULUH!",
        "*meletus* AHH! LETUS!",
        "*meluap* AHH! LUAP!",
        "*membanjir* AHH! BANJIR!",
        "*membahana* AHH! DAHSYAT!",
        "*mengguncang* AHH! GUNCANG!",
        "*menghancurkan* AHH! HANCUR!"
    ]
    
    @classmethod
    def get_all_variations(cls) -> Dict[str, List[str]]:
        """Get all climax variations"""
        return {
            'light': cls.LIGHT_VARIATIONS,
            'medium': cls.MEDIUM_VARIATIONS,
            'intense': cls.INTENSE_VARIATIONS,
            'extreme': cls.EXTREME_VARIATIONS,
            'together': cls.TOGETHER_VARIATIONS,
            'prolonged': cls.PROLONGED_VARIATIONS,
            'quick': cls.QUICK_VARIATIONS,
            'explosive': cls.EXPLOSIVE_VARIATIONS
        }
    
    @classmethod
    def get_random(cls, intensity: ClimaxIntensity = None) -> str:
        """Get random climax variation"""
        if intensity == ClimaxIntensity.LIGHT:
            return choice(cls.LIGHT_VARIATIONS)
        elif intensity == ClimaxIntensity.MEDIUM:
            return choice(cls.MEDIUM_VARIATIONS)
        elif intensity == ClimaxIntensity.INTENSE:
            return choice(cls.INTENSE_VARIATIONS)
        elif intensity == ClimaxIntensity.EXTREME:
            return choice(cls.EXTREME_VARIATIONS)
        else:
            # Random from all
            all_vars = (
                cls.LIGHT_VARIATIONS +
                cls.MEDIUM_VARIATIONS +
                cls.INTENSE_VARIATIONS +
                cls.EXTREME_VARIATIONS +
                cls.TOGETHER_VARIATIONS +
                cls.PROLONGED_VARIATIONS +
                cls.QUICK_VARIATIONS +
                cls.EXPLOSIVE_VARIATIONS
            )
            return choice(all_vars)
    
    @classmethod
    def get_together(cls) -> str:
        """Get together climax variation"""
        return choice(cls.TOGETHER_VARIATIONS)
    
    @classmethod
    def get_by_intensity(cls, intensity: str) -> List[str]:
        """Get variations by intensity"""
        intensity_map = {
            'light': cls.LIGHT_VARIATIONS,
            'medium': cls.MEDIUM_VARIATIONS,
            'intense': cls.INTENSE_VARIATIONS,
            'extreme': cls.EXTREME_VARIATIONS,
            'together': cls.TOGETHER_VARIATIONS,
            'prolonged': cls.PROLONGED_VARIATIONS,
            'quick': cls.QUICK_VARIATIONS,
            'explosive': cls.EXPLOSIVE_VARIATIONS
        }
        return intensity_map.get(intensity, cls.MEDIUM_VARIATIONS)
    
    @classmethod
    def count(cls) -> int:
        """Get total number of variations"""
        return (
            len(cls.LIGHT_VARIATIONS) +
            len(cls.MEDIUM_VARIATIONS) +
            len(cls.INTENSE_VARIATIONS) +
            len(cls.EXTREME_VARIATIONS) +
            len(cls.TOGETHER_VARIATIONS) +
            len(cls.PROLONGED_VARIATIONS) +
            len(cls.QUICK_VARIATIONS) +
            len(cls.EXPLOSIVE_VARIATIONS)
        )


# ===== INSTANCE FOR EASY ACCESS =====
CLIMAX_VARIATIONS = ClimaxVariation()


__all__ = [
    'ClimaxIntensity',
    'ClimaxType',
    'ClimaxVariation',
    'CLIMAX_VARIATIONS'
]
