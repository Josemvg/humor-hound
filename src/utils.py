import os
import re
import json
import matplotlib.pyplot as plt
import seaborn as sns

def load_json(file_path: str):
    """
    Loads a JSON file.

    Args:
    -------
    file_path: str
        Path to the JSON file.
    
    Returns:
    -------
    generator
    """
    for l in open(file_path, "r"):
        yield json.loads(l)


def plot_metric_curves(epochs, train_curve, val_curve, train_color, val_color, metric):
    """
    Plots the training and validation curves for a specific metric.

    Args:
    -------
    epochs: list
        List of epochs.
    train_curve: list
        List of training metric values.
    val_curve: list
        List of validation metric values.
    train_color: str
        Color of the training curve.
    val_color: str
        Color of the validation curve.
    metric: str
        Metric to plot.
    
    Returns:
    -------
    None
    """
    sns.set_theme()
    plt.figure(figsize=(15,10), dpi=200)
    plt.plot(epochs, train_curve, color=train_color, linewidth=2, label=f'Training {metric.lower()}')
    plt.plot(epochs, val_curve, color=val_color, linewidth=2, label=f'Validation {metric.lower()}')
    plt.title(f'Training and validation {metric.lower()}', fontsize=20)
    plt.xlabel("Epochs", fontsize=15)
    plt.ylabel(metric.capitalize(), fontsize=15)
    plt.legend(frameon=False, fontsize=15)
    plt.show()
    return

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