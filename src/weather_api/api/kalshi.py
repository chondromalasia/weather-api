from flask import Blueprint, jsonify
import datetime
from src.weather_api.external.kalshi_client import get_kalshi_credentials, get

kalshi_bp = Blueprint('kalshi', __name__, url_prefix='/kalshi')


@kalshi_bp.route('/balance')
def get_balance():
    """
    Get Kalshi portfolio balance.

    Returns:
        JSON response with balance information
    """
    try:
        private_key, api_key_id = get_kalshi_credentials()
        response = get(private_key, api_key_id, "/trade-api/v2/portfolio/balance")

        if response.status_code == 200:
            data = response.json()
            balance_cents = data.get('balance', 0)
            balance_dollars = balance_cents / 100

            return jsonify({
                'status': 'success',
                'balance_cents': balance_cents,
                'balance_dollars': f'{balance_dollars:.2f}',
                'timestamp': datetime.datetime.now().isoformat(),
                'raw_response': data
            })
        else:
            return jsonify({
                'status': 'error',
                'error': f'Kalshi API returned status {response.status_code}',
                'response': response.text
            }), response.status_code

    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': f'Configuration error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Unexpected error: {str(e)}'
        }), 500
