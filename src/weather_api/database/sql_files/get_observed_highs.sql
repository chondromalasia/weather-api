SELECT *
FROM observations
WHERE measurement_type = %s
    AND observation_type = %s
    AND service = %s
    AND station_id = %s
    AND (%s IS NULL OR timestamp >= %s)
    AND (%s IS NULL OR timestamp <= %s)
ORDER BY timestamp DESC;
