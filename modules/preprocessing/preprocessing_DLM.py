#from modules.preprocessing.preprocessing_abstract import preprocessing_abstract

import os
import re
import xarray
import rioxarray
import pandas as pd
import geopandas as gpd

class preprocessing_DLM(): #preprocessing_abstract
    """_summary_

    Args:
        preprocessing_abstract (_type_): _description_
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/DGM"):
        
        self.storage_directory = storage_directory
        
    def preprocess(self, imagery, polygons, crs = 25833):
        
        # get the driveway boundaries
        polygons = gpd.read_file(polygons)
        
        # handle single image
        if not isinstance(imagery, list):
            imagery = [imagery]
        
        for idx, image in enumerate(imagery):
            
            print(f"--- Processing image {idx + 1} ---")
            
            # read the grids from the image
            grids = xarray.open_dataset(image, drop_variables = ["red", "green", "blue"]).attrs["grids"]
            
            # read and combine the height profiles
            xr = xarray.combine_by_coords([rioxarray.open_rasterio(self.storage_directory + "/raw/dgm_" + grid.replace("_", "-")  + ".xyz") for grid in grids])
            xr.rio.write_crs("25833", inplace = True)
            
            # get road ID and state name
            id = re.search(re.compile("(?<=imagery/)\w\w_\w\w_\w\w\w\w"), "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/BB_ML_0001_2017-06-02.nc").group(0)
            state_name = re.search(re.compile("(?<=imagery/)\w\w"), "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/BB_ML_0001_2017-06-02.nc").group(0)
            
            ###
            # TERRAIN SUITABILITY DEFINITION
            ###
            def worker(x):
                tmp = xr.rio.clip([x])
                return (1 - (tmp.std() / (tmp.max() - tmp.min()))).values
            
            # apply definition to all polygons
            polygons.loc[polygons.link_id == id, "terrain_suitability"] = polygons[polygons.link_id == id].geometry.apply(worker)

            # get existing measurements
            if os.path.isfile(self.storage_directory + "/" + state_name + ".csv"):
                tmp = pd.read_csv(self.storage_directory + "/" + state_name + ".csv")
                # export table with mapping from link_id to terrain_suitability
                pd.concat([tmp[tmp.link_id != id], polygons.loc[polygons.link_id == id, ["link_id", "id", "terrain_suitability"]]]).\
                    to_csv(self.storage_directory + "/" + state_name + ".csv", index = False) 
            else:
                polygons[["link_id", "id", "terrain_suitability"]].\
                    to_csv(self.storage_directory + "/" + state_name + ".csv", index = False) 
            
            

# """       
if __name__ == "__main__":
    preprocessor_DLM = preprocessing_DLM()
    preprocessor_DLM.preprocess("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/BB_ML_0001_2017-08-29.nc", 
                                "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson")
#"""