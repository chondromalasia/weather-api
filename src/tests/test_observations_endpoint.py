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


class TestObservedHighsEndpoint:
    def test_observed_highs_missing_station_id(self, client):
        """Test that endpoint returns 400 when station_id is missing"""
        response = client.get('/observations/highs')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'station_id' in data['error']

    def test_observed_highs_success_default_service(self, client, mock_db):
        """Test successful observed highs request with default service"""
        from datetime import date

        mock_db.get_observed_highs.return_value = [
            {'date': date(2025, 9, 7), 'value': 75.5},
            {'date': date(2025, 9, 8), 'value': 78.2}
        ]

        response = client.get('/observations/highs?station_id=KNYC')

        assert response.status_code == 200
        data = response.get_json()
        assert data['station_id'] == 'KNYC'
        assert data['service'] == 'CLI'
        assert len(data['observed_highs']) == 2

    def test_observed_highs_custom_service(self, client, mock_db):
        """Test observed highs with custom service parameter"""
        mock_db.get_observed_highs.return_value = []

        response = client.get('/observations/highs?station_id=KNYC&service=ASOS')

        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'ASOS'
        mock_db.get_observed_highs.assert_called_once_with('KNYC', 'ASOS')
