import os

import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit


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


