-- Returns for each stock
SELECT ticker, MAX(cumulative_percent_returns) AS max_return
FROM stocks
GROUP BY ticker
ORDER BY max_return DESC;

-- Most recent price for each stock
SELECT DISTINCT ON (ticker) *
FROM stocks
ORDER BY ticker, date DESC;

-- Volatility snapshot(last 10 days)
SELECT ticker, AVG(volatility_10_days) AS avg_volatility
FROM stocks
WHERE date >= CURRENT_DATE - INTERVAL '10 days'
GROUP BY ticker
ORDER BY avg_volatility DESC;

-- Stocks that are above their 20-day moving average (bullish)
SELECT *
FROM stocks
WHERE close > moving_avg_20_days
AND date = CURRENT_DATE;

-- Daily return outliers
SELECT *
FROM stocks
WHERE ABS(daily_percent_return) > 5
ORDER BY date DESC;

-- Crossover signal (5-day MA > 20-day MA)
SELECT *
FROM stocks
WHERE moving_avg_5_days > moving_avg_20_days
AND date = CURRENT_DATE;