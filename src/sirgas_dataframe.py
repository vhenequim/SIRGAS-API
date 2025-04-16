import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def parse_sirgas_file(filepath, target_epsg=4674):
    """
    Parse SIRGAS coord file into GeoDataFrame
    
    Args:
        filepath: Path to the SIRGAS file
        target_epsg: Target EPSG code for  transformation (default: 4674 - SIRGAS 2000)
        
    Returns:
        GeoDataFrame with SIRGAS station coordinates
    """
    # Read fixed-width file format with specific encoding
    data = pd.read_fwf(filepath, skiprows=17, encoding='latin-1')
    
    # Create spatial points from XYZ coordinates
    spatial_data = gpd.GeoDataFrame(
        data, 
        geometry=gpd.points_from_xy(data['X[m]'], data['Y[m]'], data['Z[m]'], crs="EPSG:9378")
    )
    
    # Transform to target coordinate system
    return spatial_data.to_crs(f"EPSG:{target_epsg}")
