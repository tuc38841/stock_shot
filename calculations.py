import datetime
import requests
import json
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

#from iexToken import token   ---> to hide token from public view
#from iexToken import base_url
base_url = "https://cloud.iexapis.com/stable/stock/"
test_base_url = "https://sandbox.iexapis.com/stable/stock/"
token = "?token=pk_44bd5242c4ab4595b33dafa82c61ba1c"
test_token = "?token=Tpk_b0410fc3685c4561980063dfcb5279a7"

#From get_stats
current_prices = []
current_ratios = []
debt_to_equities = []
return_on_equities = []
book_values_per_shares = []
price_targets_lows = []
price_targets_highs = []
price_targets_avg = []

def chart_high_lows(companies): # takes in list of stocks
    high_minus_low = []
    for value in range(len(price_targets_highs)):
        high_minus_low.append(price_targets_highs[value] - price_targets_lows[value])

    ax = plt.subplot()
    ax.bar(np.arange(len(companies)), current_prices, yerr=high_minus_low, align='center', alpha=0.5,
           ecolor='black', capsize=5)
    ax.set_ylabel('Stock Price')
    ax.set_xticks(np.arange(len(companies)))
    ax.set_xticklabels(companies)
    ax.set_title('Current Prices with High and Low Targets')
    #plt.scatter(np.arange(len(book_values_per_shares)), book_values_per_shares)
    plt.show()

#From Advanced Stats
profit_margins = []
price_to_books = []
price_to_sales = []
EPS_list = []
PE_ratios = []
PEG_ratios = []

#IDEAS FOR STATS
# 1) use a scale graph to compare profit margins, price to book, price to sales, pe ratios and peg ratios
# 2) #CREATE GRAPHS AND SCALES TO COMPARE VALUES FOR USER TO VISUALLY REPRESENT STATS AND SEE PERFORMANCE
     #EX. add highlighted ranges to show which stats are in good range and which are not

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

    # APPEND TO LIST
    price_targets_lows.append(low_target)
    price_targets_highs.append(high_target)
    price_targets_avg.append(average_target)
    print("Analyst Targets:\n\tLow: {}\n\tHigh: {}\n\tAverage: {}\n\n".format(low_target, high_target, average_target))

#Gets PE Ratio
def get_pe_ratio(stock):
    response_json = get_response(stock, '/quote')
    latest_price = response_json['latestPrice']
    current_prices.append(latest_price)

    response = requests.get(base_url + stock + '/stats/ttmEPS' + token)
    actual_EPS = json.loads(response.text)
    EPS_list.append(actual_EPS)

    PE_ratio = round((latest_price / actual_EPS), 2)
    PE_ratios.append(PE_ratio)
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

def get_advanced_stats(stock):
    response_json = get_response(stock, '/advanced-stats')
    profit_margin = response_json['profitMargin']
    price_to_sale = response_json['priceToSales']

    # Price to Book - Market price / book value. A lower value = undervalued or fundamentally troubled (depends on industry)
    # < 1 = potentially undervalued, > 1 = possibly overvalued, < 3 can be used as benchmark
    price_to_book = response_json['priceToBook']

    # degree to which company is financing operations through debt (ability of shareholder equity to cover outstanding debt)
    # Scale : Dependent on industry. Some companies utilize debt for financing more than others (utilities > tech)
    debt_to_equity = response_json['debtToEquity']

    PEG_ratio = response_json['pegRatio']

    profit_margins.append(profit_margin)
    price_to_books.append(price_to_book)
    price_to_sales.append(price_to_sale)
    PEG_ratios.append(PEG_ratio)
    debt_to_equities.append(debt_to_equity)

# From Balance Sheet
def get_stats(stock):
    get_financials(stock)

    response_json = get_response(stock, '/balance-sheet')
    get_company(stock)
    get_financials(stock)
    get_pe_ratio(stock)

    # Current Ratio
    # Measure short-term liquidity, reflects ability to pay off all debts when due
    # Goal: 1.5 to 3.0. Below 1 = indicates liquidity problems, over 3 = not utilizing assets efficiently
    current_ratio = round(response_json['balancesheet'][0]['currentAssets'] /
                          response_json['balancesheet'][0]['totalCurrentLiabilities'], 2)

    current_ratios.append(current_ratio) #APPEND TO LIST
    print("Current ratio: ", current_ratio)

    # Return on Equity
    # net income / shareholder's equity (assets - debts). Thought of as 'return on net assets'. Want target ROE equal/above
    # average of peers
    return_on_equity = round((get_net_income(stock) / response_json['balancesheet'][0]['shareholderEquity']*100), 2)

    return_on_equities.append(return_on_equity) #APPEND TO LIST
    print("Return on Equity: %", return_on_equity)

    # current price / book value per share
    book_value_per_share = round(response_json['balancesheet'][0]['shareholderEquity'] / response_json['balancesheet'][0]['commonStock'], 2)

    book_values_per_shares.append(book_value_per_share) #APPEND TO LIST
    print(book_value_per_share)
    print("Book Value per Share: ", book_value_per_share)

    get_price_target(stock)
    get_advanced_stats(stock)

def run_stats(companies):
    for company in companies:
        get_stats(company)
        get_advanced_stats(company)
    chart_high_lows(companies)
