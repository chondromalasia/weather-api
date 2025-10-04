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