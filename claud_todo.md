# Weather API - Forecast Endpoint TODO

## Current SQL Query to Implement
```sql
WITH earliest_forecast_per_day AS (
    SELECT MIN(timestamp) as earliest_timestamp, location, provider
        FROM weather_forecasts
        WHERE location = 'KNYC'
            AND timestamp > '2025-09-06'
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
SELECT DATE(timestamp), MAX(temperature) as forecasted_high
FROM daily_forecast
GROUP BY DATE(timestamp), location, provider;
```

## API Endpoint Requirements
- **Parameters:**
  - `location` (required) - e.g., 'KNYC'
  - `provider` (required)
  - `cutoff` (optional, defaults to '2025-09-06' for now)

- **Response:** JSON with forecasted highs per day

## Implementation Steps

### 1. Install and add psycopg2 to requirements.txt
- Add PostgreSQL driver dependency

### 2. Implement database connection module (src/weather_api/database/db.py)
- Create connection using config from `src/weather_api/config/database.yaml`
- Set up connection pooling or context manager

### 3. Create database query function
- Function signature: `get_forecasted_highs(location, provider, cutoff=None)`
- Parameterize the SQL query
- Return results as list of dictionaries

### 4. Create API endpoint
- Add new route (e.g., `/forecast/highs` or `/weather/forecast/highs`)
- Accept query parameters
- Validate parameters (location and provider required)
- Call database query function
- Return JSON response

### 5. Add error handling
- Database connection errors
- Invalid/missing parameters
- No results found
- SQL errors

### 6. Write tests
- Test database query function
- Test API endpoint with valid parameters
- Test error cases

### 7. Run tests and manual testing
- Run pytest
- Test endpoint with curl/Postman

## Current Database Config
Location: `src/weather_api/config/database.yaml`
```yaml
database:
  host: "postgres.weather.svc.cluster.local"
  port: "5432"
  dbname: "weather_forecasts"
```

## Notes
- The cutoff date stays at '2025-09-06' for now but should be parameterizable
- Query filters for forecasts after 2am (EXTRACT(HOUR FROM timestamp) > 2)
- Returns max temperature per day grouped by location and provider
