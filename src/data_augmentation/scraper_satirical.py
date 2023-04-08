import requests
from bs4 import BeautifulSoup


def scrape_onion_titles(soup) -> list[str]:
    """
    Scrape the front page of theonion.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of theonion.com.
    """
    # Extract article titles from the HTML
    article_title_links = soup.find_all('a', class_='sc-1out364-0 dPMosf sc-1pw4fyi-5 hQxRDX js_link')
    article_titles = [link.get('title') for link in article_title_links]

    # Create a DataFrame from the article titles with a column for the label and another one for the source
    return article_titles

def scrape_big_american_news_titles(soup) -> list[str]:
    """
    Scrape the front page of bigamericannews.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of bigamericannews.com.
    """
    # Extract article titles from the HTML
    article_titles = soup.find_all('h3', class_='entry-title')
    article_titles = [title.text for title in article_titles]

    # Create a DataFrame from the article titles with a column for the label and another one for the source
    return article_titles

def scrape_empire_titles_page_num(page_num: int, url: str) -> tuple[int, list[str]]:
    """
    Scrape page page_num of empirenews.net's index for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of cap-news.com.
    """
    assert page_num > 0, 'Page number must be greater than 0'

    # Connect to cap-news.com and create a BeautifulSoup object from the HTML
    url = url.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    # Get every hyperlink on the page
    links = soup.find_all('a')
    # Filter out links that don't lead to articles
    article_links = [link for link in links if link.get('href').startswith('https://empirenews.net/')]

    # Get the number of pages of articles
    max_page_num = 0
    if page_num == 1:
        page_links = [link for link in links if link.get('href').startswith('https://empirenews.net/page/')]
        max_page_num = max([int(link.get('href').split('/')[-2]) for link in page_links])
        
    # Extract article titles from the HTML
    article_titles = [link.text for link in article_links]
    
    return max_page_num, article_titles

def scrape_national_report_titles(soup) -> list[str]:
    """
    Scrape the front page of cap-news.com for article titles.

    Returns:
    -------
    article_titles: list[str]
        A list of strings representing the titles of articles 
        on the news page of cap-news.com.
    """

    links = soup.find_all('a')
    # Filter out links that don't lead to articles
    article_links = [link for link in links if link.get('href').startswith('https://nationalreport.net/')]

    # Extract article titles from the HTML
    article_titles = [link.text for link in article_links]
    
    return article_titles