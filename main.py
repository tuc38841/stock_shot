#“Data provided by IEX Cloud”
#<a href="https://iexcloud.io">Data provided by IEX Cloud</a>

import pandas as pd
from matplotlib import pyplot as plt
import requests
import json
from charts import get_price

base_url = "https://sandbox.iexapis.com/stable/stock/"
token = "?token=Tpk_b0410fc3685c4561980063dfcb5279a7"

class Stock_shot:
    def __init__(self, stock):
        self.stock = stock

    # Returns Company, open and close values, latest price
    def get_quote(self, stock):
        response = requests.get(base_url + stock + '/quote' + token)
        response_json = json.loads(response.text)
        print(response_json)

    # Returns list of tickers of similar companies (note changes in response)
    def get_peers(self, stock):
        response = requests.get(base_url + stock + '/peers' + token)
        response_json = json.loads(response.text)
        print(response_json)

    # Returns company name, exchange listed, and industry
    def get_company(self, stock):
        response = requests.get(base_url + stock + '/company' + token)
        response_json = json.loads(response.text)
        company_name = response_json['companyName']
        exchange = response_json['exchange']
        industry = response_json['industry']
        print(company_name, exchange, industry)

    # Returns historical price information based on user inputted date range



def search_stock():
    stock_string = input('Enter a stock ticker, or multiple tickers separated by a ",": ').upper()
    stock_lst = stock_string.replace(" ", "").split(",")
    print(stock_lst)
    for stock in stock_lst:
        single_stock = Stock_shot(stock)
        single_stock.get_quote(stock)
        single_stock.get_peers(stock)
        single_stock.get_company(stock)
    get_price(stock_lst)


search_stock()