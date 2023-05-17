import os
import re
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
    train_sequences = tokenizer.texts_to_sequences(X_train[col])
    test_sequences = tokenizer.texts_to_sequences(X_test[col])

    # Get lenght of the longest sequence
    max_seq_len = max([len(seq) for seq in train_sequences])
    # Get vocabulary size
    vocab_size = len(tokenizer.word_index) + 1
    
    # Applying padding to both train and test sets
    train_padded = pad_sequences(train_sequences, maxlen=max_seq_len, padding="post")
    test_padded = pad_sequences(test_sequences, maxlen=max_seq_len, padding="post")

    return train_padded, test_padded, max_seq_len, vocab_size, tokenizer

def preprocess_text(text, contractions, stop_words, lemmatizer):
    """
    Preprocesses a text.

    Args:
    -------
    text: str
        Text to preprocess.
    contractions: pandas.DataFrame
        DataFrame containing contractions.
    stopwords: list
        List of stopwords.
    lemmatizer: nltk.stem.WordNetLemmatizer
        Lemmatizer.
    language: str, optional
        Language of the text. Defaults to "english".
    
    Returns:
    -------
    text: str
        The preprocessed text.
    """
    # Convert to lowercase
    text = text.lower()
    # Expand contractions
    text = " ".join(
        [contractions[contractions["contraction"] == word]["expanded"].values[0]
            if word in contractions["contraction"].values
            else word for word in text.split()])
    # Remove non-alphanumeric characters
    text = re.sub(r'[^\w\s]', '', text)
    # Remove digits
    text = re.sub(r'\d', '', text)
    # Remove stop words
    text = " ".join([word for word in text.split() if word not in stop_words])
    # Lemmatize words
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

def filter_words_by_frequency(text, word_freq, threshold=3):
    """
    Given a text and a dictionary with the frequency of each word,
    return a text with the words with frequency less than 3 removed.

    Parameters
    ----------
    text : str
        Text to be filtered.
    word_freq : dict
        Dictionary with the frequency of each word.
    
    Returns
    -------
    str
        Text with the words with frequency less than 3 removed.
    """
    words = text.split()
    filtered_words = [word for word in words if word_freq.get(word, 0) > threshold]
    return " ".join(filtered_words)

def load_glove_embeddings(path_to_glove_file: str) -> dict:
    """
    Loads GloVe embeddings.

    Args:
    -------
    path_to_glove_file: str
        Path to the GloVe embeddings file.

    Returns:
    -------
    embeddings_index: dict
        Dictionary where each key is a word and each value is the corresponding embedding.
    """
    embeddings_index = {}
    with open(path_to_glove_file, encoding="utf8") as f:
        for line in f:
            word, coefs = line.split(maxsplit=1)
            coefs = np.fromstring(coefs, "f", sep=" ")
            embeddings_index[word] = coefs

    return embeddings_index

def create_embedding_matrix(embeddings_index: dict, tokenizer: keras.preprocessing.text.Tokenizer, num_tokens: int, embedding_dim: int) -> tuple[np.ndarray, int, int]:
    """
    Creates an embedding matrix.

    Args:
    -------
    embeddings_index: dict
        Dictionary where each key is a word and each value is the corresponding embedding.
    tokenizer: keras.preprocessing.text.Tokenizer
        Tokenizer to use.
    num_tokens: int
        Number of tokens.
    embedding_dim: int
        Dimension of the embeddings.

    Returns:
    -------
    embedding_matrix: np.array
        Embedding matrix.
    hits: int
        Number of words in the vocabulary that are also in the embeddings.
    misses: int
        Number of words in the vocabulary that are not in the embeddings.
    """
    # Initialize hits and misses to 0
    # i) hits: number of words in the vocabulary that are also in the embeddings
    # ii) misses: number of words in the vocabulary that are not in the embeddings
    hits = 0
    misses = 0
    # Prepare embedding matrix
    embedding_matrix = np.zeros((num_tokens, embedding_dim))
    for word, i in tokenizer.word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # Words not found in embedding index will be all-zeros.
            # This includes the representation for "padding" and "OOV"
            embedding_matrix[i] = embedding_vector
            hits += 1
        else:
            misses += 1

    return embedding_matrix, hits, misses