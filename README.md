# Weather API

A simple Flask-based weather API service that provides endpoints for weather data retrieval and processing.

## Features

- RESTful API endpoints
- Health check monitoring
- Dockerized deployment
- CI/CD pipeline with GitHub Actions

## API Endpoints

- `GET /` - Hello world endpoint with service status
- `GET /health` - Health check endpoint

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