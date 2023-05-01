import pandas as pd
from constants import *
from sklearn.model_selection import train_test_split


def read_data(file_path):
    return pd.read_csv(file_path)


def split_data(data):
    positive_data = data[data["class"] == 1]
    negative_data = data[data["class"] == 0]

    # Split positive data
    pos_train_val, pos_test = train_test_split(
        positive_data, test_size=0.2, random_state=42, stratify=positive_data["class"]
    )
    pos_train, pos_val = train_test_split(
        pos_train_val, test_size=0.2, random_state=42, stratify=pos_train_val["class"]
    )

    # Split negative data
    neg_train_val, neg_test = train_test_split(
        negative_data, test_size=0.1, random_state=42, stratify=negative_data["class"]
    )
    neg_train, neg_val = train_test_split(
        neg_train_val, test_size=0.1, random_state=42, stratify=neg_train_val["class"]
    )

    # Training dataset
    train = pd.concat([pos_train, neg_train])
    # Validation dataset
    val = pd.concat([pos_val, neg_val])
    # Test dataset
    test = pd.concat([pos_test, neg_test])

    # Shuffle to ensure randomness
    train = train.sample(frac=1, random_state=42).reset_index(drop=True)
    val = val.sample(frac=1, random_state=42).reset_index(drop=True)
    test = test.sample(frac=1, random_state=42).reset_index(drop=True)

    assert train["domain"].nunique() == len(train)
    assert val["domain"].nunique() == len(val)
    assert test["domain"].nunique() == len(test)

    return train, val, test


def save_data(train, val, test, path="data/"):
    train.to_csv(path + "train.csv", index=False)
    val.to_csv(path + "val.csv", index=False)
    test.to_csv(path + "test.csv", index=False)


def split_and_save_data(file_path, data_dir="data/"):
    data = read_data(file_path)
    train, val, test = split_data(data)
    save_data(train, val, test, path=data_dir)


split_and_save_data(FileDef.ALL.value, data_dir="data/")
