from django.db import models

# Create your models here.
from django.shortcuts import render
# from rest_framework.response import Response
from rest_framework import status
# from django.http import JsonResponse
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json

def get_current_data(url):

        result = requests.get(url)
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
        while "" in data:
            data.remove("")
        print({"Stock_Name": stock_name,
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
                })

get_current_data("https://www.moneycontrol.com/india/stockpricequote/cementmajor/acc/ACC06")
