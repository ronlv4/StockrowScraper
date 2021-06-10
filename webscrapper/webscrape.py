'''
This scrapper collects financial information about publicly traded companies from the site stockrow.com
it arraged all the data in an excel spread sheet organised by company ticker symbol and afterwards it's data.

@author Ron Levi
version 1.0.0 January 2021

#TODO fix output excel's colums width
add filters:
   financial, by ticker, by sector...
adjust numbers to millions or thousands
improve efficiency
improve generic format
'''
import xlsxwriter
from fastapi import FastAPI
import requests
import csv
import json
import ast
import pandas as pd
import numpy as np
import openpyxl

app = FastAPI()


@app.get('/')
def index():
    return 'g'

def create_id_name_dict(indicators):
    stockrow_codes = {}
    for indicators_dict in indicators:
        stockrow_codes[indicators_dict['id']] = indicators_dict['name']
    return stockrow_codes


def get_companies_tickers():
    # from sp500 csv file get a list of all companies
    # create list where first odd index is ticker and even is company name
    sp500_companies = {}
    df = pd.read_excel('sp500.xlsx')
    ticker_symbols = df['Ticker'].values
    company_names = df['Name'].values
    for i in range(len(ticker_symbols)):
        sp500_companies[ticker_symbols[i]] = company_names[i]
    return sp500_companies


def getfields(response):
    # input: response file of stockrow api of a specific company and financial statement
    # output: list of all available headers of financial information on that response file
    company_data = response.json()
    company_fields = []
    for dics in company_data:
        for keys in dics:
            company_fields.append(keys)
    company_fields = (dict.fromkeys(company_fields))
    return company_fields


def write_company_data(ticker, state):
    # append to output excel file financial information
    with open('allCompanies.csv', mode='a') as csv_file:
        response = requests.get(
            f"https://stockrow.com/api/companies/{ticker}/financials.json?ticker={ticker}&dimension=A&section={state}")
        if response.status_code == 404:
            return
        fieldnames = getfields(response)
        datalst = response.json()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_file.writelines("{} Data:\n\n".format(state))
        writer.writeheader()
        for dicts in datalst:
            try:
                dicts['id'] = stockrow_codes[dicts['id']]
                writer.writerow(dicts)
            except KeyError:
                pass


indicators = requests.get("https://stockrow.com/api/indicators.json")
statements = ["Cash+Flow", "Balance+Sheet", "Income+Statement", "Metrics", "Growth"]
indicators = indicators.json()
stockrow_codes = create_id_name_dict(indicators)

with open('allCompanies.csv', mode='w') as cleaning:
    cleaning.writelines("This is a webscrapper by Ron Levi\n\n")

companiesTickers = get_companies_tickers().values()
for index, company in enumerate(companiesTickers):
    if index % 2 == 0:
        with open('allCompanies.csv', mode='a') as cleaning:
            cleaning.writelines("Company Name: {}\n Ticker: {}\n\n".format(companiesTickers[index + 1], company))
        for state in statements:
            write_company_data(company, state)
    if index % 50 == 0:
        print(f"{index / 2} companies scraped so far", end=" ,")
        print(f"{len(companiesTickers) / 2} left.")
cleaning.close()
