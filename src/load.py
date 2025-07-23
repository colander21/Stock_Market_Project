import sqlite3
import pandas as pd
import logging
from sqlalchemy import create_engine


def load_to_sqlite(csv_path, db_path, table_name='stocks'):
    df = pd.read_csv(csv_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

def load_to_postgres(csv_path, db_name, user, password, host='localhost', port=5432, table_name='stocks'):
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df['date'] = df['date'].dt.date

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    df.to_sql(table_name, engine, if_exists='replace', index=False)

def run():
    file_path = "../data/cleaned_portfolio_data.csv"
    load_to_sqlite(file_path, "../database/stocks.db")
    load_to_postgres(file_path, "stockdata", "carsonolander", "securepassword")