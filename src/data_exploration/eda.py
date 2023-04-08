import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import plotly.express as px
import pandas as pd

def check_class_imbalance(data: pd.DataFrame, col: str) -> None:
    """
    Checks the class imbalance in a pandas DataFrame column.

    Args:
    -------
    data: pd.DataFrame
        Dataframe to process.
    col: str
        Name of the column to process.
    
    Returns:
    -------
    pd.DataFrame:
        Dataframe with the absolute and relative frequencies of each class.
    """
    return (data
        .groupby(by=col)
        # Get the absolute frequencies
        .agg(Freq=(col, "count"))
        # Compute the relative frequencies
        .assign(Rel_Freq = lambda x: x["Freq"] / x["Freq"].sum())
        # Reset the index and sort by label
        .reset_index()
        .sort_values(by=col)
    )

def get_word_counts(data: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Gets the number of occurrences of every word in a 
    pandas DataFrame column containing text.

    Args:
    -------
    data: pd.DataFrame
        Dataframe to process.
    col: str
        Name of the column to process.
    
    Returns:
    -------
    word_count: pd.DataFrame
        Dataframe with the number of occurrences of every word.
    """
    # Get the number of occurrences of every word in the dataset
    word_count = pd.Series(" ".join(data[col]).split()).value_counts()
    # Convert into a DataFrame
    word_count = pd.DataFrame(word_count).reset_index()
    # Rename columns
    word_count.columns = ["word", "frequency"]

    return word_count

def plot_top_n_words_frequency(word_counts: pd.DataFrame, word_col:str, freq_col:str, top_n: int, palette = "YlOrRd_r") -> None:
    """
    Plots the frequency distribution of the n most common words in the dataset.

    Args:
    -------
    word_counts: pd.DataFrame
        Dataframe with the number of occurrences of every word.
    word_col: str
        Name of the word column.
    freq_col: str
        Name of the frequency column.
    top_n: int
        Number of most common words to plot.
    palette: str
        Color palette to use.
    
    Returns:
    -------
    None
        The function plots the frequency distribution of the n most common words in the dataset.
    """
    # Plot the frequency distribution of the n most common words in the dataset
    plt.figure(figsize=(10,5), dpi=120)
    sns.barplot(data=word_counts.head(top_n), x=word_col, y=freq_col, palette=palette)
    plt.title(f'Frequency distribution of the {top_n} most common words', fontsize=18)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks(rotation=90)
    # Despine the plot
    sns.despine(left=True, bottom=True)
    plt.show()
    return

def plot_word_frequency_distribution(word_counts: pd.DataFrame, freq_col:str, color = "#791100") -> None:
    """
    Plots the frequency distribution of every word in the dataset.

    Args:
    -------
    word_counts: pd.DataFrame
        Dataframe with the number of occurrences of every word.
    freq_col: str
        Name of the frequency column.
    color: str
        Color to use.

    Returns:
    -------
    None
    """
    # Plot the frequency distribution of every word in the dataset
    plt.figure(figsize=(10, 5), dpi=120)
    sns.histplot(data=word_counts, x=freq_col, bins=100, kde=True, color=color)
    plt.title("Frequency distribution of every word", fontsize=18)
    plt.xlabel("Frequency", fontsize=14)
    plt.ylabel("Number of words", fontsize=14)
    # Despine the plot
    sns.despine(left=True, bottom=True)
    # Remove the background color
    plt.gca().set_facecolor("white")
    plt.show()

def plot_word_frequency_distribution_n_occurrences(word_counts: pd.DataFrame, freq_col:str, n: int, color = "#791100") -> None:
    """
    Plots the frequency distribution of every word in the dataset
    with less than n occurrences.

    Args:
    -------
    word_counts: pd.DataFrame
        Dataframe with the number of occurrences of every word.
    freq_col: str
        Name of the frequency column.
    n: int
        Number of occurrences.
    color: str
        Color to use.
    
    Returns:
    -------
    None
    """
    # Plot the frequency distribution of the words with less than 100 occurrences
    plt.figure(figsize=(10, 5), dpi=120)
    sns.histplot(data=word_counts[word_counts[freq_col] <= n], x=freq_col, bins=50, kde=True, color=color)
    plt.title(f"Frequency distribution of the words with less than {n} occurrences", fontsize=18)
    plt.xlabel("Frequency", fontsize=14)
    plt.ylabel("Number of words", fontsize=14)
    # Despine the plot
    sns.despine(left=True, bottom=True)
    # Remove the background color
    plt.gca().set_facecolor("white")
    plt.show()
    return

def plot_headline_length_distribution(data: pd.DataFrame(), text_col: str, label: str) -> None:
    """
    Plots a histogram of the headline length distribution.

    Args:
    -------
    data: pd.DataFrame
        Dataframe to plot.
    text_col: str
        Name of the column to plot.
    label: str
        Name of the label column.
    
    Returns:
    -------
    None
        The function plots a histogram of the headline length distribution.
    """
    # Plot the histogram of the headline length distribution
    fig = px.histogram(
        data, 
        x=text_col,
        height=700, 
        color=label, 
        title="Headlines Length Distribution", 
        marginal="box"
    )
    fig.show()
    return 

def plot_wordcloud(data: pd.DataFrame(), col: str) -> None:
    """
    Plots a wordcloud from a pandas DataFrame column.

    Args:
    -------
    data: pd.DataFrame
        Dataframe to plot.
    col: str
        Name of the column to plot.
    
    Returns:
    -------
    None
        The function plots a wordcloud.
    """
    # Join all the text together
    all_text = " ".join([i for i in data[col]])
    # Print the total number of words
    print(f"Total number of words: {len(all_text)}")

    # Set the wordcloud parameters
    wc = WordCloud(
        background_color="white",
        width=1600,
        height=900,
        max_words=300, 
        contour_width=3, 
        contour_color='steelblue'
    )
    # Generate the wordcloud from the text
    wc.generate(all_text)

    # Plot the wordcloud
    plt.figure(figsize=(15, 8), facecolor='k')
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    return

def plot_wordcloud_by_label(data: pd.DataFrame(), text_col: str, label: str) -> None:
    """
    Plots a wordcloud for each label in a pandas DataFrame column.

    Args:
    -------
    data: pd.DataFrame
        Dataframe to plot.
    text_col: str
        Name of the column to plot.
    label: str
        Name of the label column.
    
    Returns:
    -------
    None
        The function plots a wordcloud for each label.
    """
    label_values = data[label].unique()
    # Create a vertical subfigure plot with len(label_values) rows and 1 column
    fig, axes = plt.subplots(len(label_values), 1, figsize=(15, 8*len(label_values)), facecolor='k')
    # Loop through the label values
    for i, label_value in enumerate(label_values):
        # Join all the text together
        all_text = " ".join([i for i in data[data[label] == label_value][text_col]])
        # Print the total number of words
        print(f"Total number of words for {label_value}: {len(all_text)}")
        # Set the wordcloud parameters
        wc = WordCloud(
            background_color="white",
            width=1600,
            height=900,
            max_words=300, 
            contour_width=3, 
            contour_color='steelblue'
        )
        # Generate the wordcloud from the text
        wc.generate(all_text)
        # Plot the wordcloud
        axes[i].imshow(wc)
        axes[i].axis("off")
        axes[i].set_title(f'Wordcloud for class {label_value}', fontsize=20)

    plt.show()
    return
