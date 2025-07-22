import pandas as pd
import logging
from extract import create_csv

def clean_data(filename):
    logging.info(f'Reading from {filename} and cleaning up data')
    df = pd.read_csv(filename)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.dropna()
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    df.sort_values(by=['ticker', 'date'], inplace=True)
    
    df['date'] = pd.to_datetime(df['date'])
    df['daily_change'] = df['close'] - df['open']
    df['daily_percent_return'] = 100 * df['daily_change']/df['open']

    return df


def run():
    input_path = '../data/my_portfolio.csv'
    data = clean_data(input_path)
    output_path = '../data/cleaned_portfolio_data.csv'
    create_csv(data, output_path)

 