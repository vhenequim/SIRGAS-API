import requests
import gzip
import shutil

# Constants
MULTIANUAL_COORD_URL = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.CRD.gz"
MULTIANUAL_SPEED_URL = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.VEL.gz"

def decompress_file(filename):
    """Decompress a gzip file and return the output filename"""
    out_filename = filename.replace('.gz','')
    with gzip.open(filename, 'rb') as f_in:
        with open(out_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return out_filename

def download_file(url):
    """Download a file from the given URL and return the local filename"""
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def get_sirgas_coord_url():
    """Return the URL for SIRGAS coordinate data"""
    return MULTIANUAL_COORD_URL

def get_sirgas_speed_url():
    """Return the URL for SIRGAS speed data"""
    return MULTIANUAL_SPEED_URL

