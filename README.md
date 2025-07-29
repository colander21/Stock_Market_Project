# Stock Market Data Pipeline Project

A complete end-to-end data engineering pipeline that extracts, transforms, and loads stock market data for technical analysis and signal detection. Built using Python, pandas, yfinance, and PostgreSQL/SQLite.

---

## Project Overview

This project demonstrates a full ETL pipeline with:
- **Data extraction** from Yahoo Finance using `yfinance`
- **Data transformation** with key financial indicators
- **Loading** into both **SQLite** and **PostgreSQL** databases
- **SQL queries** to analyze returns, volatility, and trends
- **Optional**: Visualization or signal-based backtesting extensions

---

## Project Architecture

src/
- extract.py # Pulls data from yfinance
- transform.py # Cleans and enriches data with metrics
- load.py # Loads into SQLite and PostgreSQL
- ueries.sql # SQL queries for analysis
- main.py # Runs full ETL pipeline


---

## Features Engineered

The following columns are added during the transformation step, grouped per `ticker`:

- `intraday_change` – Close price minus open price
- `daily_close_change` – Close[today] - Close[yesterday]
- `daily_percent_return` – Percentage change from previous close
- `moving_avg_5_days` – 5-day moving average
- `moving_avg_20_days` – 20-day moving average
- `volatility_10_days` – Rolling 10-day standard deviation of returns
- `cumulative_returns` – Cumulative price change
- `cumulative_percent_returns` – Cumulative return over time

---

## SQL Query Highlights

Stored in [`queries.sql`](./queries.sql):

- Highest-returning stocks by cumulative return
- Most volatile tickers in the last 10 days
- Stocks trading above their 20-day moving average
- MA crossover signals (5-day > 20-day)
- Daily return outliers

### Example (PostgreSQL):
```sql
SELECT ticker, ROUND(AVG(volatility_10_days), 2) AS avg_volatility
FROM stocks
WHERE date >= CURRENT_DATE - INTERVAL '10 days'
GROUP BY ticker
ORDER BY avg_volatility DESC;
```
This query returns the average 10-day volatility for each stock, rounded to 2 decimal places, using only the most recent 10 days of data.


# Tech Stack
Language: Python 3.11
Libraries: pandas, yfinance, sqlalchemy
Databases: SQLite (local), PostgreSQL (production)
Optional Tools: cron

# Getting Started

1. Clone the repository
git clone https://github.com/colander21/Stock_Market_Project.git
cd Stock_Market_Project

2. Set up your Python environment
conda create -n stockmarketenv python=3.11
conda activate stockmarketenv
pip install -r requirements.txt

3. Create Postgres database
store credentials in .env file
  - DB_NAME
  - DB_PASSWORD
  - DB_USER
  - DB_HOST
  - DB_PORT
  
4. Run the pipeline
python src/main.py

# Possible Extensions
Add signal-based backtesting (e.g. MA crossover strategies)
Build a Streamlit dashboard to visualize trends and performance
Deploy to cloud infrastructure (PostgreSQL on AWS, BigQuery, etc.)


# What I Learned
How to build a clean ETL pipeline with modular Python code
Feature engineering for financial time-series data
Managing data workflows with real-world databases
Writing and organizing reusable SQL for analytics
