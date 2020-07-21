# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:03:32 2020

@author: joesh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as datetime


import plotly
import cufflinks as cf
cf.go_offline()

import requests
from urllib.request import urlopen

def pageReturn():
    page = urlopen("https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily-deaths/").read()
    page = page.decode(encoding="UTF-8")
    return page

def mostRecent(page):
    today = datetime.datetime.now()
    for i in range(0,10):
        month = today.strftime("%B")
        day = str(today.day)
        if page.find(day + " " + month) != -1:
            break
        today = today - datetime.timedelta(days=1)
    return today

def downloadFile():
    page = pageReturn()
    today = mostRecent(page)
    
    year = str(today.year)
    month = today.strftime("%B")
    day = str(today.day)
    
    dls = "https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2020/07/COVID-19-total-announced-deaths-"\
    +day+"-"+month+"-"+year+".xlsx"
    resp = requests.get(dls)
    output = open('latestcovid19data.xlsx', 'wb')
    output.write(resp.content)
    output.close()

def createDataFrame(sheet):   
    if sheet == "region":
        sheetN = 2
        extraRow = False
    elif sheet == "age":
        sheetN = 4
        extraRow = True
    else:
        print("Invalid string input")
        return
    
    page = pageReturn()
    today = mostRecent(page)
    
    begin = datetime.datetime(2020,3,1)
    diff = today - begin

    skips = list(range(0,15)) + [17] + [23*extraRow]
    cols = [1] + list(range(4,diff.days+3))

    df = pd.read_excel('latestcovid19data.xlsx',sheet_name=sheetN,skiprows=skips,index_col=0,usecols=cols)
    df = df.transpose().astype(dtype="int64")
    df.name = "Deaths by " + sheet
    return df

def lineGraph(df,includeTotal):
    if includeTotal == False:
        df = df[df.columns.difference(['England','Total'])]
    plt.figure(figsize=(14,8))
    for elem in df:
        df[elem].plot(label=elem)
    plt.legend()
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Deaths')
    plt.title(df.name)
    plt.show()


def rollingGraph(df,includeTotal):
    if includeTotal == False:
        df = df[df.columns.difference(['England','Total'])]
    plt.figure(figsize=(14,8))
    for elem in df:
        df[elem].rolling(window=7,center=True).mean().plot(label=elem)
    plt.legend()
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Deaths')
    plt.title(df.name)
    plt.show()
