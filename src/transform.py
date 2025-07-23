import pandas as pd
import logging
from extract import create_csv

def clean_data(filename):
    logging.info(f'Reading from {filename} and cleaning up data')
    df = pd.read_csv(filename)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.dropna()
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    df.sort_values(by=['ticker', 'date'], ascending=[True, True], inplace=True)
    
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['intraday_change'] = df['close'] - df['open']
    df['daily_close_change'] = df.groupby('ticker')['close'].transform(lambda x: x - x.shift(1))
    df['daily_percent_return'] = df.groupby('ticker')['close'].transform(lambda x: x.pct_change()) * 100
    df['moving_avg_5_days'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=5).mean())
    df['moving_avg_20_days'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(window=20).mean())
    df['volatility_10_days'] = df.groupby('ticker')['daily_percent_return'].transform(lambda x: x.rolling(window=10).std())
    df['cumulative_returns'] = df.groupby('ticker')['daily_close_change'].cumsum()
    df['cumulative_percent_returns'] = df.groupby('ticker')['daily_percent_return'].cumsum()

    columns_to_round = {
    'intraday_change': 2,
    'daily_close_change': 2,
    'daily_percent_return': 4,
    'moving_avg_5_days': 2,
    'moving_avg_20_days': 2,
    'volatility_10_days': 4,
    'cumulative_returns': 2,
    'cumulative_percent_returns': 4,
    }

    for col, decimals in columns_to_round.items():
        df[col] = df[col].round(decimals)

    return df


def run():
    input_path = '../data/my_portfolio.csv'
    data = clean_data(input_path)
    output_path = '../data/cleaned_portfolio_data.csv'
    create_csv(data, output_path)

 