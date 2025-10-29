from flask import Blueprint, jsonify, request, current_app
import datetime
from src.weather_api.database.database import Database

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello World from Weather API!',
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'running'
    })


@weather_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'weather-api',
        'timestamp': datetime.datetime.now().isoformat()
    })


@weather_bp.route('/endpoints')
def list_endpoints():
    """List all available API endpoints."""
    endpoints = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            endpoints.append({
                'endpoint': rule.rule,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
            })
    return jsonify({'endpoints': endpoints})


@weather_bp.route('/forecast/highs')
def forecast_highs():
    """
    Get forecasted daily high temperatures.

    Query Parameters:
        location (required): Location code (e.g., 'KNYC')
        provider (required): Weather data provider
        cutoff (optional): Cutoff date (default: '2025-09-06')

    Returns:
        JSON response with forecasted highs per day
    """
    location = request.args.get('location')
    provider = request.args.get('provider')
    cutoff = request.args.get('cutoff', '2025-09-06')

    if not location:
        return jsonify({'error': 'Missing required parameter: location'}), 400

    if not provider:
        return jsonify({'error': 'Missing required parameter: provider'}), 400

    try:
        db = Database()
        results = db.get_forecasted_highs(location, provider, cutoff)

        # Convert date objects to strings for JSON serialization
        for result in results:
            if 'date' in result and result['date']:
                result['date'] = result['date'].isoformat()

        return jsonify({
            'location': location,
            'provider': provider,
            'cutoff': cutoff,
            'forecasted_highs': results
        })
    except AttributeError as e:
        return jsonify({'error': f'Query file not found: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@weather_bp.route('/observations/highs')
def observed_highs():
    """
    Get observed daily high temperatures.

    Query Parameters:
        station_id (required): Station ID (e.g., 'KNYC')
        service (optional): Data service (default: 'CLI')

    Returns:
        JSON response with observed highs per day
    """
    station_id = request.args.get('station_id')
    service = request.args.get('service', 'CLI')

    if not station_id:
        return jsonify({'error': 'Missing required parameter: station_id'}), 400

    try:
        db = Database()
        results = db.get_observed_highs(station_id, service)

        # Convert date objects to strings for JSON serialization
        for result in results:
            if 'date' in result and result['date']:
                result['date'] = result['date'].isoformat()

        return jsonify({
            'station_id': station_id,
            'service': service,
            'observed_highs': results
        })
    except AttributeError as e:
        return jsonify({'error': f'Query file not found: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@weather_bp.route('/observations/latest')
def most_recent_observation():
    """
    Get the date of the most recent observation for a station.

    Query Parameters:
        station_id (required): Station ID (e.g., 'KMIA')
        service (optional): Data service (default: 'CLI')

    Returns:
        JSON response with the most recent observation timestamp
    """
    station_id = request.args.get('station_id')
    service = request.args.get('service', 'CLI')

    if not station_id:
        return jsonify({'error': 'Missing required parameter: station_id'}), 400

    try:
        db = Database()
        results = db.get_most_recent_observation(station_id, service)

        # Convert timestamp to string for JSON serialization
        for result in results:
            if 'most_recent_observation' in result and result['most_recent_observation']:
                result['most_recent_observation'] = result['most_recent_observation'].isoformat()

        return jsonify({
            'station_id': station_id,
            'service': service,
            'most_recent_observation': results[0]['most_recent_observation'] if results and results[0]['most_recent_observation'] else None
        })
    except AttributeError as e:
        return jsonify({'error': f'Query file not found: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@weather_bp.route('/observations/temperatures/max')
def max_temperature_observations():
    """
    Get all maximum temperature observations for a station.

    Query Parameters:
        station_id (required): Station ID (e.g., 'KMIA')
        service (optional): Data service (default: 'CLI')

    Returns:
        JSON response with all max temperature observations ordered by timestamp DESC
    """
    station_id = request.args.get('station_id')
    service = request.args.get('service', 'CLI')

    if not station_id:
        return jsonify({'error': 'Missing required parameter: station_id'}), 400

    try:
        db = Database()
        results = db.get_max_temperature_observations(station_id, service)

        # Convert date and timestamp objects to strings for JSON serialization
        for result in results:
            if 'timestamp' in result and result['timestamp']:
                result['timestamp'] = result['timestamp'].isoformat()
            if 'date' in result and result['date']:
                result['date'] = result['date'].isoformat()

        return jsonify({
            'station_id': station_id,
            'service': service,
            'count': len(results),
            'observations': results
        })
    except AttributeError as e:
        return jsonify({'error': f'Query file not found: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@weather_bp.route('/forecast/providers')
def forecast_providers():
    """
    Get distinct list of weather forecast providers.

    Returns:
        JSON response with list of provider names
    """
    try:
        db = Database()
        results = db.get_distinct_forecast_providers()

        return jsonify({
            'providers': results
        })
    except AttributeError as e:
        return jsonify({'error': f'Query file not found: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@weather_bp.route('/forecast/locations')
def forecast_locations():
    """
    Get distinct list of forecast locations.

    Returns:
        JSON response with list of location codes
    """
    try:
        db = Database()
        results = db.get_distinct_forecast_locations()

        return jsonify({
            'locations': results
        })
    except AttributeError as e:
        return jsonify({'error': f'Query file not found: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500