#“Data provided by IEX Cloud”
#<a href="https://iexcloud.io">Data provided by IEX Cloud</a>

from matplotlib import pyplot as plt
import requests
import json

base_url = "https://sandbox.iexapis.com/stable/stock/"
token = "?token=Tpk_b0410fc3685c4561980063dfcb5279a7"

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


def get_price(stocks):
    chart_range = input("Would you like to see 1d, 1m, 3m, 6m, ytd, 1y, 2y, or 5y of data?:  ")
    stock_lst_for_legend = stocks
    for stock in stocks:
        try:
            response = requests.get(base_url + stock + '/chart/' + chart_range + token)
            response_json = json.loads(response.text)

            year_mon_day = [i['date'] for i in response_json]
            day_length = range(len(year_mon_day))
            day = [i['date'][-2:] for i in response_json]
            close_value = [i['close'] for i in response_json]

            percentage_return = round((((close_value[-1] - close_value[0]) / close_value[0]) * 100), 1)
            print("Return During Period: {}% for {}".format(percentage_return, stock))

            # values for 1d

            # values for 3m, 6m, ytd, 1y, and 2y
            dates_of_months = [i['date'][5:7] for i in response_json]
            dates_of_months_int = [int(i) for i in dates_of_months]
            print(dates_of_months_int)

            # values for 5y
            year5_years = [i['date'][:4] for i in response_json]
            year5_years_int = [int(i) for i in year5_years]

            if chart_range == "1m":  # legend colors incorrect
                ax = plt.subplot()
                plt.plot(day_length, close_value)
                ax.set_xticks(day_length)
                ax.set_xticklabels(day)
                ax.legend(stock_lst_for_legend)
                plt.show()

        except Exception as e:
            print(e)
            print("Make sure to enter values exactly as stated in question (no spaces).")


