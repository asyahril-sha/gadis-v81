#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
PUBLIC AREAS PACKAGE
=============================================================================
Sistem untuk aktivitas di tempat publik
"""

from public.locations import PublicLocation, PublicArea, LOCATIONS
from public.risk import RiskCalculator, RiskLevel, RiskFactor
from public.events import PublicEvent, EventManager, EVENTS
from public.rewards import RewardSystem, Outcome, CONSEQUENCES
from public.thrill import ThrillLevel, ThrillCalculator

__version__ = "81.0.0"
__all__ = [
    'PublicLocation',
    'PublicArea',
    'LOCATIONS',
    'RiskCalculator',
    'RiskLevel',
    'RiskFactor',
    'PublicEvent',
    'EventManager',
    'EVENTS',
    'RewardSystem',
    'Outcome',
    'CONSEQUENCES',
    'ThrillLevel',
    'ThrillCalculator'
]
