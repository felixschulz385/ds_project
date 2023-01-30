from modules.analysis.analysis_abstract import analysis_abstract 
import re
import pandas as pd
import geopandas as gpd
import xarray
import rioxarray

class analysis_irradiation(analysis_abstract): #
    """
    A class implementing the analysis of average annual irradiation in W/m^2
    
    Args:
        storage_directory (str): The path to the storage directory of OSM data
        
    Methods:
        analyze: Calculates average 
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/SARAH"):
        self.storage_directory = storage_directory
    
    def analyze(self, polygons):
        """
        
        A function getting the best possible value for yearly irradiation from the SARAH data for each polygon

        Args:
            polygons (str): The path to the GeoJSON containing all turnoff polygons
            
        """
        
        # get the driveway boundaries
        driveways = gpd.read_file(polygons)
        
        # get state name
        state_name = driveways.link_id.str.extract(r"(\w\w(?=_))")[0].unique()[0]

        # get the irradiation data
        irradiation = rioxarray.open_rasterio(f"{self.storage_directory}/processed/gh_0_year.nc", mask_and_scale = True)
        
        # define a function getting the nearest measurement for irradiation per turnoff
        def worker(x):
            if x != None:
                return irradiation.sel(x = list(x.coords)[0][0], y = list(x.coords)[0][1], method = "nearest").values[0]
        
        # apply the function on all turnoffs
        driveways["irradiation"] = driveways.centroid.apply(worker)  
        
        # export the results
        driveways.loc[:,["link_id", "id", "irradiation"]].to_csv(f"{self.storage_directory}/analysis/{state_name}_irradiation.csv")

"""       
if __name__ == "__main__":
    analysis_irradiation = analysis_irradiation()
    analysis_irradiation.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson")
"""