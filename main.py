#“Data provided by IEX Cloud”
#<a href="https://iexcloud.io">Data provided by IEX Cloud</a>

import pandas as pd
from matplotlib import pyplot as plt
import requests
import json
from charts import get_chart_info

base_url = "https://cloud.iexapis.com/stable/stock/"
token = "?token=pk_44bd5242c4ab4595b33dafa82c61ba1c"
#old_base_url = "https://sandbox.iexapis.com/stable/stock/"
#old_token = "?token=Tpk_b0410fc3685c4561980063dfcb5279a7"

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

def search_stock():
    stock_string = input("Enter a company's stock ticker (ex. apple = aapl): ").upper()
    stock_lst = stock_string.replace(" ", "").split()
    print(stock_lst)
    for stock in stock_lst:
        single_stock = Stock_shot(stock)
        single_stock.get_quote(stock)
        peers = single_stock.get_peers(stock)
        single_stock.get_company(stock)
    peers = requests.get(base_url + stock_string + '/peers' + token)
    peers_json = json.loads(peers.text)
    stock_plus_peers = stock_lst + peers_json
    print(stock_plus_peers)
    get_chart_info(stock_plus_peers)


search_stock()