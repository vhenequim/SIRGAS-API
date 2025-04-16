import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def read_sirgas_dataframe(filename, epsg=4674):
    df = pd.read_fwf(filename, skiprows=17, encoding='latin-1') #9378
    gdf = gpd.GeoDataFrame(
        df, 
        geometry = gpd.points_from_xy(df['X[m]'], df['Y[m]'], df['Z[m]'], crs="EPSG:9378" )
    )   
    return gdf.to_crs(f"EPSG:{epsg}")

if __name__ == "__main__":
    from sirgas_downloader import sirgas_downloader
    test_obj = sirgas_downloader()

    saved_file_name = test_obj.download(test_obj.multianual_coord_url)
    decompressed_crd_file = test_obj.decompress(saved_file_name)    
    
    df = read_sirgas_dataframe(decompressed_crd_file)
    df.plot()
    plt.show()
    print(df)