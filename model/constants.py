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

    SANS_HIGH = "/home/chance/GitHub/gradient_boosted_dns/data/sus/sans_high.csv"
    SANS_MED = "/home/chance/GitHub/gradient_boosted_dns/data/sus/sans_med.csv"
    SANS_LOW = "/home/chance/GitHub/gradient_boosted_dns/data/sus/sans_low.csv"
    OISD = "/home/chance/GitHub/gradient_boosted_dns/data/sus/oisd_big_domains.csv"
    CERTPL = "/home/chance/GitHub/gradient_boosted_dns/data/sus/certpl.csv"
    AIRVPN = "/home/chance/GitHub/gradient_boosted_dns/data/sus/airvpn.csv"
    BENIGN = "/home/chance/GitHub/gradient_boosted_dns/data/legit/top-1m.csv"
    ALL = "/home/chance/GitHub/gradient_boosted_dns/data/all.csv"
    TRAIN = "/home/chance/GitHub/gradient_boosted_dns/data/train.csv"
    VALIDATE = "/home/chance/GitHub/gradient_boosted_dns/data/val.csv"
    TEST = "/home/chance/GitHub/gradient_boosted_dns/data/test.csv"
