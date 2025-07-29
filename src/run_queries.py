from sqlalchemy import create_engine
import pandas as pd
import re
from dotenv import load_dotenv
import os
import logging

def run():
    load_dotenv()
    db_name=os.getenv('DB_NAME')
    db_user=os.getenv('DB_USER')
    db_password=os.getenv('DB_PASSWORD')
    db_port=os.getenv('DB_PORT')
    db_host=os.getenv('DB_HOST')
    
    logging.info('Reading queries.sql')
    with open('queries.sql') as f:
        sql_queries = f.read()
    
    query_blocks = re.findall(r"--\s*name:\s*(.*?)\n(.*?)(?=(--\s*name:|\Z))", sql_queries, re.DOTALL)

    queries = {name.strip(): sql.strip() for name, sql, _ in query_blocks}

    logging.info('Connecting to remote database')
    engine=create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    for name, sql in queries.items():
        try:
            df = pd.read_sql_query(sql, engine)
            df.to_csv(f'../data/{name}.csv', index=False)
            print(f"Saved: {name}.csv")
        except Exception as e:
            print(f"Error in query '{name}': {e}")

    logging.info('Query results loaded to csv files successfully')