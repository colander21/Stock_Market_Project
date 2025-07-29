import sqlite3
from sqlalchemy import create_engine, Numeric, Date, Text, BigInteger
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


def load_to_sqlite(csv_path, db_path, table_name='stocks'):
    df = pd.read_csv(csv_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

def load_to_postgres(csv_path, db_name, user, password, port, host='localhost', table_name='stocks'):
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df['date'] = df['date'].dt.date
    df['volatility_10_days'] = pd.to_numeric(df['volatility_10_days'], errors='coerce')
    df['moving_avg_5_days'] = pd.to_numeric(df['moving_avg_5_days'], errors='coerce')
    df['moving_avg_20_days'] = pd.to_numeric(df['moving_avg_20_days'], errors='coerce')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    dtype_map = {
        'date': Date(),
        'ticker': Text(),
        'open': Numeric(10, 4),
        'high': Numeric(10, 4),
        'low': Numeric(10, 4),
        'close': Numeric(10, 4),
        'volume': BigInteger(),
        'intraday_change': Numeric(10, 4),
        'daily_close_change': Numeric(10, 4),
        'daily_percent_return': Numeric(6, 4),
        'moving_avg_5_days': Numeric(10, 4),
        'moving_avg_20_days': Numeric(10, 4),
        'volatility_10_days': Numeric(10, 4),
        'cumulative_returns': Numeric(10, 4),
        'cumulative_percent_returns': Numeric(6, 4)
    }

    df.to_sql(table_name, engine, if_exists='replace', index=False, dtype=dtype_map)

def run():
    file_path = "../data/cleaned_portfolio_data.csv"
    load_to_sqlite(file_path, "../database/stocks.db")
    load_dotenv()
    db_name=os.getenv('DB_NAME')
    db_user=os.getenv('DB_USER')
    db_password=os.getenv('DB_PASSWORD')
    db_port=os.getenv('DB_PORT')
    load_to_postgres(file_path, db_name, db_user, db_password, port=db_port)

    