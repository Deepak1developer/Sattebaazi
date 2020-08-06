# from django.shortcuts import render
# from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json


def map_url(request):
    ticker = request.GET.get('ticker', None)
    with open('./ticker_mapping_url.json') as f:
        json_data = json.load(f)
    return get_current_data(json_data[ticker])


def get_list_of_ticker(request):
    with open('./ticker_mapping_url.json') as f:
        json_data = json.load(f)
    return JsonResponse(list(json_data.keys()), safe=False, status=status.HTTP_200_OK)


def get_current_data(ticker):
    try:
        # import pdb
        # pdb.set_trace()
        result = requests.get(ticker)
        soup = BeautifulSoup(result.text, 'html.parser')
        stock_name = soup.find("h1", attrs={'class': 'pcstname'}).text
        all_data = soup.find("div", attrs={'class': 'nsert'})
        data = all_data.text.split("\n")
        community_sentiment = soup.find("div", attrs={'class': 'commounity_senti'}).text
        technical_rating = soup.find("div", attrs={'class': 'mt15 CTR pb20'}).find('a')['title']
        p_e = soup.find_all("div", attrs={'class': 'value_txtfr'})[1].text
        list_bsh = re.findall("parseInt\('(.*?)'\);", community_sentiment)
        buy_percentage = list_bsh[0] if len(list_bsh) >= 1 else None
        sell_percentage = list_bsh[1] if len(list_bsh) >= 2 else None
        hold_percentage = list_bsh[2] if len(list_bsh) >= 3 else None
        data = [x for x in data if x != ""]
        return JsonResponse({"Stock_Name": stock_name,
                "Price_Change": data[3],
                "Prev_Close": data[14],
                "Open_Price": data[16],
                "52_Week_Low": data[20],
                "52_Week_High": data[22],
                "Technical_Rating": technical_rating,
                "Buy_Percentage": buy_percentage,
                "Sell_Percentage": sell_percentage,
                "Hold_Percentage": hold_percentage,
                "P/E": p_e
                }, status=status.HTTP_200_OK)
    except:
        # return Error: Something went wrong
        print(ticker)


def fetch_nifty50_data(request):
    """return the stats of ticker for passed interval."""

    nifty50_list = list(pd.read_csv('/home/nineleaps/stock_market/nifty50list.csv')['Symbol'])  # add path for csv file
    # e.g=> nifty50_list = ['AXISBANK', 'BAJAJCON', 'BAJAJ-AUTO']
    result_list = []
    for ticker in nifty50_list:
        df = pd.read_csv('/home/nineleaps/stock_market/nse_data/{ticker}.csv'.format(
            ticker=ticker.upper()))  # add folder_name in the path of csv file
        result_list.extend(df.sort_values('Date', ascending=False).head(1).to_dict('records'))
    print(result_list)
    return JsonResponse(result_list, safe=False, status=status.HTTP_200_OK)

# def search(request):
#     """return the stats of ticker for passed interval.
#     :param ticker: string, name of ticker"""
#     result_list=[]
#     ticker = request.GET.get('ticker', None)
#     print(ticker)
#     df = pd.read_csv('/home/nineleaps/stock_market/nse_data/{ticker}.csv'.format(ticker=ticker.upper()))    # add folder_name in the path of csv file
#     result_list.extend(df.sort_values('Date', ascending=False).head(10).to_dict('records'))
#     print(result_list)
#     return JsonResponse(result_list, safe=False, status=status.HTTP_200_OK)