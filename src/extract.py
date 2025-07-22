import yfinance as yf
import pandas as pd
from datetime import date, timedelta
import logging


def download_stock_data(tickers, start_date, end_date, interval='1d'):
    # download stock data for specified stocks(tickers) in provided range(start_date to end_date)
    logging.info(f'Downloading data for: {tickers}')
    stock_data = yf.download(tickers=tickers, start=start_date, end=end_date, interval=interval, group_by='ticker')
    # remove multi index to create regular dataframe
    stock_data = stock_data.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1).reset_index(level=0)


    return stock_data

def create_csv(data, filename):
    logging.info(f'Saving data to: {filename}')
    data.to_csv(filename)

def run():
    portfolio = ['AAPL', 'GOOG', 'VTI', 'LUV']
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    stock_data = download_stock_data(portfolio, thirty_days_ago, today)
    output_path = '../data/my_portfolio.csv'
    create_csv(stock_data, output_path)
 



