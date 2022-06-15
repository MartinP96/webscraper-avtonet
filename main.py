"""
 File name: main.py
 Author: Martin Porenta
 Date: 28.03.2022

 Description: This file contains main program for webscraper

 Content:
 Additional Requirements:
    HTMLScraper_avtonet class
    WebBot class

"""

import WebBot

if __name__ == '__main__':

    scraper_filter_path = "configuration/avtonet_search_filter.csv"
    scraper_output_path = "output/"
    bot1 = WebBot.WebBot(scraper_filter_path, scraper_output_path)
    bot1.run()

