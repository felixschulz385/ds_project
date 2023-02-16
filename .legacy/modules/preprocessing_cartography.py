from modules.preprocessing.preprocessing_abstract import preprocessing_abstract 
from geopandas import read_file
import fiona
fiona.supported_drivers["NAS"] = "raw"
from geocube.api.core import make_geocube

class preprocessing_cartography(preprocessing_abstract):
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/cartography"):
        self.storage_directory = storage_directory
    
    def preprocess(self):
        
        print("Preprocessing settlements...")
        # read in the data
        shapes = read_file(f"{self.storage_directory}/raw/BDA_41010.xml")
        
        # creating a buffer around each shape for the distances of 0, 300, 600, 1000, 3000
        for buffer in [0, 300, 600, 1000, 3000]:
            tmp = shapes
            tmp["geometry"] = tmp["geometry"].apply(lambda x: x.buffer(buffer, resolution = 1, join_style = 2))
            
            # export to JSON
            tmp.to_file(f"{self.storage_directory}/processed/settlements_{buffer}m.json", driver="GeoJSON")
            
            # create a dummy that is '1 in each geometry - all others will be filled as 0 in the next step
            tmp["settlement"] = 1
            # rasterize the images and write a netCDF file
            make_geocube(tmp, measurements = ["settlement"], resolution = (-1e2, 1e2), fill = 0). \
                to_netcdf(f"{self.storage_directory}/processed/settlements_{buffer}m.nc")
            
        