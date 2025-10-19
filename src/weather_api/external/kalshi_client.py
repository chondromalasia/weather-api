import os
import base64
import requests
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

from src.weather_api.config.loader import Config


def load_private_key_from_env():
    """Load the private key from base64-encoded environment variable."""
    private_key_b64 = os.environ.get('KALSHI_PRIVATE_KEY')
    if not private_key_b64:
        raise ValueError("KALSHI_PRIVATE_KEY environment variable must be set")

    # Decode from base64
    private_key_pem = base64.b64decode(private_key_b64)

    return serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )


def create_signature(private_key, timestamp, method, path):
    """Create the request signature."""
    message = f"{timestamp}{method}{path}".encode('utf-8')
    signature = private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')


def get(private_key, api_key_id, path, base_url=None):
    """Make an authenticated GET request to the Kalshi API."""
    if base_url is None:
        config = Config()
        base_url = config.kalshi_config['base_url']

    timestamp = str(int(datetime.now().timestamp() * 1000))
    signature = create_signature(private_key, timestamp, "GET", path)

    headers = {
        'KALSHI-ACCESS-KEY': api_key_id,
        'KALSHI-ACCESS-SIGNATURE': signature,
        'KALSHI-ACCESS-TIMESTAMP': timestamp
    }

    return requests.get(base_url + path, headers=headers)


# Helper function to get configured client credentials
def get_kalshi_credentials():
    """Get Kalshi API credentials from environment variables."""
    api_key_id = os.environ.get('KALSHI_API_KEY_ID')
    if not api_key_id:
        raise ValueError("KALSHI_API_KEY_ID environment variable must be set")

    private_key = load_private_key_from_env()

    return private_key, api_key_id
