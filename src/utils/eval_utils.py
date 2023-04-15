import matplotlib.pyplot as plt
import seaborn as sns

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
    # Add grid
    sns.set_style("whitegrid")
    # Set figure size
    plt.figure(figsize=(12,8), dpi=200)
    # Plot curves
    plt.plot(epochs, train_curve, color=train_color, linewidth=2, label=f'Training {metric.lower()}')
    plt.plot(epochs, val_curve, color=val_color, linewidth=2, label=f'Validation {metric.lower()}')
    # Set title and labels
    plt.title(f'Training and validation {metric.lower()}', fontsize=20)
    plt.xlabel("Epochs", fontsize=15)
    plt.ylabel(metric.capitalize(), fontsize=15)
    # Remove top and right spines
    sns.despine(left=True, bottom=True)
    # Put the legend outside of the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()
    return