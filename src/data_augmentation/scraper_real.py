import re
import html
import unicodedata

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
    # Define the words that should be excluded from the article titles
    excluded_words = ('...','?')
    # Get every headline on the page
    article_title_headlines = soup.find_all('a', class_='media__link')
    # Extract article titles from the HTML
    article_titles = [
        title.text.strip().replace('\n', '') for title in article_title_headlines
        if not any(words in title.text.lower() for words in excluded_words)
    ]
    
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
    # Define translation table
    excluded_words = ('subscribe', 'newsletters')
    translation_table = str.maketrans({
        '\n': '', 
        '"': '',
        '’': '\'',
    })
    # Get every headline on the page
    article_title_headlines = soup.find_all('span')
    # Extract article titles from the HTML
    article_titles = [
        title.text.strip().translate(translation_table) for title in article_title_headlines
        if not any(words in title.text.lower() for words in excluded_words)                  
    ]

    return article_titles

def scrape_athletic_titles(soup) -> list[str]:
<<<<<<< HEAD
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
=======
>>>>>>> 9e398eb5817aedb23bf31d84f4e402fe546b9a38
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