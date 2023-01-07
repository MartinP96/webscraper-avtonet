from datetime import datetime
import csv

'''
 File name: ScraperArticles.py
 Author: Martin Porenta
 Date: 28.03.2022 

 Description: This file contains basic objects for scraped articles and scraped articles list.

 Content:
    ArticleInstance class (ArticleInstance class that is scraped from HTML file)
    ArticleList class (List class of all found class on HTML file)

 Additional Requirements:
    /
'''

'''
    Article instance class - defines properties of found articles on Avtonet.
'''

class ArticleInstance:

    def __init__(self):
        """
            Class constructor: Set date and time uppon class creation

            Inputs:
                /
        """
        self.time_stamp = datetime.now()

        self.instance = 0
        self.name = ""
        self.price = ""
        self.year = ""
        self.kilometers = ""
        self.url = ""
        self.id = ""
        self.time_stamp = ""
        self.test = ""

    def print_article(self):
        """
            Public print_article method: Prints Article object attributes to console (NOT USED)
            Inputs:
                /
            Return:
                /
        """
        print(" ")
        print("Name:" + self.name)
        print("Price:" + self.price)
        print("Year:" + self.year)
        print("Kilometers:" + self.kilometers)
        print("Url:" + self.url)
        print(" ")

    def generate_report_string(self):
        """
            Public generate_report_string method: Generate report string (NOT USED)
            Inputs:
                /
            Return:
                report_string: report string of article attributes
        """
        report_string = f"{self.instance}:\n Ime: {self.name} \n Letnik: {self.year} \n Cena: {self.price} " \
              f"\n Kilometri: {self.kilometers} \n" \
              f" Url: {self.url}\n" \
              f" Id: {self.id} \n----------------------------\n"
        return report_string

    def generate_csv_row(self):
        """
            Public generate_csv_row method: generates csv row from object attributes
            Inputs:
                /
            Return:
                report_string: csv_row
        """
        return [self.name, self.price, self.year, self.kilometers, self.id, self.url]

    def read_csv_row(self, csv_row):
        """
            Public read_csv_row method: reads object attributes from csv row
            Inputs:
                csv_rows: input csv rows to be parsed into Article object attributes
            Return:
                /
        """
        self.name = csv_row[0]
        self.price = csv_row[1]
        self.year = csv_row[2]
        self.kilometers = csv_row[3]
        self.url = csv_row[5]
        self.id = csv_row[4]

class ArticleList:

    def __init__(self, filter_name=""):
        """
            Class constructor:

            Inputs:
                filter_name (defulat value = ""): Name of article_list, used for in
                creating output result folder structure
        """
        self.time_stamp = datetime.now()
        self.list = []
        self.filter_name = filter_name
        self.num_of_articles = 0
        self.time_stamp = None
        self.filter_name = ""

    def assign_list(self, input_list):
        """
            Public asign list method: Assings list of Articles to ArticleList object
            Inputs:
                input_list: list of articles
            Return:
                /
        """
        self.list = input_list.copy()
        self.num_of_articles = len(self.list)
        self.time_stamp = datetime.now()

    def append_list(self, list_element):
        """
            Public append list  method: Append new Article object to ArticleList
            Inputs:
                list_element: input article object
            Return:
                /
        """
        self.list.append(list_element)
        self.num_of_articles += 1

    def return_list(self):
        """
            Public return_list list  method: Return copy of list of Article objects
            Inputs:
                /
            Return:
                return_list: list of Article objecst
        """
        return_list = self.list.copy()
        return return_list

    def read_csv(self, path):
        """
            Public read_csv method: Reads articles from csv file and stores it to list
            Inputs:
                path: path to input csv file
            Return:
                /
        """

        # Load old article list and compare with new article list
        tmp = []
        with open(path, 'r', encoding='UTF8', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            for i in reader:
                article_i = ArticleInstance()
                article_i.read_csv_row(i)
                tmp.append(article_i)
        self.list = tmp.copy()
        self.num_of_articles = len(self.list)

    def write_csv(self, path):
        """
            Public write_csv method: Writes whole list of Articles to output csv file
            Inputs:
                path: path to output csv file
            Return:
                /
        """

        with open(path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for i in self.list:
                writer.writerow(i.generate_csv_row())
