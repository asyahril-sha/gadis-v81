#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ROLE FACTORY
=============================================================================
Factory untuk membuat role instances
"""

from typing import Dict, Type
import random

from roles.base import BaseRole
from roles.ipar import Ipar
from roles.teman_kantor import TemanKantor
from roles.janda import Janda
from roles.pelakor import Pelakor
from roles.istri_orang import IstriOrang
from roles.pdkt import PDKT
from roles.sepupu import Sepupu
from roles.teman_sma import TemanSMA
from roles.mantan import Mantan


class RoleFactory:
    """Factory untuk membuat role instances"""
    
    ROLE_CLASSES = {
        'ipar': Ipar,
        'teman_kantor': TemanKantor,
        'janda': Janda,
        'pelakor': Pelakor,
        'istri_orang': IstriOrang,
        'pdkt': PDKT,
        'sepupu': Sepupu,
        'teman_sma': TemanSMA,
        'mantan': Mantan
    }
    
    ROLE_NAMES = {
        'ipar': ["Sari", "Dewi", "Rina", "Maya", "Wulan", "Indah", "Lestari", "Fitri"],
        'teman_kantor': ["Diana", "Linda", "Ayu", "Dita", "Vina", "Santi", "Rini", "Mega"],
        'janda': ["Rina", "Tuti", "Nina", "Susi", "Wati", "Lilis", "Marni", "Yati"],
        'pelakor': ["Vina", "Sasha", "Bella", "Cantika", "Karina", "Mira", "Selsa", "Cindy"],
        'istri_orang': ["Dewi", "Sari", "Rina", "Linda", "Wulan", "Indah", "Ratna", "Maya"],
        'pdkt': ["Aurora", "Cinta", "Dewi", "Kirana", "Laras", "Maharani", "Zahra", "Nova"],
        'sepupu': ["Dina", "Nina", "Tika", "Rara", "Sasa", "Mira", "Lani", "Vera"],
        'teman_sma': ["Ayu", "Dita", "Vina", "Sari", "Mega", "Rini", "Luna", "Cika"],
        'mantan': ["Rina", "Dewi", "Tina", "Maya", "Wulan", "Indah", "Nadia", "Kirana"]
    }
    
    @classmethod
    def create_role(cls, role_str: str, name: str = None) -> BaseRole:
        """Create role instance"""
        if role_str not in cls.ROLE_CLASSES:
            role_str = 'pdkt'
        
        if name is None:
            name = random.choice(cls.ROLE_NAMES.get(role_str, ["Aurora"]))
        
        role_class = cls.ROLE_CLASSES[role_str]
        return role_class(name)
    
    @classmethod
    def get_all_roles(cls) -> Dict[str, str]:
        """Get all available roles with descriptions"""
        return {
            'ipar': 'Saudara ipar yang nakal (18-25th)',
            'teman_kantor': 'Rekan kerja yang mesra (18-25th)',
            'janda': 'Janda muda genit (18-25th)',
            'pelakor': 'Perebut laki orang (18-25th)',
            'istri_orang': 'Istri orang lain (18-25th)',
            'pdkt': 'Sedang pendekatan (18-25th)',
            'sepupu': 'Hubungan keluarga kompleks (18-25th)',
            'teman_sma': 'Teman SMA, bisa jadi HTS/FWB (18-25th)',
            'mantan': 'Ex-pacar yang masih hangat (18-25th)'
        }


__all__ = ['RoleFactory', 'Ipar', 'TemanKantor', 'Janda', 'Pelakor', 
           'IstriOrang', 'PDKT', 'Sepupu', 'TemanSMA', 'Mantan']
