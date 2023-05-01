import re
import logging
import numpy as np
import pandas as pd
from constants import *

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log/debug.log", mode="w")],
)


def ratio_calculator(row: pd.Series, char_type: str) -> float:
    # Copyright (C) 2020 Claudio Marques - All Rights Reserved
    # Modified 2023 Chance Tudor
    """Calculates the percentage of specific character types that make up a domain name."""
    domain = row["domain"]
    try:
        return len([char for char in domain if char in char_type]) / len(domain)
    except Exception as e:
        logging.exception(f"Error in ratio_calculator(): {e}")
        return 0.0


def sequence_calculator(row: pd.Series, char_type: str) -> int:
    # Copyright (C) 2020 Claudio Marques - All Rights Reserved
    # Modified 2023 Chance Tudor
    """Calculates the maximum number of consecutive character sequences."""
    domain = row["domain"]
    try:
        return max(
            map(len, "".join(i if i in char_type else " " for i in domain).split())
        )
    except Exception as e:
        logging.exception(f"Error in sequence_calculator(): {e}")
        return 0


def strange_char_count(row: pd.Series) -> int:
    # Copyright (C) 2020 Claudio Marques - All Rights Reserved
    # Modified 2023 Chance Tudor
    """Returns the number of strange characters, defined as number of characters different from [a-zA-Z]"""
    domain = row["domain"]
    try:
        domain = re.sub(r"[a-zA-Z\.]+", "", domain)
        if len(domain) > 0:
            digits = sum(char.isdigit() for char in domain)
            digits = 0 if digits <= 2 else digits - 2
            domain = re.sub(r"[0-9]+", "", domain)
            return len(domain) + digits
        return 0
    except Exception as e:
        logging.exception(f"Error in strange_char_count(): {e}")
        return 0


def create_dataset(in_file: str) -> pd.DataFrame:
    df = pd.read_csv(in_file)
    df["domain"] = df["domain"].astype(str)
    df["domain_length"] = df["domain"].apply(lambda row: len(row)).astype(int)
    df["strange_char_count"] = df.apply(strange_char_count, axis=1).astype(int)
    df["numeric_sequence"] = df.apply(
        lambda row: sequence_calculator(row, CharDef.NUMERIC.value), axis=1
    ).astype(int)
    df["numeric_ratio"] = df.apply(
        lambda row: ratio_calculator(row, CharDef.NUMERIC.value), axis=1
    ).astype(float)
    df["consonant_ratio"] = df.apply(
        lambda row: ratio_calculator(row, CharDef.CONSONANT.value), axis=1
    ).astype(float)
    df["vowel_ratio"] = df.apply(
        lambda row: ratio_calculator(row, CharDef.VOWEL.value), axis=1
    ).astype(float)
    df["class"] = (
        int(1) if "sus" in in_file else int(0)
    )  # 1 means malicious, 0 means benign

    return df.convert_dtypes()


def create_and_write():
    datasets = [
        FileDef.SANS_HIGH.value,
        FileDef.SANS_MED.value,
        FileDef.SANS_LOW.value,
        FileDef.OISD.value,
        FileDef.CERTPL.value,
        FileDef.AIRVPN.value,
        FileDef.BENIGN.value,
    ]
    for i, dset in enumerate(datasets):
        df = create_dataset(dset).drop_duplicates(subset="domain")
        if i == 0:  # if first dataset
            df.to_csv(
                FileDef.ALL.value, index=False, mode="w", header=True
            )  # write the header
        else:
            df.to_csv(
                FileDef.ALL.value, index=False, mode="a", header=False
            )  # else, don't write the header


def clean(in_file: str, out_file: str):
    df = pd.read_csv(in_file).drop_duplicates(subset="domain")
    df["id"] = np.arange(len(df), dtype=np.int64)
    df.to_csv(out_file, index=False, mode="w", header=True)


create_and_write()
clean(FileDef.ALL.value, FileDef.ALL.value)
