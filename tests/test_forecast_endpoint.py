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


class TestForecastHighsEndpoint:
    def test_forecast_highs_missing_location(self, client):
        """Test that endpoint returns 400 when location is missing"""
        response = client.get('/forecast/highs?provider=test_provider')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'location' in data['error']

    def test_forecast_highs_missing_provider(self, client):
        """Test that endpoint returns 400 when provider is missing"""
        response = client.get('/forecast/highs?location=KNYC')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'provider' in data['error']

    def test_forecast_highs_success(self, client, mock_db):
        """Test successful forecast highs request"""
        from datetime import date

        # Mock the database response
        mock_db.get_forecasted_highs.return_value = [
            {'date': date(2025, 9, 7), 'forecasted_high': 75.5},
            {'date': date(2025, 9, 8), 'forecasted_high': 78.2}
        ]

        response = client.get('/forecast/highs?location=KNYC&provider=test_provider')

        assert response.status_code == 200
        data = response.get_json()

        assert data['location'] == 'KNYC'
        assert data['provider'] == 'test_provider'
        assert data['cutoff'] == '2025-09-06'
        assert 'forecasted_highs' in data
        assert len(data['forecasted_highs']) == 2
        assert data['forecasted_highs'][0]['date'] == '2025-09-07'
        assert data['forecasted_highs'][0]['forecasted_high'] == 75.5

    def test_forecast_highs_with_custom_cutoff(self, client, mock_db):
        """Test forecast highs with custom cutoff date"""
        mock_db.get_forecasted_highs.return_value = []

        response = client.get('/forecast/highs?location=KNYC&provider=test_provider&cutoff=2025-09-10')

        assert response.status_code == 200
        data = response.get_json()
        assert data['cutoff'] == '2025-09-10'

        # Verify the database method was called with correct parameters
        mock_db.get_forecasted_highs.assert_called_once_with('KNYC', 'test_provider', '2025-09-10')

    def test_forecast_highs_database_error(self, client, mock_db):
        """Test that database errors are handled correctly"""
        mock_db.get_forecasted_highs.side_effect = Exception('Database connection failed')

        response = client.get('/forecast/highs?location=KNYC&provider=test_provider')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database error' in data['error']

    def test_forecast_highs_query_file_not_found(self, client, mock_db):
        """Test that AttributeError for missing query file is handled"""
        mock_db.get_forecasted_highs.side_effect = AttributeError('Filename not found')

        response = client.get('/forecast/highs?location=KNYC&provider=test_provider')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Query file not found' in data['error']
