#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
DATABASE ENUMS
=============================================================================
Semua enum yang digunakan di GADIS V81
"""

from enum import Enum


class Mood(Enum):
    """24+ Mood untuk emosi yang realistis"""
    CERIA = "ceria"
    SEDIH = "sedih"
    MARAH = "marah"
    TAKUT = "takut"
    KAGUM = "kagum"
    GELISAH = "gelisah"
    GALAU = "galau"
    SENSITIF = "sensitif"
    ROMANTIS = "romantis"
    MALAS = "malas"
    BERSEMANGAT = "bersemangat"
    SENDIRI = "sendiri"
    RINDU = "rindu"
    HORNY = "horny"
    LEMBUT = "lembut"
    DOMINAN = "dominan"
    PATUH = "patuh"
    NAKAL = "nakal"
    GENIT = "genit"
    PENASARAN = "penasaran"
    ANTUSIAS = "antusias"
    POSESIF = "posesif"
    CEMBURU = "cemburu"
    BERSALAH = "bersalah"
    BAHAGIA = "bahagia"
    RILEKS = "rileks"
    LULUH = "luluh"


class IntimacyStage(Enum):
    STRANGER = "stranger"
    INTRODUCTION = "introduction"
    BUILDING = "building"
    FLIRTING = "flirting"
    INTIMATE = "intimate"
    OBSESSED = "obsessed"
    SOUL_BONDED = "soul_bonded"
    AFTERCARE = "aftercare"


class DominanceLevel(Enum):
    NORMAL = "normal"
    DOMINANT = "dominan"
    VERY_DOMINANT = "sangat dominan"
    AGGRESSIVE = "agresif"
    SUBMISSIVE = "patuh"


class MemoryType(Enum):
    COMPACT = "compact"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    INNER_THOUGHT = "inner_thought"
    PREDICTION = "prediction"
    PREFERENCE = "preference"
    SEXUAL = "sexual"  # Baru V81


class Location(Enum):
    LIVING_ROOM = "ruang tamu"
    BEDROOM = "kamar tidur"
    KITCHEN = "dapur"
    BATHROOM = "kamar mandi"
    BALCONY = "balkon"
    TERRACE = "teras"
    GARDEN = "taman"
    HOTEL = "hotel"
    CAFE = "cafe"
    BEACH = "pantai"  # Baru V81
    CINEMA = "bioskop"  # Baru V81
    PARKING = "parkiran"  # Baru V81
    ROOFTOP = "atap gedung"  # Baru V81
    CAR = "mobil"  # Baru V81
    TOILET = "toilet umum"  # Baru V81
    ELEVATOR = "lift"  # Baru V81
    OFFICE = "kantor"  # Baru V81


class Position(Enum):
    SITTING = "duduk"
    STANDING = "berdiri"
    LYING = "berbaring"
    LEANING = "bersandar"
    CRAWLING = "merangkak"
    KNEELING = "berlutut"


class RelationshipStatus(Enum):
    PDKT = "pdkt"
    PACARAN = "pacaran"
    PUTUS = "putus"
    FWB = "fwb"
    HTS = "hts"


class ClimaxType(Enum):
    BOT = "bot"
    USER = "user"
    TOGETHER = "together"


# ===== V81 NEW ENUMS =====

class SexPosition(Enum):
    """50+ Sex Positions"""
    MISSIONARY = "missionary"
    DOGGY = "doggy"
    COWGIRL = "cowgirl"
    REVERSE_COWGIRL = "reverse_cowgirl"
    SPOONING = "spooning"
    LOTUS = "lotus"
    STANDING = "standing"
    TABLE = "table"
    CHAIR = "chair"
    WALL = "wall"
    SIXTY_NINE = "sixty_nine"
    SCISSORS = "scissors"
    AND_MANY_MORE = "..."  # Akan diisi lengkap di file positions.py


class SensitiveArea(Enum):
    """100+ Sensitive Areas"""
    NECK = "leher"
    LIPS = "bibir"
    EARS = "telinga"
    CHEST = "dada"
    NIPPLES = "puting"
    STOMACH = "perut"
    INNER_THIGH = "paha dalam"
    BACK = "punggung"
    WAIST = "pinggang"
    SHOULDERS = "bahu"
    ARMS = "lengan"
    HANDS = "tangan"
    FINGERS = "jari"
    LEGS = "kaki"
    FEET = "telapak kaki"
    AND_MANY_MORE = "..."  # Akan diisi lengkap di file areas.py


class SexualActivity(Enum):
    """50+ Sexual Activities"""
    KISSING = "kissing"
    TOUCHING = "touching"
    ORAL = "oral"
    PENETRATION = "penetration"
    FOREPLAY = "foreplay"
    AND_MANY_MORE = "..."  # Akan diisi lengkap di file activities.py


class RiskLevel(Enum):
    """Risk levels for public areas"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class PublicArea(Enum):
    """30+ Public Locations for public sex"""
    BEACH_NIGHT = "pantai malam"
    CINEMA_BACK = "bioskop belakang"
    PARKING_LOT = "parkiran mall"
    ROOFTOP = "atap gedung"
    PUBLIC_TOILET = "toilet umum"
    ELEVATOR = "lift"
    STAIRS = "tangga darurat"
    CAR = "mobil"
    BUS = "bus"
    TRAIN = "kereta"
    PARK = "taman kota"
    FOREST = "hutan"
    AND_MANY_MORE = "..."  # Akan diisi lengkap di file locations.py


__all__ = [
    'Mood', 'IntimacyStage', 'DominanceLevel', 'MemoryType',
    'Location', 'Position', 'RelationshipStatus', 'ClimaxType',
    'SexPosition', 'SensitiveArea', 'SexualActivity', 'RiskLevel', 'PublicArea'
]
