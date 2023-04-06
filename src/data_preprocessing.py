import os

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences


def train_test_split(df: pd.DataFrame, target: str, test_size: float = 0.2, random_state: int = 2023):
    """
    Splits a dataframe into train and test sets.

    Args:
    -------
    df: pd.DataFrame
        Dataframe to split.
    target: str
        Name of the target column.
    test_size: float
        Proportion of the dataset to include in the test split.
    random_state: int
        Seed for the random number generator.

    Returns:
    -------
    df_tr: pd.DataFrame
        Train dataframe.
    df_ts: pd.DataFrame
        Test dataframe.
    """
    # Create train and test sets
    split = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    for train_index, test_index in split.split(df, df[target]):
        df_tr = df.loc[train_index]
        df_ts = df.loc[test_index]
    
    # Create X and y for both train and test sets
    X_train = df_tr.drop(target, axis=1)
    y_train = df_tr[target]
    X_test = df_ts.drop(target, axis=1)
    y_test = df_ts[target]

    return X_train, y_train, X_test, y_test


def tokenization(tokenizer: keras.preprocessing.text.Tokenizer, X_train: pd.Series, X_test: pd.Series, col: str) -> tuple[np.ndarray, np.ndarray, int, int]:
    """
    Tokenizes a column of a dataframe by applying: tokenization, sequencing and padding. 

    Args:
    -------
    tokenizer: keras.preprocessing.text.Tokenizer
        Tokenizer to use.
    X_train: pd.Series
        Train dataframe.
    X_test: pd.Series
        Test dataframe.
    col: str
        Name of the column to tokenize.

    Returns:
    -------
    train_padded: np.array
        Padded train sequences.
    test_padded: np.array
        Padded test sequences.
    max_seq_len: int
        Length of the longest sequence.
    vocab_size: int
        Size of the vocabulary.
    """
    # Fit tokenizer on train set
    tokenizer.fit_on_texts(X_train[col])

    # Conver text to sequences for both train and test sets
    train_sequences = tokenizer.texts_to_sequences(X_train["headline"])
    test_sequences = tokenizer.texts_to_sequences(X_test["headline"])

    # Get lenght of the longest sequence
    max_seq_len = max([len(seq) for seq in train_sequences])
    # Get vocabulary size
    vocab_size = len(tokenizer.word_index) + 1
    
    # Applying padding to both train and test sets
    train_padded = pad_sequences(train_sequences, maxlen=max_seq_len, padding="post")
    test_padded = pad_sequences(test_sequences, maxlen=max_seq_len, padding="post")

    return train_padded, test_padded, max_seq_len, vocab_size