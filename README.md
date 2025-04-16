# SIRGAS API

A FastAPI-based REST API for accessing SIRGAS (Sistema de Referência Geocêntrico para as Américas) coordinate data.

## Project Overview

This API provides access to SIRGAS reference station data, allowing users to:
- Query SIRGAS stations with geographic filtering
- Retrieve station coordinate data in GeoJSON format
- Filter stations by country or coordinate boundaries

## Architecture

The project follows a simple, modular structure:

- `src/api.py`: Main FastAPI application with endpoint definitions
- `src/sirgas_downloader.py`: Handles downloading and decompressing SIRGAS data files
- `src/sirgas_dataframe.py`: Converts raw SIRGAS data into GeoDataFrames

The API automatically downloads and processes the latest SIRGAS data on first request, caching it for subsequent use.

## API Endpoints

- **GET /** - API root - provides basic info about the API
- **GET /stations** - Get all SIRGAS stations with optional filtering
  - Parameters:
    - `limit`: Maximum number of stations to return (default: 100)
    - `offset`: Number of stations to skip (default: 0)
    - `min_lat, max_lat, min_lon, max_lon`: Coordinate boundary filters

## Installation

1. Clone the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   uvicorn src.api:app --reload
   ```

## Testing the API

You can test the API using the following Python script:

```python
import requests
import json

# Base URL - Update this with your actual API URL
BASE_URL = "https://sirgas-api.onrender.com"

def print_response(response):
    """Print response in a readable format"""
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")

def test_api():
    """Test the SIRGAS API root and stations endpoints"""
    # Test root endpoint
    print("\nTesting root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    
    # Test stations endpoint
    print("\nTesting stations endpoint...")
    response = requests.get(f"{BASE_URL}/stations", params={"limit": 10})
    print_response(response)

if __name__ == "__main__":
    test_api()
```

## Deployment

The API is deployed on Render and can be accessed at: https://sirgas-api.onrender.com