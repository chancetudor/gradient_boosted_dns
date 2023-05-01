from enum import Enum


class CharDef(Enum):
    # Copyright (C) 2020 Claudio Marques - All Rights Reserved
    # Modified 2023 Chance Tudor
    """Enumeration of what constitutes specific character types."""
    VOWEL = "aeiou"
    CONSONANT = "bcdfghjklmnpqrstvwxyz"
    NUMERIC = "0123456789"
    SPECIALCHAR = "!\"#|\\$%&/()=?«»´`*+ºª^~;,-_@£€{[]}'"


class FileDef(Enum):
    """Enumeration of data files."""

    SANS_HIGH = "data/sus/sans_high.csv"
    SANS_MED = "data/sus/sans_med.csv"
    SANS_LOW = "data/sus/sans_low.csv"
    OISD = "data/sus/oisd_big_domains.csv"
    CERTPL = "data/sus/certpl.csv"
    AIRVPN = "data/sus/airvpn.csv"
    BENIGN = "data/legit/top-1m.csv"
    ALL = "data/all.csv"
    TRAIN = "data/train.csv"
    VALIDATE = "data/val.csv"
    TEST = "data/test.csv"
