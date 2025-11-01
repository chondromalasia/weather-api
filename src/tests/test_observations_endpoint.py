import pytest
from unittest.mock import Mock, patch
from datetime import datetime, date
from src.weather_api.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db():
    """Mock database instance"""
    with patch('src.weather_api.api.weather.Database') as mock:
        db_instance = Mock()
        mock.return_value = db_instance
        yield db_instance


class TestObservedHighsEndpoint:
    """Test suite for the /observations/highs endpoint"""

    def test_missing_station_id(self, client):
        """Test that endpoint returns 400 when station_id is missing"""
        response = client.get('/observations/highs')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'station_id' in data['error']

    def test_success_with_defaults(self, client, mock_db):
        """Test successful request with all default parameters"""
        mock_db.get_observed_highs.return_value = [
            {
                'timestamp': datetime(2025, 10, 29, 14, 0, 0),
                'date': date(2025, 10, 29),
                'station_id': 'KNYC',
                'measurement_type': 'temperature',
                'observation_type': 'max',
                'value': 75.5,
                'service': 'CLI'
            },
            {
                'timestamp': datetime(2025, 10, 28, 14, 0, 0),
                'date': date(2025, 10, 28),
                'station_id': 'KNYC',
                'measurement_type': 'temperature',
                'observation_type': 'max',
                'value': 78.2,
                'service': 'CLI'
            }
        ]

        response = client.get('/observations/highs?station_id=KNYC')

        assert response.status_code == 200
        data = response.get_json()
        assert data['station_id'] == 'KNYC'
        assert data['service'] == 'CLI'
        assert data['measurement_type'] == 'temperature'
        assert data['observation_type'] == 'max'
        assert data['count'] == 2
        assert len(data['observations']) == 2

        # Verify the database method was called with correct defaults
        mock_db.get_observed_highs.assert_called_once_with(
            'KNYC', 'temperature', 'max', 'CLI', None, None
        )

    def test_custom_service(self, client, mock_db):
        """Test with custom service parameter"""
        mock_db.get_observed_highs.return_value = []

        response = client.get('/observations/highs?station_id=KNYC&service=ASOS')

        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'ASOS'
        assert data['count'] == 0
        mock_db.get_observed_highs.assert_called_once_with(
            'KNYC', 'temperature', 'max', 'ASOS', None, None
        )

    def test_custom_measurement_type(self, client, mock_db):
        """Test with custom measurement_type parameter"""
        mock_db.get_observed_highs.return_value = [
            {
                'timestamp': datetime(2025, 10, 29, 14, 0, 0),
                'station_id': 'KNYC',
                'measurement_type': 'precipitation',
                'observation_type': 'total',
                'value': 0.5,
                'service': 'CLI'
            }
        ]

        response = client.get('/observations/highs?station_id=KNYC&measurement_type=precipitation&observation_type=total')

        assert response.status_code == 200
        data = response.get_json()
        assert data['measurement_type'] == 'precipitation'
        assert data['observation_type'] == 'total'
        assert data['count'] == 1
        mock_db.get_observed_highs.assert_called_once_with(
            'KNYC', 'precipitation', 'total', 'CLI', None, None
        )

    def test_with_start_date(self, client, mock_db):
        """Test with start date parameter"""
        mock_db.get_observed_highs.return_value = []

        response = client.get('/observations/highs?station_id=KMIA&start=2025-01-01')

        assert response.status_code == 200
        data = response.get_json()
        assert data['start'] == '2025-01-01'
        assert data['end'] is None
        mock_db.get_observed_highs.assert_called_once_with(
            'KMIA', 'temperature', 'max', 'CLI', '2025-01-01', None
        )

    def test_with_end_date(self, client, mock_db):
        """Test with end date parameter"""
        mock_db.get_observed_highs.return_value = []

        response = client.get('/observations/highs?station_id=KMIA&end=2025-12-31')

        assert response.status_code == 200
        data = response.get_json()
        assert data['start'] is None
        assert data['end'] == '2025-12-31'
        mock_db.get_observed_highs.assert_called_once_with(
            'KMIA', 'temperature', 'max', 'CLI', None, '2025-12-31'
        )

    def test_with_date_range(self, client, mock_db):
        """Test with both start and end date parameters"""
        mock_db.get_observed_highs.return_value = [
            {
                'timestamp': datetime(2025, 6, 15, 14, 0, 0),
                'date': date(2025, 6, 15),
                'station_id': 'KMIA',
                'measurement_type': 'temperature',
                'observation_type': 'max',
                'value': 92.5,
                'service': 'CLI'
            }
        ]

        response = client.get('/observations/highs?station_id=KMIA&start=2025-01-01&end=2025-12-31')

        assert response.status_code == 200
        data = response.get_json()
        assert data['start'] == '2025-01-01'
        assert data['end'] == '2025-12-31'
        assert data['count'] == 1
        mock_db.get_observed_highs.assert_called_once_with(
            'KMIA', 'temperature', 'max', 'CLI', '2025-01-01', '2025-12-31'
        )

    def test_all_parameters_custom(self, client, mock_db):
        """Test with all parameters customized"""
        mock_db.get_observed_highs.return_value = []

        response = client.get(
            '/observations/highs?station_id=KJFK&measurement_type=wind&observation_type=gust'
            '&service=ASOS&start=2025-05-01&end=2025-05-31'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['station_id'] == 'KJFK'
        assert data['measurement_type'] == 'wind'
        assert data['observation_type'] == 'gust'
        assert data['service'] == 'ASOS'
        assert data['start'] == '2025-05-01'
        assert data['end'] == '2025-05-31'
        mock_db.get_observed_highs.assert_called_once_with(
            'KJFK', 'wind', 'gust', 'ASOS', '2025-05-01', '2025-05-31'
        )

    def test_database_error_handling(self, client, mock_db):
        """Test that database errors are handled gracefully"""
        mock_db.get_observed_highs.side_effect = Exception('Database connection failed')

        response = client.get('/observations/highs?station_id=KNYC')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database error' in data['error']

    def test_query_file_not_found_error(self, client, mock_db):
        """Test that missing query file errors are handled"""
        mock_db.get_observed_highs.side_effect = AttributeError('Query file not found')

        response = client.get('/observations/highs?station_id=KNYC')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Query file not found' in data['error']

    def test_timestamp_serialization(self, client, mock_db):
        """Test that datetime objects are properly serialized to ISO format"""
        mock_db.get_observed_highs.return_value = [
            {
                'timestamp': datetime(2025, 10, 29, 14, 30, 45),
                'date': date(2025, 10, 29),
                'station_id': 'KNYC',
                'value': 75.5
            }
        ]

        response = client.get('/observations/highs?station_id=KNYC')

        assert response.status_code == 200
        data = response.get_json()
        assert data['observations'][0]['timestamp'] == '2025-10-29T14:30:45'
        assert data['observations'][0]['date'] == '2025-10-29'
