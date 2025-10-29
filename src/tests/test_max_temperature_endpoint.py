import pytest
from unittest.mock import Mock, patch
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


class TestMaxTemperatureObservationsEndpoint:
    def test_max_temps_missing_station_id(self, client):
        """Test that endpoint returns 400 when station_id is missing"""
        response = client.get('/observations/temperatures/max')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'station_id' in data['error']

    def test_max_temps_success_default_service(self, client, mock_db):
        """Test successful max temperature observations request with default service"""
        from datetime import datetime

        mock_db.get_max_temperature_observations.return_value = [
            {
                'timestamp': datetime(2025, 10, 29, 14, 0, 0),
                'station_id': 'KMIA',
                'measurement_type': 'temperature',
                'observation_type': 'max',
                'value': 85.5,
                'service': 'CLI'
            },
            {
                'timestamp': datetime(2025, 10, 28, 14, 0, 0),
                'station_id': 'KMIA',
                'measurement_type': 'temperature',
                'observation_type': 'max',
                'value': 83.2,
                'service': 'CLI'
            }
        ]

        response = client.get('/observations/temperatures/max?station_id=KMIA')

        assert response.status_code == 200
        data = response.get_json()
        assert data['station_id'] == 'KMIA'
        assert data['service'] == 'CLI'
        assert data['count'] == 2
        assert len(data['observations']) == 2

    def test_max_temps_custom_service(self, client, mock_db):
        """Test max temperature observations with custom service parameter"""
        mock_db.get_max_temperature_observations.return_value = []

        response = client.get('/observations/temperatures/max?station_id=KMIA&service=ASOS')

        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'ASOS'
        assert data['count'] == 0
        mock_db.get_max_temperature_observations.assert_called_once_with('KMIA', 'ASOS')

    def test_max_temps_database_error(self, client, mock_db):
        """Test that database errors are handled properly"""
        mock_db.get_max_temperature_observations.side_effect = Exception('Database connection failed')

        response = client.get('/observations/temperatures/max?station_id=KMIA')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database error' in data['error']
