import os
import re
import csv
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils.misc_utils import setup_logger
from data_augmentation.scraper_real import *
from data_augmentation.scraper_satirical import *

# URLs for the news websites to scrape
# Sarcastic websites
THE_ONION_URL = 'https://www.theonion.com/breaking-news'
BIG_AMERICAN_NEWS_URL = 'http://bigamericannews.com/'
EMPIRE_NEWS_URL = 'https://empirenews.net/page/{}/'
NATIONAL_REPORT_URL = 'https://nationalreport.net/'
# Non-sarcastic websites
FOX_NEWS_URL = 'https://www.foxnews.com/'
NY_TIMES_URL = 'https://www.nytimes.com/'
TELEGRAPH_URL = 'https://www.telegraph.co.uk/'
USNEWS_URL = 'https://www.usnews.com/'
ATHLETIC_URL = "https://theathletic.com/uk/"
GUARDIAN_UK_URL = "https://www.theguardian.com/uk-news"
GUARDIAN_US_URL = "https://www.theguardian.com/us-news"

# Directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')

# File names
CSV_FILE_NAME = 'Sarcasm_Headlines_Dataset_v2.csv'
OOS_CSV_FILE_NAME = 'Sarcasm_Headlines_Dataset_OOS.csv'

class Data_augmentation:
    """
    Gets data from the web to augment the dataset.

    Methods:
    -------
    get_titles_from_page()
        Scrape the front page of a news website for article titles.
    get_news_titles()
        Gets the titles of articles from the news websites.
    preprocess_data(data: pd.DataFrame)
        Preprocesses the data.
    save_data(data: pd.DataFrame, file_name: str)
        Saves the data to a CSV file.
    
    Attributes:
    -------
    logger: logging.Logger
        The logger for the class.
    """
    def __init__(self):
        """
        Sets up a logger and creates a class attribute for the logger.
        """
        setup_logger(LOG_DIR)
        logger = logging.getLogger(__name__)
        self.logger = logger

    def get_titles_from_page(self, url: str, getter) -> list[str]:
        """
        Scrape the front page of a news website for article titles.

        Args:
        -------
        self: Data_augmentation
            The object on which the method is called.
        url: str
            The URL of the news website to scrape.
        getter: function
            The function to use to scrape the news website.

        Returns:
        -------
        article_titles: list[str]
            A list of strings representing the titles of articles 
            on the news page of the news website.
        """
        try:
            # If the given url is EMPIRE_NEWS_URL, then we need to scrape multiple pages
            if url == EMPIRE_NEWS_URL:
                # Get the first page of articles and the number of pages of articles
                max_page_num, article_titles = getter(1, EMPIRE_NEWS_URL)

                # Get the titles of articles on every page
                for page_num in range(2, max_page_num + 1):
                    _, page_articles = getter(page_num, EMPIRE_NEWS_URL)
                    article_titles.extend(page_articles)
                    if page_num % 10 == 0:
                        self.logger.info(f'Got {len(article_titles)} articles from {url} - Page {page_num} of {max_page_num}')
                
            else:
                # Connect to the news website and create a BeautifulSoup object from the HTML
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract article titles from the HTML
                article_titles = getter(soup)

            self.logger.info(f'Got {len(article_titles)} articles from {url}')
            return article_titles

        except Exception as e:
            self.logger.exception(f'Error getting news articles from {url}: {e}')
            return []

    def get_news_titles(self) -> pd.DataFrame:
        """
        Calls the functions to scrape the front pages of news websites for article titles.

        Methods:
        -------
        self: Data_augmentation
            The object on which the method is called.

        Returns:
        -------
        titles_df: pd.DataFrame
            A pandas DataFrame containing the article titles, the news website they 
            came from, and their label (whether they are real or satirical).
        """
        # Create a dictionary of news websites and their url, getter, and label
        news_websites_info = {
            'The Onion':{
                'url': THE_ONION_URL,
                'getter': scrape_onion_titles,
                'label': 1
            },
            'Big American News':{
                'url': BIG_AMERICAN_NEWS_URL,
                'getter': scrape_big_american_news_titles,
                'label': 1
            },
            'Empire News':{
                'url': EMPIRE_NEWS_URL,
                'getter': scrape_empire_titles_page_num,
                'label': 1
            },
            'Fox News':{
                'url': FOX_NEWS_URL,
                'getter': scrape_fox_news_titles,
                'label': 0
            },
            'NY Times':{
                'url': NY_TIMES_URL,
                'getter': scrape_ny_times_titles,
                'label': 0
            },
            'Telegraph':{
                'url': TELEGRAPH_URL,
                'getter': scrape_telegraph_titles,
                'label': 0
            },
            'Athletic':{
                'url': ATHLETIC_URL,
                'getter': scrape_athletic_titles,
                'label': 0
            },
            'Guardian':{
                'url': GUARDIAN_UK_URL,
                'getter': scrape_guardian_titles,
                'label': 0
            },
            'Guardian':{
                'url': GUARDIAN_UK_URL,
                'getter': scrape_guardian_titles,
                'label': 0
            }
        }

        # Get the article titles from the web
        website_dfs = []
        for website_name, website_info in news_websites_info.items():
            website_titles = pd.DataFrame({
                'headline': self.get_titles_from_page(url = website_info['url'], getter = website_info['getter']),
                'label': website_info['label'],
                'news_source': website_name
            })
            website_dfs.append(website_titles)
        
        # Concatenate the dataframes
        titles = pd.concat(website_dfs, ignore_index=True)

        return titles

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data for later use in the model.

        Args:
        ----------
        self: Data_augmentation
            The object on which the method is called.
        data: pd.DataFrame
            A pandas DataFrame containing the article titles and their labels.
        
        Returns:
        -------
        data: pd.DataFrame
            A pandas DataFrame containing the article titles and their labels.
        """
        return (data
            # Drop duplicate rows, rows with NaN values, and rows with empty strings
            .loc[data['headline'] != '']
            .drop_duplicates()
            .dropna()
            # Convert numeric characters into empty strings
            .loc[data['headline'].apply(lambda x: re.sub('[0-9]', '', str(x)) is not None)]
            # Drop rows with non-ascii characters
            .loc[data['headline'].apply(lambda x: re.match('^[\x00-\x7F]*$', str(x)) is not None)]
            # Drop rows with length less than 5 or greater than 100
            .loc[data['headline'].apply(lambda x: len(str(x).split()) >= 3 and len(str(x).split()) <= 100)]
            # Drop rows with non-alphanumeric characters
            .loc[data['headline'].apply(lambda x: re.match('^[a-zA-Z0-9 ]*$', str(x)) is not None)]
        )

    def save_data(self, data: pd.DataFrame, file_name: str) -> None:
        """
        Export the data to a CSV file.

        Args:
        -------
        self: Data_augmentation
            The object on which the method is called.
        data: pd.DataFrame
            A pandas DataFrame containing the article titles and their labels.
        file_name: str
            The name of the CSV file to export the data to.

        Returns:
        -------
        None
            The data is exported to a CSV file.
        """
        # Check if the OOS dataset exists
        if os.path.exists(os.path.join(DATA_DIR, file_name)):
            # Load the OOS dataset
            existing_data = pd.read_csv(
                filepath_or_buffer=os.path.join(DATA_DIR, file_name), 
                sep=';', quoting=csv.QUOTE_ALL
            )
            # Append the new data to the existing dataset
            data = pd.concat([existing_data, data], ignore_index=True)
            # Drop duplicate rows
            data.drop_duplicates(inplace=True)
            self.logger.info('Appending new data to existing OOS dataset...')
        else:
            self.logger.info('OOS dataset does not exist. Creating new dataset...')

        # Save the data to a csv file
        data.to_csv(
            path_or_buf=os.path.join(DATA_DIR, file_name), 
            sep=';', quoting=csv.QUOTE_ALL, index=False
        )

        self.logger.info(f'Saved data to {os.path.join(DATA_DIR, file_name)}')