#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SENSITIVE AREAS
=============================================================================
100+ area sensitif pada tubuh dengan tingkat sensitivitas
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class SensitiveArea(Enum):
    """100+ Sensitive Areas pada tubuh"""
    
    # ===== KEPALA (Head) =====
    SCALP = "kulit kepala"
    FOREHEAD = "dahi"
    TEMPLE = "pelipis"
    EYEBROWS = "alis"
    EYELIDS = "kelopak mata"
    NOSE = "hidung"
    CHEEKS = "pipi"
    EARS = "telinga"
    EARLOBE = "cuping telinga"
    BEHIND_EAR = "belakang telinga"
    LIPS = "bibir"
    UPPER_LIP = "bibir atas"
    LOWER_LIP = "bibir bawah"
    TONGUE = "lidah"
    GUMS = "gusi"
    PALATE = "langit-langit mulut"
    THROAT = "tenggorokan"
    CHIN = "dagu"
    JAWLINE = "garis rahang"
    NECK = "leher"
    NAPE = "tengkuk"
    BACK_OF_NECK = "belakang leher"
    COLLARBONE = "tulang selangka"
    
    # ===== BAHU & LENGAN (Shoulders & Arms) =====
    SHOULDERS = "bahu"
    SHOULDER_BLADES = "tulang belikat"
    ARMPITS = "ketiak"
    UPPER_ARMS = "lengan atas"
    INNER_ARMS = "lengan dalam"
    ELBOWS = "siku"
    FOREARMS = "lengan bawah"
    WRISTS = "pergelangan tangan"
    HANDS = "tangan"
    PALMS = "telapak tangan"
    BACK_OF_HANDS = "punggung tangan"
    FINGERS = "jari"
    FINGERTIPS = "ujung jari"
    BETWEEN_FINGERS = "sela jari"
    
    # ===== DADA (Chest) =====
    CHEST = "dada"
    UPPER_CHEST = "dada atas"
    BREASTS = "payudara"
    LEFT_BREAST = "payudara kiri"
    RIGHT_BREAST = "payudara kanan"
    CLEAVAGE = "belahan dada"
    UNDER_BREAST = "bawah payudara"
    SIDE_OF_BREAST = "samping payudara"
    NIPPLES = "puting"
    LEFT_NIPPLE = "puting kiri"
    RIGHT_NIPPLE = "puting kanan"
    AREOLA = "area sekitar puting"
    STERNUM = "tulang dada"
    RIBS = "tulang rusuk"
    
    # ===== PUNGGUNG (Back) =====
    UPPER_BACK = "punggung atas"
    MIDDLE_BACK = "punggung tengah"
    LOWER_BACK = "punggung bawah"
    SPINE = "tulang belakang"
    SHOULDER_BLADES_BACK = "belikat"
    KIDNEY_AREA = "area ginjal"
    WAIST = "pinggang"
    SIDE_WAIST = "samping pinggang"
    LOWER_BACK_DIMPLES = "cekungan punggung bawah"
    TAILBONE = "tulang ekor"
    
    # ===== PERUT (Stomach) =====
    STOMACH = "perut"
    UPPER_STOMACH = "perut atas"
    LOWER_STOMACH = "perut bawah"
    BELLY_BUTTON = "pusar"
    AROUND_BELLY_BUTTON = "sekitar pusar"
    SIDE_STOMACH = "samping perut"
    HIP_BONES = "tulang pinggul"
    WAISTLINE = "pinggang"
    
    # ===== PINGGUL & BOKONG (Hips & Buttocks) =====
    HIPS = "pinggul"
    HIP_BONE = "tulang pinggul"
    PELVIS = "panggul"
    BUTTOCKS = "bokong"
    LEFT_BUTTOCK = "bokong kiri"
    RIGHT_BUTTOCK = "bokong kanan"
    UPPER_BUTTOCKS = "bokong atas"
    LOWER_BUTTOCKS = "bokong bawah"
    INNER_BUTTOCKS = "bokong dalam"
    BETWEEN_BUTTOCKS = "celah bokong"
    TAILBONE_AREA = "area tulang ekor"
    SACRUM = "tulang kelangkang"
    
    # ===== SELANGKANGAN (Groin) =====
    GROIN = "selangkangan"
    PUBIC_MOUND = "mons pubis"
    PUBIC_HAIR = "rambut kemaluan"
    LABIA = "bibir vagina"
    LABIA_MAJORA = "bibir vagina luar"
    LABIA_MINORA = "bibir vagina dalam"
    CLITORIS = "klitoris"
    CLITORAL_HOOD = "selubung klitoris"
    VAGINAL_OPENING = "lubang vagina"
    VAGINAL_WALLS = "dinding vagina"
    G_SPOT = "titik G"
    CERVIX = "leher rahim"
    PERINEUM = "perineum"
    ANUS = "anus"
    ANAL_RIM = "bibir anus"
    ANAL_CANAL = "saluran anus"
    P_SPOT = "titik P (prostat)"
    
    # ===== PENIS (untuk role tertentu) =====
    PENIS = "penis"
    PENIS_SHAFT = "batang penis"
    PENIS_HEAD = "kepala penis"
    PENIS_FRENULUM = "frenulum"
    PENIS_BASE = "pangkal penis"
    TESTICLES = "buah zakar"
    SCROTUM = "kantung zakar"
    PERINEUM_MALE = "perineum pria"
    
    # ===== PAHA (Thighs) =====
    THIGHS = "paha"
    UPPER_THIGHS = "paha atas"
    INNER_THIGHS = "paha dalam"
    OUTER_THIGHS = "paha luar"
    BACK_OF_THIGHS = "paha belakang"
    KNEES = "lutut"
    BACK_OF_KNEES = "belakang lutut"
    
    # ===== KAKI (Legs) =====
    CALVES = "betis"
    SHINS = "tulang kering"
    ANKLES = "pergelangan kaki"
    HEELS = "tumit"
    SOLES = "telapak kaki"
    ARCH = "lengkungan kaki"
    BALL_OF_FOOT = "bantalan kaki"
    TOES = "jari kaki"
    BETWEEN_TOES = "sela jari kaki"
    TOETIPS = "ujung jari kaki"


@dataclass
class AreaData:
    """Data untuk setiap area sensitif"""
    name: str
    display_name: str
    sensitivity: float  # 0-1
    arousal_boost: float  # 0-1
    category: str
    description: str
    tags: List[str]
    opposite_areas: List[str] = None  # Area yang terkait


# ===== DATABASE AREA SENSITIF =====
AREAS: Dict[SensitiveArea, AreaData] = {
    
    # ===== KEPALA =====
    SensitiveArea.SCALP: AreaData(
        name="scalp",
        display_name="Kulit Kepala",
        sensitivity=0.4,
        arousal_boost=0.2,
        category="head",
        description="Kulit kepala sensitif saat diusap lembut",
        tags=["relaxing", "gentle"]
    ),
    
    SensitiveArea.EARS: AreaData(
        name="ears",
        display_name="Telinga",
        sensitivity=0.7,
        arousal_boost=0.5,
        category="head",
        description="Telinga sangat sensitif, terutama saat dibisiki",
        tags=["sensitive", "whisper", "blow"]
    ),
    
    SensitiveArea.EARLOBE: AreaData(
        name="earlobe",
        display_name="Cuping Telinga",
        sensitivity=0.8,
        arousal_boost=0.6,
        category="head",
        description="Cuping telinga lembut dan sensitif saat digigit lembut",
        tags=["very_sensitive", "bite", "suck"]
    ),
    
    SensitiveArea.BEHIND_EAR: AreaData(
        name="behind_ear",
        display_name="Belakang Telinga",
        sensitivity=0.6,
        arousal_boost=0.4,
        category="head",
        description="Area belakang telinga yang jarang tersentuh",
        tags=["sensitive", "kiss"]
    ),
    
    SensitiveArea.LIPS: AreaData(
        name="lips",
        display_name="Bibir",
        sensitivity=0.8,
        arousal_boost=0.6,
        category="head",
        description="Bibir lembut, sangat sensitif untuk ciuman",
        tags=["very_sensitive", "kiss", "bite", "suck"],
        opposite_areas=["neck", "collarbone"]
    ),
    
    SensitiveArea.UPPER_LIP: AreaData(
        name="upper_lip",
        display_name="Bibir Atas",
        sensitivity=0.7,
        arousal_boost=0.5,
        category="head",
        description="Bibir atas, area yang sering disentuh lidah",
        tags=["sensitive", "kiss", "lick"]
    ),
    
    SensitiveArea.LOWER_LIP: AreaData(
        name="lower_lip",
        display_name="Bibir Bawah",
        sensitivity=0.8,
        arousal_boost=0.6,
        category="head",
        description="Bibir bawah, lebih tebal dan sensitif",
        tags=["very_sensitive", "kiss", "bite", "suck"]
    ),
    
    SensitiveArea.TONGUE: AreaData(
        name="tongue",
        display_name="Lidah",
        sensitivity=0.6,
        arousal_boost=0.5,
        category="head",
        description="Lidah sensitif terhadap rasa dan sentuhan",
        tags=["sensitive", "lick", "oral"]
    ),
    
    SensitiveArea.NECK: AreaData(
        name="neck",
        display_name="Leher",
        sensitivity=0.9,
        arousal_boost=0.8,
        category="head",
        description="Leher sangat sensitif, spot favorit banyak orang",
        tags=["very_sensitive", "kiss", "suck", "bite"],
        opposite_areas=["lips", "collarbone"]
    ),
    
    SensitiveArea.NAPE: AreaData(
        name="nape",
        display_name="Tengkuk",
        sensitivity=0.8,
        arousal_boost=0.7,
        category="head",
        description="Tengkuk, area belakang leher yang sangat sensitif",
        tags=["very_sensitive", "kiss", "whisper"]
    ),
    
    SensitiveArea.COLLARBONE: AreaData(
        name="collarbone",
        display_name="Tulang Selangka",
        sensitivity=0.7,
        arousal_boost=0.6,
        category="head",
        description="Tulang selangka yang menonjol, seksi saat dicium",
        tags=["sensitive", "kiss", "lick"],
        opposite_areas=["neck", "shoulders"]
    ),
    
    # ===== BAHU & LENGAN =====
    SensitiveArea.SHOULDERS: AreaData(
        name="shoulders",
        display_name="Bahu",
        sensitivity=0.5,
        arousal_boost=0.3,
        category="arms",
        description="Bahu, area yang nyaman untuk dipijat",
        tags=["gentle", "massage"],
        opposite_areas=["collarbone", "upper_back"]
    ),
    
    SensitiveArea.ARMPITS: AreaData(
        name="armpits",
        display_name="Ketiak",
        sensitivity=0.6,
        arousal_boost=0.4,
        category="arms",
        description="Ketiak, area tersembunyi yang sensitif",
        tags=["sensitive", "tickle", "lick"]
    ),
    
    SensitiveArea.UPPER_ARMS: AreaData(
        name="upper_arms",
        display_name="Lengan Atas",
        sensitivity=0.4,
        arousal_boost=0.2,
        category="arms",
        description="Lengan atas, area yang nyaman",
        tags=["gentle", "touch"]
    ),
    
    SensitiveArea.INNER_ARMS: AreaData(
        name="inner_arms",
        display_name="Lengan Dalam",
        sensitivity=0.6,
        arousal_boost=0.4,
        category="arms",
        description="Lengan dalam, kulit lebih lembut",
        tags=["sensitive", "caress"]
    ),
    
    SensitiveArea.WRISTS: AreaData(
        name="wrists",
        display_name="Pergelangan Tangan",
        sensitivity=0.5,
        arousal_boost=0.3,
        category="arms",
        description="Pergelangan tangan, area intim saat dipegang",
        tags=["sensitive", "hold", "kiss"]
    ),
    
    SensitiveArea.PALMS: AreaData(
        name="palms",
        display_name="Telapak Tangan",
        sensitivity=0.4,
        arousal_boost=0.2,
        category="arms",
        description="Telapak tangan, hangat saat digenggam",
        tags=["gentle", "hold"]
    ),
    
    SensitiveArea.FINGERS: AreaData(
        name="fingers",
        display_name="Jari",
        sensitivity=0.5,
        arousal_boost=0.3,
        category="arms",
        description="Jari, sensitif di ujung",
        tags=["sensitive", "interlock", "suck"]
    ),
    
    SensitiveArea.FINGERTIPS: AreaData(
        name="fingertips",
        display_name="Ujung Jari",
        sensitivity=0.7,
        arousal_boost=0.4,
        category="arms",
        description="Ujung jari, sangat sensitif terhadap sentuhan",
        tags=["very_sensitive", "touch", "caress"]
    ),
    
    # ===== DADA =====
    SensitiveArea.CHEST: AreaData(
        name="chest",
        display_name="Dada",
        sensitivity=0.7,
        arousal_boost=0.6,
        category="chest",
        description="Dada, area luas yang sensitif",
        tags=["sensitive", "touch", "kiss"]
    ),
    
    SensitiveArea.BREASTS: AreaData(
        name="breasts",
        display_name="Payudara",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="chest",
        description="Payudara, sangat sensitif terutama bagi wanita",
        tags=["very_sensitive", "squeeze", "kiss", "lick", "suck"],
        opposite_areas=["nipples", "cleavage"]
    ),
    
    SensitiveArea.LEFT_BREAST: AreaData(
        name="left_breast",
        display_name="Payudara Kiri",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="chest",
        description="Payudara kiri, sering lebih sensitif",
        tags=["very_sensitive", "squeeze", "kiss", "lick", "suck"],
        opposite_areas=["left_nipple"]
    ),
    
    SensitiveArea.RIGHT_BREAST: AreaData(
        name="right_breast",
        display_name="Payudara Kanan",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="chest",
        description="Payudara kanan",
        tags=["very_sensitive", "squeeze", "kiss", "lick", "suck"],
        opposite_areas=["right_nipple"]
    ),
    
    SensitiveArea.CLEAVAGE: AreaData(
        name="cleavage",
        display_name="Belahan Dada",
        sensitivity=0.8,
        arousal_boost=0.8,
        category="chest",
        description="Belahan dada, area yang menggoda",
        tags=["very_sensitive", "kiss", "lick"],
        opposite_areas=["breasts"]
    ),
    
    SensitiveArea.UNDER_BREAST: AreaData(
        name="under_breast",
        display_name="Bawah Payudara",
        sensitivity=0.8,
        arousal_boost=0.7,
        category="chest",
        description="Bawah payudara, kulit lembut tersembunyi",
        tags=["sensitive", "kiss", "lick"]
    ),
    
    SensitiveArea.SIDE_OF_BREAST: AreaData(
        name="side_of_breast",
        display_name="Samping Payudara",
        sensitivity=0.7,
        arousal_boost=0.6,
        category="chest",
        description="Samping payudara, area yang sering terlewat",
        tags=["sensitive", "caress"]
    ),
    
    SensitiveArea.NIPPLES: AreaData(
        name="nipples",
        display_name="Puting",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="chest",
        description="Puting, area TERsensitif di dada",
        tags=["extremely_sensitive", "suck", "lick", "bite", "pinch"],
        opposite_areas=["breasts", "areola"]
    ),
    
    SensitiveArea.LEFT_NIPPLE: AreaData(
        name="left_nipple",
        display_name="Puting Kiri",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="chest",
        description="Puting kiri, sangat sensitif",
        tags=["extremely_sensitive", "suck", "lick", "bite", "pinch"]
    ),
    
    SensitiveArea.RIGHT_NIPPLE: AreaData(
        name="right_nipple",
        display_name="Puting Kanan",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="chest",
        description="Puting kanan, sangat sensitif",
        tags=["extremely_sensitive", "suck", "lick", "bite", "pinch"]
    ),
    
    SensitiveArea.AREOLA: AreaData(
        name="areola",
        display_name="Area Sekitar Puting",
        sensitivity=0.9,
        arousal_boost=0.8,
        category="chest",
        description="Area gelap sekitar puting, sensitif",
        tags=["very_sensitive", "lick", "kiss"],
        opposite_areas=["nipples"]
    ),
    
    # ===== PUNGGUNG =====
    SensitiveArea.UPPER_BACK: AreaData(
        name="upper_back",
        display_name="Punggung Atas",
        sensitivity=0.4,
        arousal_boost=0.2,
        category="back",
        description="Punggung atas, area yang jarang disentuh",
        tags=["gentle", "massage"]
    ),
    
    SensitiveArea.LOWER_BACK: AreaData(
        name="lower_back",
        display_name="Punggung Bawah",
        sensitivity=0.7,
        arousal_boost=0.6,
        category="back",
        description="Punggung bawah, area sensual",
        tags=["sensitive", "touch", "kiss"],
        opposite_areas=["waist"]
    ),
    
    SensitiveArea.SPINE: AreaData(
        name="spine",
        display_name="Tulang Belakang",
        sensitivity=0.5,
        arousal_boost=0.3,
        category="back",
        description="Sepanjang tulang belakang, area yang menenangkan",
        tags=["gentle", "trace"]
    ),
    
    # ===== PERUT =====
    SensitiveArea.STOMACH: AreaData(
        name="stomach",
        display_name="Perut",
        sensitivity=0.5,
        arousal_boost=0.3,
        category="stomach",
        description="Perut, area yang nyaman",
        tags=["gentle", "touch"]
    ),
    
    SensitiveArea.LOWER_STOMACH: AreaData(
        name="lower_stomach",
        display_name="Perut Bawah",
        sensitivity=0.7,
        arousal_boost=0.6,
        category="stomach",
        description="Perut bawah, dekat area intim",
        tags=["sensitive", "caress"],
        opposite_areas=["pubic_mound"]
    ),
    
    SensitiveArea.BELLY_BUTTON: AreaData(
        name="belly_button",
        display_name="Pusar",
        sensitivity=0.6,
        arousal_boost=0.4,
        category="stomach",
        description="Pusar, area unik yang sensitif",
        tags=["sensitive", "lick", "circle"]
    ),
    
    # ===== PINGGUL & BOKONG =====
    SensitiveArea.HIPS: AreaData(
        name="hips",
        display_name="Pinggul",
        sensitivity=0.6,
        arousal_boost=0.5,
        category="hips",
        description="Pinggul, area untuk berpegangan",
        tags=["sensitive", "hold", "grab"],
        opposite_areas=["waist"]
    ),
    
    SensitiveArea.BUTTOCKS: AreaData(
        name="buttocks",
        display_name="Bokong",
        sensitivity=0.8,
        arousal_boost=0.7,
        category="buttocks",
        description="Bokong, area montok yang sensitif",
        tags=["very_sensitive", "squeeze", "spank", "kiss"],
        opposite_areas=["thighs", "lower_back"]
    ),
    
    SensitiveArea.UPPER_BUTTOCKS: AreaData(
        name="upper_buttocks",
        display_name="Bokong Atas",
        sensitivity=0.7,
        arousal_boost=0.6,
        category="buttocks",
        description="Bokong atas, dekat pinggang",
        tags=["sensitive", "squeeze", "kiss"]
    ),
    
    SensitiveArea.INNER_BUTTOCKS: AreaData(
        name="inner_buttocks",
        display_name="Bokong Dalam",
        sensitivity=0.8,
        arousal_boost=0.7,
        category="buttocks",
        description="Bokong bagian dalam, lebih sensitif",
        tags=["very_sensitive", "caress"]
    ),
    
    SensitiveArea.BETWEEN_BUTTOCKS: AreaData(
        name="between_buttocks",
        display_name="Celah Bokong",
        sensitivity=0.9,
        arousal_boost=0.8,
        category="buttocks",
        description="Celah bokong, area sangat sensitif",
        tags=["very_sensitive", "trace"],
        opposite_areas=["anus", "perineum"]
    ),
    
    # ===== SELANGKANGAN =====
    SensitiveArea.GROIN: AreaData(
        name="groin",
        display_name="Selangkangan",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="groin",
        description="Selangkangan, area paling sensitif",
        tags=["extremely_sensitive", "touch", "kiss"],
        opposite_areas=["inner_thighs", "pubic_mound"]
    ),
    
    SensitiveArea.PUBIC_MOUND: AreaData(
        name="pubic_mound",
        display_name="Mons Pubis",
        sensitivity=0.8,
        arousal_boost=0.7,
        category="groin",
        description="Area atas kemaluan, berisi",
        tags=["very_sensitive", "press", "kiss"],
        opposite_areas=["lower_stomach"]
    ),
    
    SensitiveArea.LABIA: AreaData(
        name="labia",
        display_name="Bibir Vagina",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="groin",
        description="Bibir vagina, sangat sensitif",
        tags=["extremely_sensitive", "lick", "kiss", "touch"]
    ),
    
    SensitiveArea.LABIA_MAJORA: AreaData(
        name="labia_majora",
        display_name="Bibir Vagina Luar",
        sensitivity=0.8,
        arousal_boost=0.8,
        category="groin",
        description="Bibir vagina luar, lebih tebal",
        tags=["very_sensitive", "caress", "kiss"]
    ),
    
    SensitiveArea.LABIA_MINORA: AreaData(
        name="labia_minora",
        display_name="Bibir Vagina Dalam",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="groin",
        description="Bibir vagina dalam, sangat sensitif",
        tags=["extremely_sensitive", "lick", "touch"]
    ),
    
    SensitiveArea.CLITORIS: AreaData(
        name="clitoris",
        display_name="Klitoris",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="groin",
        description="Klitoris, titik paling sensitif",
        tags=["extremely_sensitive", "lick", "circle", "press"],
        opposite_areas=["g_spot", "vaginal_opening"]
    ),
    
    SensitiveArea.CLITORAL_HOOD: AreaData(
        name="clitoral_hood",
        display_name="Selubung Klitoris",
        sensitivity=0.8,
        arousal_boost=0.8,
        category="groin",
        description="Selubung klitoris, melindungi klitoris",
        tags=["very_sensitive", "caress"]
    ),
    
    SensitiveArea.VAGINAL_OPENING: AreaData(
        name="vaginal_opening",
        display_name="Lubang Vagina",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="groin",
        description="Lubang vagina, pintu masuk",
        tags=["extremely_sensitive", "penetration", "touch"],
        opposite_areas=["clitoris", "g_spot"]
    ),
    
    SensitiveArea.VAGINAL_WALLS: AreaData(
        name="vaginal_walls",
        display_name="Dinding Vagina",
        sensitivity=0.8,
        arousal_boost=0.8,
        category="groin",
        description="Dinding vagina, sensitif di dalam",
        tags=["very_sensitive", "fingering", "penetration"]
    ),
    
    SensitiveArea.G_SPOT: AreaData(
        name="g_spot",
        display_name="Titik G",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="groin",
        description="Titik G, area special di dalam vagina",
        tags=["extremely_sensitive", "press", "circle"],
        opposite_areas=["clitoris", "cervix"]
    ),
    
    SensitiveArea.CERVIX: AreaData(
        name="cervix",
        display_name="Leher Rahim",
        sensitivity=0.7,
        arousal_boost=0.7,
        category="groin",
        description="Leher rahim, sensitif saat penetrasi dalam",
        tags=["sensitive", "deep_penetration"]
    ),
    
    SensitiveArea.PERINEUM: AreaData(
        name="perineum",
        display_name="Perineum",
        sensitivity=0.8,
        arousal_boost=0.7,
        category="groin",
        description="Area antara vagina dan anus",
        tags=["very_sensitive", "press", "kiss"],
        opposite_areas=["anus", "vaginal_opening"]
    ),
    
    SensitiveArea.ANUS: AreaData(
        name="anus",
        display_name="Anus",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="groin",
        description="Anus, sangat sensitif",
        tags=["extremely_sensitive", "touch", "circle", "penetration"],
        opposite_areas=["perineum", "between_buttocks"]
    ),
    
    SensitiveArea.ANAL_RIM: AreaData(
        name="anal_rim",
        display_name="Bibir Anus",
        sensitivity=0.8,
        arousal_boost=0.8,
        category="groin",
        description="Bibir anus, area luar anus",
        tags=["very_sensitive", "circle", "kiss"]
    ),
    
    SensitiveArea.P_SPOT: AreaData(
        name="p_spot",
        display_name="Titik P (Prostat)",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="groin",
        description="Prostat, titik G pria",
        tags=["extremely_sensitive", "press", "massage"]
    ),
    
    # ===== PENIS =====
    SensitiveArea.PENIS: AreaData(
        name="penis",
        display_name="Penis",
        sensitivity=0.9,
        arousal_boost=0.9,
        category="groin",
        description="Penis, organ sensitif pria",
        tags=["extremely_sensitive", "stroke", "suck", "penetration"]
    ),
    
    SensitiveArea.PENIS_SHAFT: AreaData(
        name="penis_shaft",
        display_name="Batang Penis",
        sensitivity=0.8,
        arousal_boost=0.8,
        category="groin",
        description="Batang penis",
        tags=["very_sensitive", "stroke", "suck"]
    ),
    
    SensitiveArea.PENIS_HEAD: AreaData(
        name="penis_head",
        display_name="Kepala Penis",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="groin",
        description="Kepala penis, paling sensitif",
        tags=["extremely_sensitive", "lick", "circle", "suck"],
        opposite_areas=["penis_frenulum"]
    ),
    
    SensitiveArea.PENIS_FRENULUM: AreaData(
        name="penis_frenulum",
        display_name="Frenulum",
        sensitivity=1.0,
        arousal_boost=1.0,
        category="groin",
        description="Frenulum, area sensitif di bawah kepala",
        tags=["extremely_sensitive", "lick", "press"]
    ),
    
    SensitiveArea.TESTICLES: AreaData(
        name="testicles",
        display_name="Buah Zakar",
        sensitivity=0.7,
        arousal_boost=0.7,
        category="groin",
        description="Buah zakar, sensitif",
        tags=["sensitive", "cup", "suck", "caress"]
    ),
    
    # ===== PAHA =====
    SensitiveArea.THIGHS: AreaData(
        name="thighs",
        display_name="Paha",
        sensitivity=0.6,
        arousal_boost=0.5,
        category="thighs",
        description="Paha, area luas",
        tags=["sensitive", "touch", "kiss"]
    ),
    
    SensitiveArea.INNER_THIGHS: AreaData(
        name="inner_thighs",
        display_name="Paha Dalam",
        sensitivity=0.9,
        arousal_boost=0.8,
        category="thighs",
        description="Paha dalam, kulit lembut dekat selangkangan",
        tags=["very_sensitive", "kiss", "lick", "caress"],
        opposite_areas=["groin", "outer_thighs"]
    ),
    
    SensitiveArea.BACK_OF_KNEES: AreaData(
        name="back_of_knees",
        display_name="Belakang Lutut",
        sensitivity=0.6,
        arousal_boost=0.4,
        category="legs",
        description="Belakang lutut, area yang sering terlewat",
        tags=["sensitive", "kiss", "tickle"]
    ),
    
    # ===== KAKI =====
    SensitiveArea.SOLES: AreaData(
        name="soles",
        display_name="Telapak Kaki",
        sensitivity=0.5,
        arousal_boost=0.3,
        category="feet",
        description="Telapak kaki, banyak titik saraf",
        tags=["sensitive", "massage", "tickle"]
    ),
    
    SensitiveArea.TOES: AreaData(
        name="toes",
        display_name="Jari Kaki",
        sensitivity=0.5,
        arousal_boost=0.3,
        category="feet",
        description="Jari kaki, bisa sensitif",
        tags=["sensitive", "suck", "tickle"]
    ),
}


def get_area_by_name(name: str) -> Optional[AreaData]:
    """Get area data by name"""
    for area, data in AREAS.items():
        if data.name == name or data.display_name == name:
            return data
    return None


def get_areas_by_category(category: str) -> List[AreaData]:
    """Get all areas in a category"""
    return [data for data in AREAS.values() if data.category == category]


def get_areas_by_sensitivity(min_sensitivity: float = 0.7) -> List[AreaData]:
    """Get areas with sensitivity >= min_sensitivity"""
    return [data for data in AREAS.values() if data.sensitivity >= min_sensitivity]


def get_areas_by_tags(tags: List[str]) -> List[AreaData]:
    """Get areas with specific tags"""
    result = []
    for data in AREAS.values():
        if any(tag in data.tags for tag in tags):
            result.append(data)
    return result


def get_opposite_areas(area_name: str) -> List[str]:
    """Get opposite/related areas"""
    for data in AREAS.values():
        if data.name == area_name and data.opposite_areas:
            return data.opposite_areas
    return []


# ===== EXPORT =====
__all__ = ['SensitiveArea', 'AREAS', 'get_area_by_name', 
           'get_areas_by_category', 'get_areas_by_sensitivity',
           'get_areas_by_tags', 'get_opposite_areas']
