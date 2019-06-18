#“Data provided by IEX Cloud”
#<a href="https://iexcloud.io">Data provided by IEX Cloud</a>

from matplotlib import pyplot as plt
import datetime
import requests
import json

base_url = "https://sandbox.iexapis.com/stable/stock/"
token = "?token=Tpk_b0410fc3685c4561980063dfcb5279a7"

months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

# Gets index position at which month changes, so we can mark which tick to label on chart
def get_tick_index(input_months_int):
    month_tick_index = []
    for num in range(len(input_months_int)):
        if num == 0:
            month_tick_index.append(num)
        elif input_months_int[num] > input_months_int[num - 1]:
            month_tick_index.append(num)
        elif input_months_int[num] == 1 and input_months_int[num - 1] == 12:
            month_tick_index.append(num)
    return month_tick_index

# Gets the month at the tick postion
def get_month_labels(input_months_int):
    month_ticks = []
    months_for_chart = []
    for num in range(len(input_months_int)):
        if num == 0:
            month_ticks.append(input_months_int[num])
        elif input_months_int[num] > input_months_int[num - 1]:
            month_ticks.append(input_months_int[num])
        elif input_months_int[num] == 1 and input_months_int[num - 1] == 12:
            month_ticks.append(input_months_int[num])
    for num in month_ticks:
        if num in months.keys():
            months_for_chart.append(months[num])
    return months_for_chart

# ticks and labels for 5 year data for better spacing on graph
def get_5y_ticks(input_years_int):
    month_ticks = []
    for num in range(len(input_years_int)):
        if input_years_int[num] > input_years_int[num - 1]:
            month_ticks.append(num)
    return month_ticks

def get_5y_labels(input_years_int):
    labels_for_chart = []
    for num in range(len(input_years_int)):
        if input_years_int[num] > input_years_int[num - 1]:
            labels_for_chart.append(input_years_int[num])
    return labels_for_chart

def get_x_and_y_values():
    for index, value in enumerate(companies):
        plt.plot(x_values[index], y_values[index])
        print("Return During Period: {}% for {}".format(returns_per_range[index], companies[index]))

chart_range = ""
companies = []
x_values = []
y_values = []
month_day_values = []
months_labels = []
five_year_labels = []
returns_per_range = []

# Returns historical price information based on user inputted date range
def get_chart_info(stocks):
    chart_range = input("Would you like to see 1m, 3m, 6m, ytd, 1y, 2y, or 5y of data?:  ")
    stock_lst_for_legend = stocks

    for stock in stock_lst_for_legend:
        companies.append(stock)
        try:
            response = requests.get(base_url + stock + '/chart/' + chart_range + token)
            response_json = json.loads(response.text)

            year_mon_day = [i['date'] for i in response_json]
            day_length = range(len(year_mon_day))
            x_values.append(day_length)
            close_value = [i['close'] for i in response_json]
            y_values.append(close_value)

            # values of 1m
            day = [i['date'][-2:] for i in response_json]
            month_day_values.append(day)

            # values for 3m, 6m, ytd, 1y, and 2y
            dates_of_months_int = [int(i['date'][5:7]) for i in response_json]
            months_labels.append(dates_of_months_int)

            # values for 5y
            five_years_int = [int(i['date'][:4]) for i in response_json]
            five_year_labels.append(five_years_int)

            percentage_return = round((((close_value[-1] - close_value[0]) / close_value[0]) * 100), 1)
            returns_per_range.append(percentage_return)

        except Exception as e:
            print(e)
            print("Make sure to enter values exactly as stated in question (no spaces).")

    get_chart(chart_range)

##########1y, 2y, 5y won't step through ticks and/or ticklabels############

def get_chart(chart_range):
    if chart_range == '1m':
        ax = plt.subplot()
        for index, value in enumerate(companies):
            plt.plot(x_values[index], y_values[index])
            print("Return During Period: {}% for {}".format(returns_per_range[index], companies[index]))
        ax.set_xticks(x_values[index])
        ax.set_xticklabels(month_day_values[index])
        ax.legend(companies)
        plt.show()

    elif chart_range == ("3m") or ("6m") or ("ytd"):
        ax = plt.subplot()
        for index, value in enumerate(companies):
            plt.plot(x_values[index], y_values[index])
            print("Return During Period: {}% for {}".format(returns_per_range[index], companies[index]))
        ax.set_xticks(get_tick_index(months_labels[index]))
        ax.set_xticklabels(get_month_labels(months_labels[index]))
        ax.legend(companies)
        plt.show()

    elif chart_range == "1y":
        ax = plt.subplot()
        for index, value in enumerate(companies):
            plt.plot(x_values[index], y_values[index])
            print("Return During Period: {}% for {}".format(returns_per_range[index], companies[index]))
        ax.set_xticks(get_tick_index(months_labels[index])[::3])
        ax.set_xticklabels(get_month_labels(months_labels[index])[::3])
        ax.legend(companies)
        plt.show()

    elif chart_range == "2y":
        ax = plt.subplot()
        for index, value in enumerate(companies):
            plt.plot(x_values[index], y_values[index])
            print("Return During Period: {}% for {}".format(returns_per_range[index], companies[index]))
        ax.set_xticks(get_tick_index(months_labels[index]))[::6]
        ax.set_xticklabels(get_month_labels(months_labels[index]))[::6]
        ax.legend(companies)
        plt.show()
        print(get_tick_index(months_labels[index]))[::6]
        print((get_month_labels(months_labels[index])))[::6]

    elif chart_range == "5y":
        ax = plt.subplot()
        for index, value in enumerate(companies):
            plt.plot(x_values[index], y_values[index])
            print("Return During Period: {}% for {}".format(returns_per_range[index], companies[index]))
        ax.set_xticks(get_5y_ticks(five_year_labels[index]))
        ax.set_xticklabels(get_5y_labels(five_year_labels[index]))
        ax.legend(companies)
        plt.show()

    else:
        print("Error in retrieving chart. Please try again.")

