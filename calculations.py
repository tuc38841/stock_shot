import datetime
import requests
import json

from requests import Response

base_url = "https://cloud.iexapis.com/stable/stock/"
token = "?token=pk_44bd5242c4ab4595b33dafa82c61ba1c"

#Gets PE Ratio
def get_pe_ratio(stock):
    response = requests.get(base_url + stock + '/quote' + token)
    response_json = json.loads(response.text)
    close_value = response_json['close']
    print(close_value)

    response = requests.get(base_url + stock + '/stats/ttmEPS' + token)
    actual_EPS = json.loads(response.text)
    print(actual_EPS)

    PE_ratio = round((close_value / actual_EPS), 2)
    print("PE Ratio (TTM): {}".format(PE_ratio))



#PE ratio:
# Current price / EPS
#    Need to obtain EPS then build func to divide current price by EPS
 #   Need to factor in negative EPS (Try/error block)

get_pe_ratio('aapl')