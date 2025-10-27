SELECT MAX(timestamp) as most_recent_observation
FROM observations
WHERE station_id = %s
  AND service = %s;
