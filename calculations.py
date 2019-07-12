import datetime
import requests
import json
#from iexToken import token   ---> to hide token from public view
#from iexToken import base_url

from requests import Response

base_url = "https://cloud.iexapis.com/stable/stock/"
token = "?token=pk_44bd5242c4ab4595b33dafa82c61ba1c"

def get_response(stock, url_string):
    response = requests.get(base_url + stock + url_string + token)
    response_json = json.loads(response.text)
    return response_json

def get_company(stock):
    response_json = get_response(stock, '/company')
    company_name = response_json['companyName']
    exchange = response_json['exchange']
    industry = response_json['industry']
    print(company_name, "||", exchange, "||", industry)

def get_price_target(stock):
    response_json = get_response(stock, '/price-target')
    low_target = response_json['priceTargetLow']
    high_target = response_json['priceTargetHigh']
    average_target = response_json['priceTargetAverage']
    print("Analyst Targets:\n\tLow: {}\n\tHigh: {}\n\tAverage: {}\n\n".format(low_target, high_target, average_target))

#Gets PE Ratio
def get_pe_ratio(stock):
    response_json = get_response(stock, '/quote')
    close_value = response_json['close']
    #print(close_value)

    response = requests.get(base_url + stock + '/stats/ttmEPS' + token)
    actual_EPS = json.loads(response.text)
    #print(actual_EPS)

    PE_ratio = round((close_value / actual_EPS), 2)
    print("PE Ratio (TTM): {}".format(PE_ratio))

#Defaults to quaterly financial data
def get_financials(stock):
    response_json = get_response(stock, '/financials')
    report_date = response_json['financials'][0]['reportDate']
    return report_date
    print(return_date)

def get_net_income(stock):
    response_json = get_response(stock, '/income')
    net_income = response_json['income'][0]['netIncome']
    return net_income
    print(net_income)


#Advanced stats -> Balance sheet
def get_stats(stock):
    response_json = get_response(stock, '/balance-sheet')
    get_company(stock)
    get_pe_ratio(stock)

    # Current Ratio
    # Measure short-term liquidity, reflects ability to pay off all debts when due
    # Goal: 1.5 to 3.0. Below 1 = indicates liquidity problems, over 3 = not utilizing assets efficiently
    current_ratio = round(response_json['balancesheet'][0]['currentAssets'] /
                          response_json['balancesheet'][0]['totalCurrentLiabilities'], 2)
    print("Current ratio: ", current_ratio)

    # D/E
    # degree to which company is financing operations through debt (ability of shareholder equity to cover outstanding debt)
    # Scale : Dependent on industry. Some companies utilize debt for financing more than others (utilities > tech)
    debt_to_equity = round(response_json['balancesheet'][0]['longTermDebt'] /
                           response_json['balancesheet'][0]['shareholderEquity'], 2)
    print("Debt to Equity Ratio: ", debt_to_equity)

    # Return on Equity
    # net income / shareholder's equity (assets - debts). Though of as 'return on net assets'. Want target ROE equal/above
    # average of peers
    return_on_equity = round((get_net_income(stock) / response_json['balancesheet'][0]['shareholderEquity']*100), 2)
    print("Return on Equity: %", return_on_equity)

    # Price to Book
    # Market price / book value. A lower value = undervalued or fundamentally troubled (depends on industry)
    # < 1 = potentially undervalued, > 1 = possibly overvalued, < 3 can be used as benchmark
    # current price / book value per share
    book_value_per_share = round(response_json['balancesheet'][0]['shareholderEquity'] / \
                           response_json['balancesheet'][0]['commonStock'], 2)
    print("Book Value per Share: ", book_value_per_share)
    response_pe = requests.get(base_url + stock + '/quote' + token)
    response_pe_json = json.loads(response_pe.text)
    current_price = response_pe_json['close']

    price_to_book = round(current_price / book_value_per_share, 2)
    print("Price to book Ratio: ", price_to_book)

    get_price_target(stock)

    #profit_margin = response_json['profitMargin']
    #price_to_sales = response_json['priceToSales']

    #earnings growth rate = current EPS / previous EPS (use annual data)
    #PE_ratio = get_pe_ratio(stock)
    #PEG_ratio = response_json['pegRatio']



