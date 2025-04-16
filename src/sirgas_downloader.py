import requests
import gzip
import shutil

class sirgas_downloader():
    def __init__(self):
        self.multianual_coord_url = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.CRD.gz"
        self.multianual_speed_url = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.VEL.gz"
    def decompress(self, filename):
        out_filename = filename.replace('.gz','')
        with gzip.open(filename, 'rb') as f_in:
            with open(out_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return out_filename

    def download(self, url):
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                    f.write(chunk)
        return local_filename

if __name__ == "__main__":
    test_obj = sirgas_downloader()
    saved_file_name = test_obj.download(test_obj.multianual_coord_url)
    test_obj.decompress(saved_file_name)