import os
import logging
from pathlib import Path

import psycopg

from src.weather_api.config.loader import Config

class Database:
    def __init__(self):
        self.config = Config().database_config

        try:
            self.config["user"] = os.environ.get('POSTGRES_USER')
            self.config["password"] = os.environ.get('POSTGRES_PASSWORD')
        except:
            logger.info("Trouble with environment variables")

        self.sql_files_path = Path(__file__).parent / "sql_files"

        self.conn = psycopg.connect(**self.config)
        self.cur = self.conn.cursor()

        self.files = self.load_files()

    def load_files(self):
        return [f for f in os.listdir(self.sql_files_path)
                if os.path.isfile(self.sql_files_path / f) and f.endswith('.sql')]

    def read_query(self, query_name):
        if query_name in self.files:
            with open(self.sql_files_path / query_name, 'r') as to_read:
                return to_read.read()
        else:
            raise AttributeError(f'Filename {query_name} not found')

    def get_forecasted_highs(self, location, provider, cutoff='2025-09-06'):
        """
        Get forecasted daily high temperatures for a location and provider.

        Args:
            location: Location code (e.g., 'KNYC')
            provider: Weather data provider
            cutoff: Cutoff date (default: '2025-09-06')

        Returns:
            List of dictionaries with date and forecasted_high
        """
        query = self.read_query('get_forecasted_highs.sql')

        self.cur.execute(query, (location, cutoff, provider))
        columns = [desc[0] for desc in self.cur.description]
        results = []
        for row in self.cur.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def get_observed_highs(self, station_id, service='CLI'):
        """
        Get observed daily high temperatures for a station.

        Args:
            station_id: Station ID (e.g., 'KNYC')
            service: Data service (default: 'CLI')

        Returns:
            List of dictionaries with date and value
        """
        query = self.read_query('get_observed_highs.sql')

        self.cur.execute(query, (service, station_id))
        columns = [desc[0] for desc in self.cur.description]
        results = []
        for row in self.cur.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def get_most_recent_observation(self, station_id, service='CLI'):
        """
        Get the date of the most recent observation for a station.

        Args:
            station_id: Station ID (e.g., 'KMIA')
            service: Data service (default: 'CLI')

        Returns:
            List of dictionaries with most_recent_observation timestamp
        """
        query = self.read_query('get_most_recent_observation.sql')

        self.cur.execute(query, (station_id, service))
        columns = [desc[0] for desc in self.cur.description]
        results = []
        for row in self.cur.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def get_distinct_forecast_providers(self):
        """
        Get distinct list of weather forecast providers.

        Returns:
            List of dictionaries with provider names
        """
        query = self.read_query('get_distinct_forecast_providers.sql')

        self.cur.execute(query)
        columns = [desc[0] for desc in self.cur.description]
        results = []
        for row in self.cur.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def get_distinct_forecast_locations(self):
        """
        Get distinct list of forecast locations.

        Returns:
            List of dictionaries with location codes
        """
        query = self.read_query('get_distinct_forecast_locations.sql')

        self.cur.execute(query)
        columns = [desc[0] for desc in self.cur.description]
        results = []
        for row in self.cur.fetchall():
            results.append(dict(zip(columns, row)))
        return results
