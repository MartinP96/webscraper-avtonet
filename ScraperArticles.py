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

    instance = 0
    name : str
    price : str
    year = ""
    kilometers = ""
    url = ""
    id = ""
    time_stamp = ""
    test = ""

    """
        Class constructor: Set date and time uppon class creation

        Inputs:
            /
    """
    def __init__(self):
        self.time_stamp = datetime.now()

    """
        Public print_article method: Prints Article object attributes to console (NOT USED)
        Inputs: 
            /
        Return: 
            /
    """
    def print_article(self):
        print(" ")
        print("Name:" + self.name)
        print("Price:" + self.price)
        print("Year:" + self.year)
        print("Kilometers:" + self.kilometers)
        print("Url:" + self.url)
        print(" ")

    """
        Public generate_report_string method: Generate report string (NOT USED)
        Inputs: 
            /
        Return: 
            report_string: report string of article attributes
    """
    def generate_report_string(self):
        report_string = f"{self.instance}:\n Ime: {self.name} \n Letnik: {self.year} \n Cena: {self.price} " \
              f"\n Kilometri: {self.kilometers} \n" \
              f" Url: {self.url}\n" \
              f" Id: {self.id} \n----------------------------\n"
        return report_string

    """
        Public generate_csv_row method: generates csv row from object attributes
        Inputs: 
            /
        Return: 
            report_string: csv_row
    """
    def generate_csv_row(self):
        return [self.name, self.price, self.year, self.kilometers, self.id, self.url]

    """
        Public read_csv_row method: reads object attributes from csv row
        Inputs: 
            csv_rows: input csv rows to be parsed into Article object attributes
        Return: 
            /
    """
    def read_csv_row(self, csv_row):
        self.name = csv_row[0]
        self.price = csv_row[1]
        self.year = csv_row[2]
        self.kilometers = csv_row[3]
        self.url = csv_row[5]
        self.id = csv_row[4]

'''
    Article list class - contains list of all found articles
'''
class ArticleList:

    # Variables
    num_of_articles = 0
    list = None
    time_stamp = None
    filter_name = ""

    """
        Class constructor: 

        Inputs:
            filter_name (defulat value = ""): Name of article_list, used for in 
            creating output result folder structure
    """
    def __init__(self, filter_name=""):
        self.time_stamp = datetime.now()
        self.list = []
        self.filter_name = filter_name

    """
        Public asign list method: Assings list of Articles to ArticleList object
        Inputs: 
            input_list: list of articles 
        Return: 
            /
    """
    def assign_list(self, input_list):
        self.list = input_list.copy()
        self.num_of_articles = len(self.list)
        self.time_stamp = datetime.now()

    """
        Public append list  method: Append new Article object to ArticleList
        Inputs: 
            list_element: input article object
        Return: 
            /
    """
    def append_list(self, list_element):
        self.list.append(list_element)
        self.num_of_articles += 1

    """
        Public return_list list  method: Return copy of list of Article objects
        Inputs: 
            /
        Return: 
            return_list: list of Article objecst
    """
    def return_list(self):
        return_list = self.list.copy()
        return return_list

    """
        Public read_csv method: Reads articles from csv file and stores it to list
        Inputs: 
            path: path to input csv file
        Return: 
            /
    """
    def read_csv(self, path):
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

    """
        Public write_csv method: Writes whole list of Articles to output csv file
        Inputs: 
            path: path to outptu csv file
        Return: 
            /
    """
    def write_csv(self, path):
        with open(path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for i in self.list:
                writer.writerow(i.generate_csv_row())
