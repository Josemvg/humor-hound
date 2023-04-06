import os
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