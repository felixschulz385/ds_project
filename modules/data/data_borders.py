"""
This class downloads the GADM boundary data for Germany
"""

from modules.data.data_abstract import data_abstract
from urllib.request import urlretrieve
import geopandas as gpd

class data_borders(data_abstract):
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders"):
        self.storage_directory = storage_directory
    
    def query(self, spatial_bounds = "available", temporal_bounds = "available", crs = 25833):
        
        print("Downloading...")
        for level in range(5):
            urlretrieve(f"https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_DEU_{level}.json",
                        f"{self.storage_directory}/gadm41_DEU_{level}.json")
            
        print("Reprojecting...")
        for level in range(5):
            # import the downloaded file, reproject it and export it
            gpd.read_file(f"{self.storage_directory}/gadm41_DEU_{level}.json").\
                to_crs(f"EPSG:{crs}"). \
                    to_file(f"{self.storage_directory}/gadm41_DEU_{level}.json", driver="GeoJSON")
            
        print("--- Download complete ---")