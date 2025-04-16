from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd
import geopandas as gpd
from datetime import datetime

from src.sirgas_downloader import sirgas_downloader
from src.sirgas_dataframe import read_sirgas_dataframe

app = FastAPI(title="SIRGAS API", description="API for SIRGAS coordinate data")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store the dataframe
_dataframe = None

def get_dataframe():
    """Load dataframe if not already loaded"""
    global _dataframe
    if _dataframe is None:
        try:
            downloader = sirgas_downloader()
            saved_file_name = downloader.download(downloader.multianual_coord_url)
            decompressed_crd_file = downloader.decompress(saved_file_name)
            _dataframe = read_sirgas_dataframe(decompressed_crd_file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading SIRGAS data: {str(e)}")
    return _dataframe

@app.get("/", tags=["Info"])
async def root():
    """API root - provides basic info"""
    return {"message": "SIRGAS API", "endpoints": ["/stations", "/stations/{station_id}"]}

@app.get("/stations", tags=["Stations"])
async def get_stations(
    limit: int = Query(100, description="Maximum number of stations to return"),
    offset: int = Query(0, description="Number of stations to skip"),
    country: Optional[str] = Query(None, description="Filter by country code"),
    min_lat: Optional[float] = Query(None, description="Minimum latitude"),
    max_lat: Optional[float] = Query(None, description="Maximum latitude"),
    min_lon: Optional[float] = Query(None, description="Minimum longitude"),
    max_lon: Optional[float] = Query(None, description="Maximum longitude"),
):
    """Get all SIRGAS stations with optional filtering"""
    df = get_dataframe()
    
    # Apply filters
    filtered_df = df.copy()
    
    if country:
        filtered_df = filtered_df[filtered_df['COD_PAIS'] == country]
    
    # Filter by coordinates if needed
    if min_lat is not None:
        filtered_df = filtered_df[filtered_df.geometry.y >= min_lat]
    if max_lat is not None:
        filtered_df = filtered_df[filtered_df.geometry.y <= max_lat]
    if min_lon is not None:
        filtered_df = filtered_df[filtered_df.geometry.x >= min_lon]
    if max_lon is not None:
        filtered_df = filtered_df[filtered_df.geometry.x <= max_lon]
    
    # Apply pagination
    paginated_df = filtered_df.iloc[offset:offset + limit]
    
    # Convert to geojson for proper serialization
    geojson = paginated_df.to_json()
    
    return {
        "total": len(filtered_df),
        "limit": limit,
        "offset": offset,
        "data": geojson
    }

@app.get("/stations/{station_id}", tags=["Stations"])
async def get_station(station_id: str):
    """Get a specific SIRGAS station by its ID"""
    df = get_dataframe()
    
    # Find station by ID
    station = df[df['COD'] == station_id]
    
    if len(station) == 0:
        raise HTTPException(status_code=404, detail=f"Station with ID {station_id} not found")
    
    # Convert to geojson
    geojson = station.to_json()
    
    return {"data": geojson}

@app.get("/countries", tags=["Metadata"])
async def get_countries():
    """Get list of countries with stations"""
    df = get_dataframe()
    countries = df['COD_PAIS'].unique().tolist()
    return {"countries": countries}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 