"""
 File name: WebBot.py
 Author: Martin Porenta
 Date: 28.03.2022

 Description: This file contains WebBot class

 Content:
 Additional Requirements:
    HTMLScraper_avtonet class

"""

from webscraper_avtonet.HTML_Scraper_Avtonet import HTMLScraper_avtonet
from webscraper_avtonet.HTML_Scraper_Avtonet import ArticleList
from datetime import datetime
import os

"""
    Main WebBot Class
"""
class WebBot:

    def __init__(self, scraper_filter_path, scraper_output_path):
        """
            Class constructor: Declares HTMLScraper object

            Inputs:
                scraper_filter_path: path to scraper filter csv file
                scraper_output_path: path to scraper output result folder
        """
        self._scraper = HTMLScraper_avtonet(scraper_filter_path)
        self._scraper_output_path = scraper_output_path
        self._scraper_output_path: str
        self._scraper = None
        self._current_articles = None

    def run(self):
        """
            Main WebBot public method
            Inputs: /
            Return: /
        """
        self._retrieve_data()

    def _retrieve_data(self):
        """
            Retrieve data private method:
            Method starts HTMLWebscraper, compares new scraped data to
            old data and stores it to output folders

            Inputs: /
            Return: /
        """
        print(f"WebBot retrieving data [{datetime.now()}]:")
        scraped_data = self._scraper.scrape_data()
        self._current_articles = scraped_data
        self._save_data(scraped_data)

    def _save_data(self, scraped_data):
        """
            Save data private method:
            Method saved scraped data to output folders. If output folder do not exist,
            method create output result folder structure, according to search_filter csv file.

            Inputs: scraped data
            Return: /
        """
        for data in scraped_data:
            output_folder_path = f'{self._scraper_output_path}/{data.filter_name}'
            if not os.path.isdir(output_folder_path):
                os.mkdir(output_folder_path)

            if os.path.exists(output_folder_path + "/new_articles.csv"):
                os.remove(output_folder_path + "/new_articles.csv")

            # Compare data with new and old data
            if os.path.exists(output_folder_path + "/found_articles.csv"):
                new_articles = self._compare_data(output_folder_path + "/found_articles.csv", data)
                if new_articles.num_of_articles > 0:
                    new_articles.write_csv(output_folder_path + "/new_articles.csv")
            data.write_csv(f'{self._scraper_output_path}/{data.filter_name}/found_articles.csv')

    def _compare_data(self, old_articles_path, current_articles):
        """
            Compare data private method:
            Method compares current scraped articles to old articles stored in output folders and return new
            articles.

            Inputs: old_articles_path, current_articles list object
            Return: new articles
        """
        # Read old articles
        old_articles = ArticleList()
        old_articles.read_csv(old_articles_path)

        new_articles = ArticleList()
        for current in current_articles.list:
            num_of_matches = 0
            for old in old_articles.list:
                if old.id == current.id:
                    num_of_matches += 1

                # If number of matches 0, we found new article
            if num_of_matches == 0:
                new_articles.append_list(current)

        print(f"Found {new_articles.num_of_articles} new articles. \nRetriveing data done.\n")
        return new_articles
