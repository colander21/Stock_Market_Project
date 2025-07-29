-- name: Returns for each stock
SELECT ticker, MAX(cumulative_percent_returns) AS max_return
FROM stocks
GROUP BY ticker
ORDER BY max_return DESC;

-- name: Most recent price for each stock
SELECT DISTINCT ON (ticker) date, ticker, open, close, low, high, intraday_change, daily_percent_return
FROM stocks
ORDER BY ticker, date DESC;

-- name: Volatility snapshot(last 10 days)
SELECT ticker, ROUND(AVG(volatility_10_days), 2) AS avg_volatility
FROM stocks
WHERE date >= CURRENT_DATE - INTERVAL '10 days'
GROUP BY ticker
ORDER BY avg_volatility DESC;

-- name: Stocks that are above their 20-day moving average (bullish)
SELECT date, ticker, close, daily_percent_return, moving_avg_5_days, moving_avg_20_days, cumulative_percent_returns
FROM stocks
WHERE close > moving_avg_20_days
AND date = CURRENT_DATE;

-- name: Daily return outliers
SELECT date, ticker, close, daily_percent_return, moving_avg_5_days, moving_avg_20_days
FROM stocks
WHERE ABS(daily_percent_return) > 5
ORDER BY date DESC;

-- name: Crossover signal (5-day MA > 20-day MA)
SELECT date, ticker, close, daily_percent_return, moving_avg_5_days, moving_avg_20_days, cumulative_percent_returns
FROM stocks
WHERE moving_avg_5_days > moving_avg_20_days
AND date = CURRENT_DATE;