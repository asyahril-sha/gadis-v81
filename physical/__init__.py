#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
PHYSICAL SYSTEMS PACKAGE
=============================================================================
Komponen fisik untuk bot - atribut, pakaian, lokasi, pergerakan
"""

from physical.attributes import PhysicalAttributesGenerator
from physical.clothing import ClothingSystem
from physical.location import LocationSystem
from physical.movement import MovementSystem, Position

__version__ = "81.0.0"
__all__ = [
    'PhysicalAttributesGenerator',
    'ClothingSystem',
    'LocationSystem',
    'MovementSystem',
    'Position'
]
