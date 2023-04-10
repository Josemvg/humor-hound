import re
import html
import unicodedata
from typing import Callable

def scrape_fox_news_titles(soup) -> list[str]:
    """
    Scrape the front page of cap-news.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of cap-news.com.
    """
    # Get every img on the page
    imgs = soup.find_all('img')
    # Get the alt text for each image
    article_titles = [img.get('alt') for img in imgs]
    # Decode the HTML entities in the article titles
    article_titles = [html.unescape(title) for title in article_titles]
    # Remove special characters and text between parentheses and brackets
    article_titles = [
        re.sub(r'\([^)]*\)|\[[^)]*\]', '', unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode())
        for title in article_titles
        # Remove disclaimer and articles with a '-' in the title
        if 'DO NOT USE ON FNC/FBN DIGITAL EDITORIAL. ONLY FOR CREDIBLE CONTENT' not in title and '-' not in title
    ]

    return article_titles

def scrape_ny_times_titles(soup) -> list[str]:
    """
    Scrape the front page of nytimes.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of nytimes.com.
    """
    # Define the words that should be excluded from the article titles
    excluded_words = ('review', 'weekly', ':')
    
    # Extract article titles from the HTML
    article_title_headlines = soup.find_all('h3')
    
    article_titles = [
        title.text for title in article_title_headlines 
        if not any(words in title.text.lower() for words in excluded_words)
    ]
    
    return article_titles

def scrape_telegraph_titles(soup) -> list[str]:
    """
    Scrape the front page of cnn.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of cnn.com.
    """
    # Define the words that should be excluded from the article titles
    excluded_words = ('the best', 'how', ':')
    # Get every headline on the page
    article_title_headlines = soup.find_all('span', class_='list-headline__text')
    # Extract article titles from the HTML
    article_titles = [
        title.text.replace('\n', '') for title in article_title_headlines
        if not any(words in title.text.lower() for words in excluded_words)
    ]
    
    return article_titles

def scrape_bbc_titles(soup) -> list[str]:
    """
    Scrape the front page of BBC.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of BBC.com.
    """
    # Get every headline on the page
    article_title_headlines = soup.find_all('a', class_='media__link')
    # Extract article titles from the HTML
    article_titles = [title.text.strip().replace('\n', '') for title in article_title_headlines]
    
    return article_titles

def scrape_forbes_titles(soup) -> list[str]:
    """
    Scrape the front page of forbes.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of BBC.com.
    """
    # Get every headline on the page
    article_title_headlines = soup.find_all('span')
    # Extract article titles from the HTML
    article_titles = [title.text.strip().replace('\n', '') for title in article_title_headlines]  

    return article_titles

def scrape_athletic_titles(soup) -> list[str]:
    """
    Scrape the front page of forbes.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of The Athletic.
    """
    # Get every headline on the page
    article_title_headlines = soup.find_all('p', class_="sc-30702b06-0 tfWzM")
    # Extract article titles from the HTML
    article_titles = [title.text.strip().replace('\n', '') for title in article_title_headlines]

    return article_titles

def scrape_guardian_titles(soup) -> list[str]:
    """
    Scrape the front page of forbes.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of The Guardian.
    """
    # Get every headline on the page
    article_title_headlines = soup.find_all('a', attrs={"data-link-name": "article"})
    # Extract article titles from the HTML
    article_titles = [title.text.strip().replace('\n', '') for title in article_title_headlines]

    return article_titles

def run_scraper(url: str, scraper: Callable) -> list[str]:
    """
    Runs specified scraper on URL for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the specified.
    """
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'lxml')

    article_titles = scraper(soup=soup)

    return article_titles

if __name__=='__main__':
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    import numpy as np
    url = "https://www.forbes.com/ceo-network/?sh=45537f4a7813"
    forbes_article_titles = run_scraper(url=url, scraper=scrape_forbes_titles)
    labels = np.ones(shape=len(forbes_article_titles), dtype=int)

    # save to file
    fobes_df = pd.DataFrame({"headlines": forbes_article_titles,
                           "label": labels})
    
    fobes_df.to_csv('forbes_real.csv', sep=';')
