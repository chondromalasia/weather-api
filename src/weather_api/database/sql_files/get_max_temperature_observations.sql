SELECT *
FROM observations
WHERE measurement_type = 'temperature'
    AND observation_type = 'max'
    AND service = %s
    AND station_id = %s
ORDER BY timestamp DESC;
