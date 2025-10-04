WITH earliest_forecast_per_day AS (
    SELECT MIN(timestamp) as earliest_timestamp, location, provider
        FROM weather_forecasts
        WHERE location = %s
            AND timestamp > %s
            AND EXTRACT(HOUR FROM timestamp) > 2
        GROUP BY DATE(timestamp), provider, location),
daily_forecast AS (
    SELECT wf.*
    FROM weather_forecasts wf
    INNER JOIN earliest_forecast_per_day ef
        ON wf.timestamp = ef.earliest_timestamp
        AND wf.location = ef.location
        AND wf.provider = ef.provider
    WHERE DATE(wf.end_time) = DATE(ef.earliest_timestamp)
)
SELECT DATE(timestamp) as date, MAX(temperature) as forecasted_high
FROM daily_forecast
WHERE provider = %s
GROUP BY DATE(timestamp), location, provider
ORDER BY date;
