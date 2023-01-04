from modules.data.data_abstract import data_abstract
from urllib.request import urlretrieve
from zipfile import ZipFile
import xarray
import rioxarray

class data_cartography(data_abstract):
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/SARAH"):
        self.storage_directory = storage_directory
    
    def query(self, spatial_bounds = "available", temporal_bounds = "available", crs = 25833):
        
        print("Downloading...")
        urlretrieve("http://re.jrc.ec.europa.eu/pvg_download/sarahdata/gh_0_year_sarah.zip",
            self.storage_directory + "/raw/gh_0_year_sarah.zip")

        print("Extracting...")
        with ZipFile(self.storage_directory + "/raw/gh_0_year_sarah.zip", "r") as zip_ref:
            zip_ref.extractall(self.storage_directory + "/raw")
            
        print("Reorganizing...")
        with rioxarray.open_rasterio(self.storage_directory + "/raw/gh_0_year.asc") as dat:
            dat.rio.write_nodata(-1, inplace = True)
            dat = dat.rio.set_crs("EPSG:4326")
            dat = dat.rio.reproject("EPSG:25833")
            dat.to_netcdf(self.storage_directory + "/processed/gh_0_year.nc")
        
        print("--- Download complete ---")