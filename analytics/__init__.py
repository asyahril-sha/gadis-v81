#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
ANALYTICS PACKAGE
=============================================================================
Analisis data untuk bot (single-user)
"""

from analytics.user_growth import UserAnalytics
from analytics.sexual_stats import SexualStatistics
from analytics.peak_hours import PeakHoursAnalyzer
from analytics.reports import ReportGenerator

__version__ = "81.0.0"
__all__ = [
    'UserAnalytics',
    'SexualStatistics',
    'PeakHoursAnalyzer',
    'ReportGenerator'
]
