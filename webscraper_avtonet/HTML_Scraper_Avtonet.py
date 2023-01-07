import requests
from bs4 import BeautifulSoup
import csv
import math
from webscraper_avtonet.Scraper_Articles import ArticleList, ArticleInstance
import sys

"""
 File name: HTMLScraperAvtonet.py
 Author: Martin Porenta
 Date: 28.03.2022 
 
 Description: This file contains basic object for retriving html files from Avtonet, and scraping article
 data from recieved HTML files.
 
 Content:
    HTMLScraper_avtonet class (main class for scraping data from Avtonet)
    
 Additional Requirements:
    BeautifulSoup4 installed
    
"""

"""
    HTML Avtonet Motorcycle scraper class 
"""


class HTMLScraper_avtonet:

    # Variables
    _headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.8",
        "upgrade-insecure-requests": "1",
    }

    _oblika_enum = {"sport": "6001", "naked": "6005", "enduro": "6002"}

    _filter_file_path = ""
    _search_filter = []
    _search_url = []

    def __init__(self, filter_file_path):
        """
        Class constructor: Reads search filter to dictionary and Generates
        avtonet search url string

        Inputs:
            filter_file_path: path to scraper filter csv file
        """
        # Read search filter to dictionary
        _filter_file_path = filter_file_path
        try:
            with open(filter_file_path, "r", encoding="UTF8", newline="") as f:
                filter_file_reader = csv.DictReader(f, delimiter=";")
                for i in filter_file_reader:
                    self._search_filter.append(i)
                    self._search_url.append(
                        self._generate_url(i)
                    )  # Generate Avotnet search URL string list
        except:
            print("Failure: opening configuration filter")
            sys.exit()

    def _filter_data(self, articles_list, search_filter):
        """
        Private filter data method: Filters scraped data according to search filter
        Inputs:
            articles_list: list of articles to be filtered
            search_filter: search filter for filtering data
        Return:
            filtered_article
        """
        filtered_articles = ArticleList(articles_list.filter_name)
        for instance in articles_list.list:
            # Filter by model
            if (search_filter["model"].lower()) in instance.name.lower():
                filtered_articles.append_list(instance)
        return filtered_articles

    def scrape_data(self):
        """
        Main public web scraper method: Public mehod to call web scraper
        Inputs: /
        Return:
            result: all scraped data from Avtonet
        """
        result = []
        for i_filter, i_url in zip(self._search_filter, self._search_url):
            current_filter_result = self._scrape_page(i_filter, i_url)

            if current_filter_result != -1:
                result.append(current_filter_result)

        return result

    def _scrape_page(self, search_filter, url):
        """
        Private scrape_page method:
        Mehod retrieves HTML from Avtonet server, parse it with BeutifulSoup library and extract relevant
        data from parsed HTML

        Inputs:
            search_filter: search filter
            url: avonet search url string

        Return:
            filtered_articles
        """

        # Get webpage (base page)
        response = requests.get(url, allow_redirects=False, headers=self._headers)

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        article_divs = soup.find_all(
            "div",
            {"class": "row bg-white position-relative GO-Results-Row GO-Shadow-B"},
        )

        # Check number of found articles
        num_of_articles_str = soup.find(
            "div",
            {"class": "row GO-ResultsMenuBoxnaziv GO-Rounded-T justify-content-center"},
        ).text

        # Extract number of found articles from string
        res = [int(i) for i in num_of_articles_str.split() if i.isdigit()]

        if len(res) > 0:

            num_of_articles = res[0]
            num_per_page = 48
            num_of_pages = math.ceil(num_of_articles / num_per_page)

            # Define list of articles
            articles = ArticleList(search_filter["ime_filtra"])
            # articles_list = []

            # Loop over html divs and parse article data to objects
            instance = 1
            for page in range(1, num_of_pages + 1):
                if page > 1:
                    search_url_second_page = url + str(page)
                    response = requests.get(
                        search_url_second_page, allow_redirects=False, headers=self._headers
                    )
                    # Parse HTML
                    soup = BeautifulSoup(response.text, "html.parser")
                    article_divs = soup.find_all(
                        "div",
                        {
                            "class": "row bg-white position-relative GO-Results-Row GO-Shadow-B"
                        },
                    )

                for div in article_divs:
                    current_article = ArticleInstance()
                    current_article.instance = instance

                    # Parse URL from div
                    a_url = div.find("a", href=True)
                    url_tmp = a_url["href"]
                    current_article.url = url_tmp.replace("..", "https://www.avto.net/")

                    # Get ID from URL
                    current_article.id = url_tmp[
                        url_tmp.find("id=") + 3 : url_tmp.find("&display")
                    ]

                    # Parse name from div
                    div_name = div.find_all(
                        "div",
                        {
                            "class": "GO-Results-Naziv bg-dark px-3 py-2 font-weight-bold text-truncate text-white text-decoration-none"
                        },
                    )
                    span_name = div_name[0].find("span")
                    current_article.name = span_name.text

                    # Parse price from div
                    div_price = div.find("div", {"class": "GO-Results-Price-TXT-Regular"})
                    # currentArticle.price = div_price.text
                    current_article.price = div_price.text.replace("", "").replace(" ", "")

                    # Parse year of make and kilometers from div
                    div_additional_data = div.find(
                        "div", {"class": "col-auto text-truncate py-3 GO-Results-Data"}
                    )
                    # Year of make
                    td_year = div_additional_data.find("td", {"class": "w-75 pl-3"})
                    current_article.year = td_year.text
                    # Kilometers
                    td_kilometers = div_additional_data.find_all("td", {"class": "pl-3"})
                    current_article.kilometers = ""
                    for item in td_kilometers:
                        if len(item["class"]) == 1:
                            current_article.kilometers = item.text
                            break
                    # Save article object to list of articles
                    articles.append_list(current_article)
                    instance += 1

            # Filter  scraped data
            filtered_articles = self._filter_data(articles, search_filter)
            filtered_articles.filter_name = search_filter["ime_filtra"]
            # return articles, filtered_articles
            return filtered_articles

        return -1


    def _generate_url(self, search_filter):
        """
        Private generate_url method:
        Method generates Avtonet search string url

        Inputs:
            search_filter: search filter

        Return:
            generated url string
        """

        return (
            "https://www.avto.net/Ads/results.asp?znamka="
            + search_filter["znamka"]
            + "&model="
            + search_filter["model"]
            + "&modelID="
            + "&tip="
            + "&znamka2="
            + "&model2="
            + "&tip2="
            + "&znamka3="
            + "&model3="
            + "&tip3="
            + "&cenaMin="
            + search_filter["cenaMin"]
            + "&cenaMax="
            + search_filter["cenaMax"]
            + "&letnikMin="
            + search_filter["letnikMin"]
            + "&letnikMax="
            + search_filter["letnikMax"]
            + "&bencin=0"
            "&starost2=999"
            "&oblika="
            + self._oblika_enum[search_filter["oblika"]]
            + "&ccmMin="
            + search_filter["ccmMin"]
            + "&ccmMax="
            + search_filter["ccmMax"]
            + "&mocMin="
            + search_filter["mocMin"]
            + "&mocMax="
            + search_filter["mocMax"]
            + "&kmMin=0"
            + "&kmMax=9999999"
            + "&kwMin=0"
            + "&kwMax=999"
            + "&motortakt=0"
            + "&motorvalji=0"
            + "&lokacija=0"
            + "&sirina="
            + "&dolzina="
            + "&dolzinaMIN="
            + "&dolzinaMAX="
            + "&nosilnostMIN="
            + "&nosilnostMAX="
            + "&lezisc="
            + "&presek="
            + "&premer="
            + "&col="
            + "&vijakov="
            + "&EToznaka="
            + "&vozilo="
            + "&airbag="
            + "&barva="
            + "&barvaint="
            + "&EQ1=1000000000"
            + "&EQ2=1000000000"
            + "&EQ3=1000000000"
            + "&EQ4=100000000"
            + "&EQ5=1000000000"
            + "&EQ6=1000000000"
            + "&EQ7=1110100120"
            + "&EQ8=1010000006"
            + "&EQ9=1000000000"
            + "&KAT=1060000000"
            + "&PIA="
            + "&PIAzero="
            + "&PSLO="
            + "&akcija="
            + "&paketgarancije="
            + "&broker="
            + "&prikazkategorije="
            + "&kategorija=61000"
            + "&ONLvid="
            + "&ONLnak="
            + "&zaloga=10"
            + "&arhiv="
            + "&presort="
            + "&tipsort="
            + "&stran="
        )
