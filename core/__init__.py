#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
CORE PACKAGE
=============================================================================
Komponen inti AI agent untuk GADIS V81
"""

from core.agent import GadisAgent
from core.agent_pool import AgentPool
from core.consciousness import ContinuousConsciousness, SubconsciousProcessor
from core.emotion import PADEmotionModel
from core.personality import PersonalityFormingMemory
from core.decision import NeuralDecisionSystem
from core.load_balancer import AgentLoadBalancer, load_balancer

__version__ = "81.0.0"
__all__ = [
    'GadisAgent',
    'AgentPool',
    'ContinuousConsciousness',
    'SubconsciousProcessor',
    'PADEmotionModel',
    'PersonalityFormingMemory',
    'NeuralDecisionSystem',
    'AgentLoadBalancer',
    'load_balancer'
]
