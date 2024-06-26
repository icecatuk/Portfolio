
#Created on Thu Mar 28 02:51:39 2024

#@author: kevinodonnell
#"""

import requests
import datetime
from binance.client import Client

# Binance API credentials
api_key = 'BINANCE_API'
api_secret = 'SECRET_KEY'

# Initialize Binance client
client = Client(api_key, api_secret)

# Function to fetch cryptocurrency data from CoinGecko API
def get_crypto_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to calculate the change in value for a given period
def calculate_change(current_price, old_price):
    if old_price == 0:
        return 0
    change_percent = ((current_price - old_price) / old_price) * 100
    return change_percent

# Get current date and calculate past dates
current_date = datetime.datetime.now().date()
one_day_ago = current_date - datetime.timedelta(days=1)
one_week_ago = current_date - datetime.timedelta(weeks=1)
one_month_ago = current_date - datetime.timedelta(days=30)
one_year_ago = current_date - datetime.timedelta(days=365)

# Fetch account balances from Binance
account_info = client.get_account()
balances = {item['asset'].lower(): float(item['free']) for item in account_info['balances'] if float(item['free']) > 0}

# Fetch data and calculate changes for each cryptocurrency
for coin_id, quantity in balances.items():
    try:
        data = get_crypto_data(coin_id)
        current_price = data['market_data']['current_price']['usd']
        price_24h_ago = data['market_data']['current_price']['usd'] / (1 + data['market_data']['price_change_percentage_24h_in_currency']['usd'] / 100)
        price_7d_ago = data['market_data']['current_price']['usd'] / (1 + data['market_data']['price_change_percentage_7d_in_currency']['usd'] / 100)
        price_30d_ago = data['market_data']['current_price']['usd'] / (1 + data['market_data']['price_change_percentage_30d_in_currency']['usd'] / 100)
        price_1y_ago = data['market_data']['current_price']['usd'] / (1 + data['market_data']['price_change_percentage_1y_in_currency']['usd'] / 100)

        change_24h = calculate_change(current_price, price_24h_ago)
        change_7d = calculate_change(current_price, price_7d_ago)
        change_30d = calculate_change(current_price, price_30d_ago)
        change_1y = calculate_change(current_price, price_1y_ago)

        current_value = quantity * current_price

        print(f"\nCryptocurrency: {data['name']}")
        print(f"Current Holdings: {quantity} {data['symbol'].upper()}")
        print(f"Current Value: ${current_value:.2f}")
        print(f"24 Hour Change: {change_24h:.2f}%")
        print(f"7 Day Change: {change_7d:.2f}%")
        print(f"30 Day Change: {change_30d:.2f}%")
        print(f"1 Year Change: {change_1y:.2f}%")
    except Exception as e:
        print(f"Error fetching data for {coin_id}: {str(e)}")