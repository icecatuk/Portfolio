#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import requests
from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta

# Environment variables for API keys (set these in your environment for security)
BINANCE_API_KEY = os.getenv('JhEMLZn8NUKVtASi40V2ftkGGr2K1qNrs1AMS0xoQZvvunSfGWZeJtuAU8JIjP4L')
BINANCE_API_SECRET = os.getenv('pqpiL8PLprEaMzfwjELL6BpW4LepA1NKa0DV9qkL6ecbskMrOx0ypAybU7Ob0VCO')
CMC_API_KEY = os.getenv('dc739941-3a9e-4bb5-b03a-a940658b37ac')

# Initialize Binance Client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Fetch balances from Binance
def get_binance_balances():
    account = client.get_account()
    balances = [balance for balance in account['balances'] if float(balance['free']) > 0]
    return balances

# Fetch current prices from CoinMarketCap
def get_current_prices():
    headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
    response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', headers=headers)
    data = response.json()
    prices = {item['symbol']: item['quote']['USD']['price'] for item in data['data']}
    return prices

# Calculate portfolio value and performance
def calculate_performance(balances, prices):
    portfolio = []
    for balance in balances:
        symbol = balance['asset']
        quantity = float(balance['free'])
        price = prices.get(symbol)
        if price:
            value = quantity * price
            portfolio.append({'symbol': symbol, 'quantity': quantity, 'value': value})
    df = pd.DataFrame(portfolio)
    # Placeholder for calculating day/week/month/year gains or losses
    # You would need historical data for actual calculation
    print(df)

def main():
    balances = get_binance_balances()
    prices = get_current_prices()
    calculate_performance(balances, prices)

if __name__ == "__main__":
    main()
