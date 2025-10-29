# Weather API

A simple Flask-based weather API service that provides endpoints for weather data retrieval and processing.

## Features

- RESTful API endpoints
- Health check monitoring
- Dockerized deployment
- CI/CD pipeline with GitHub Actions

## API Endpoints

### General Endpoints

#### `GET /`
Hello world endpoint with service status.

**Response:**
```json
{
  "message": "Hello World from Weather API!",
  "timestamp": "2025-10-29T12:00:00",
  "status": "running"
}
```

#### `GET /health`
Health check endpoint to verify service is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-29T12:00:00"
}
```

#### `GET /endpoints`
List all available API endpoints.

**Response:**
```json
{
  "endpoints": [...]
}
```

### Weather Forecast Endpoints

#### `GET /forecast/highs`
Get forecasted daily high temperatures for a specific location and provider.

**Query Parameters:**
- `location` (required) - Location identifier (e.g., "KNYC")
- `provider` (required) - Forecast provider name
- `cutoff` (optional) - Cutoff date in YYYY-MM-DD format (default: "2025-09-06")

**Example Request:**
```bash
curl "http://localhost:5000/forecast/highs?location=KNYC&provider=test_provider&cutoff=2025-09-06"
```

**Example Response:**
```json
{
  "location": "KNYC",
  "provider": "test_provider",
  "cutoff": "2025-09-06",
  "forecasted_highs": [
    {
      "date": "2025-09-07",
      "high_temp": 85.5
    }
  ]
}
```

#### `GET /forecast/providers`
Get list of distinct forecast providers.

**Example Response:**
```json
{
  "providers": ["provider1", "provider2"]
}
```

#### `GET /forecast/locations`
Get list of distinct forecast locations.

**Example Response:**
```json
{
  "locations": ["KNYC", "KLAX"]
}
```

### Weather Observation Endpoints

#### `GET /observations/highs`
Get observed daily high temperatures for a weather station.

**Query Parameters:**
- `station_id` (required) - Weather station identifier
- `service` (optional) - Observation service (default: "CLI")

**Example Request:**
```bash
curl "http://localhost:5000/observations/highs?station_id=KNYC&service=CLI"
```

**Example Response:**
```json
{
  "station_id": "KNYC",
  "service": "CLI",
  "observed_highs": [
    {
      "date": "2025-09-06",
      "high_temp": 83.0
    }
  ]
}
```

#### `GET /observations/latest`
Get the most recent observation for a weather station.

**Query Parameters:**
- `station_id` (required) - Weather station identifier
- `service` (optional) - Observation service (default: "CLI")

**Example Request:**
```bash
curl "http://localhost:5000/observations/latest?station_id=KNYC&service=CLI"
```

**Example Response:**
```json
{
  "station_id": "KNYC",
  "service": "CLI",
  "latest_observation": {
    "timestamp": "2025-10-29T12:00:00",
    "temperature": 75.5,
    "conditions": "Clear"
  }
}
```

#### `GET /observations/temperatures/max`
Get all maximum temperature observations for a weather station, ordered by timestamp (most recent first).

**Query Parameters:**
- `station_id` (required) - Weather station identifier (e.g., "KMIA")
- `service` (optional) - Observation service (default: "CLI")

**Example Request:**
```bash
curl "http://localhost:5000/observations/temperatures/max?station_id=KMIA&service=CLI"
```

**Example Response:**
```json
{
  "station_id": "KMIA",
  "service": "CLI",
  "count": 2,
  "observations": [
    {
      "timestamp": "2025-10-29T14:00:00",
      "station_id": "KMIA",
      "measurement_type": "temperature",
      "observation_type": "max",
      "value": 85.5,
      "service": "CLI"
    },
    {
      "timestamp": "2025-10-28T14:00:00",
      "station_id": "KMIA",
      "measurement_type": "temperature",
      "observation_type": "max",
      "value": 83.2,
      "service": "CLI"
    }
  ]
}
```

### Kalshi Integration Endpoints

#### `GET /kalshi/balance`
Get portfolio balance from Kalshi trading platform.

**Environment Variables Required:**
- `KALSHI_PRIVATE_KEY` - Private key for authentication
- `KALSHI_API_KEY_ID` - API key identifier

**Example Response:**
```json
{
  "status": "success",
  "balance": 1000.50
}
```

### Error Responses

All endpoints return consistent error responses:

**400 Bad Request** - Missing or invalid parameters
```json
{
  "error": "Missing required parameter: location"
}
```

**500 Internal Server Error** - Database or server errors
```json
{
  "error": "Database error: connection failed"
}
```

## Quick Start

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

### Docker

Build and run with Docker:

```bash
docker build -t weather-api .
docker run -p 5000:5000 weather-api
```

## Deployment

The application uses GitHub Actions for automated CI/CD:

- Tests run on every push and pull request
- Docker images are built and pushed to Docker Hub on main branch pushes
- Multi-platform support (linux/amd64, linux/arm64)

## Environment

- Python 3.11
- Flask 3.0.0
- Docker for containerization