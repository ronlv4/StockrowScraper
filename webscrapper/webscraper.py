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
import requests
import csv
import json
import ast

indicators = requests.get("https://stockrow.com/api/indicators.json")
statement = ["Cash+Flow", "Balance+Sheet", "Income+Statement", "Metrics", "Growth"]
indicators = indicators.json()
allStockrowCodes = {}
for dict in indicators:
    allStockrowCodes[dict['id']] = dict['name']


def get_companies_tickers():
    # from sp500 csv file get a list of all companies
    # create list where first odd index is ticker and even is company name
    sp500_list = []
    my_file = open('sp500.csv', mode='r')  # prepare a file containing list of companies tickers to collect data
    for (row) in my_file:
        parser = ast.literal_eval(row)
        sp500_list.append(parser[0])
        sp500_list.append(parser[1])
    return sp500_list


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
                dicts['id'] = allStockrowCodes[dicts['id']]
                writer.writerow(dicts)
            except KeyError:
                pass


with open('allCompanies.csv', mode='w') as cleaning:
    cleaning.writelines("This is a webscrapper by Ron Levi\n\n")
companiesTickers = get_companies_tickers()
companiesTickers = companiesTickers[2:]
for index, company in enumerate(companiesTickers):
    if index % 2 == 0:
        with open('allCompanies.csv', mode='a') as cleaning:
            cleaning.writelines("Company Name: {}\n Ticker: {}\n\n".format(companiesTickers[index+1], company))
        for state in statement:
            write_company_data(company, state)
    if index % 50 == 0:
        print(f"{index/2} companies scraped so far", end=" ,")
        print(f"{len(companiesTickers)/2} left.")
cleaning.close()
