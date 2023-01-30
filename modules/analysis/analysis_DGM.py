from modules.analysis.analysis_abstract import analysis_abstract

import os
import re
import xarray
import rioxarray
import pandas as pd
import geopandas as gpd

class analysis_DGM(analysis_abstract): #
    """
    A class implementing the analysis of height profiles in highway turnoffs

    Args:
        storage_directory (str): The path to the storage directory of DGM data
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/DGM"):
        
        self.storage_directory = storage_directory
        
    def analyze(self, imagery, polygons, inset = 7, crs = 25833):
        """
        
        A function calculating a measurement of terrain roughness in highway turnoffs
        The result is written to disk.

        Args:
            imagery (str): The path to the NetCDF file containing information on BB standard grids containing a turnoff
            polygons (str): The path to the GeoJSON listing all turnoff polygons in the respective state

        """
        
        # get the driveway boundaries
        driveways = gpd.read_file(polygons)
        
        # handle single image
        if not isinstance(imagery, list):
            imagery = [imagery]
        
        for idx, image in enumerate(imagery):
            
            print(f"--- Processing image {idx + 1} ---")
            
            # read the grids from the image
            grids = xarray.open_dataset(image, drop_variables = ["red", "green", "blue"]).attrs["grids"]
            
            # handle single grid
            if not isinstance(grids, list):
                grids = [grids]
            
            # read and combine the height profiles
            xr = xarray.combine_by_coords([rioxarray.open_rasterio(self.storage_directory + "/raw/dgm_" + grid.replace("_", "-")  + ".xyz") for grid in grids])
            xr.rio.write_crs("25833", inplace = True)
            
            # get road ID and state name
            driveway_id = re.search(re.compile("(?<=raw/)\w\w_\w\w_\w\w\w\w"), image).group(0)
            state_name = re.search(re.compile("(?<=raw/)\w\w"), image).group(0)
            
            ###
            # TERRAIN SUITABILITY DEFINITION
            ###
            def worker(x):
                # check if there is any geometry
                if x is not None:
                    # calculate the inset
                    inset_geometry = x.buffer(-inset)
                    # check if any area remains
                    if inset_geometry.area != 0:
                        try:
                            # cut the height profile with the polygon
                            tmp = xr.rio.clip([inset_geometry])
                            # return the terrain suitability measurement
                            return (1 - (tmp.std() / (tmp.max() - tmp.min()))).values
                        except:
                            return None
            
            # apply definition to all polygons
            driveways_out = driveways.copy().loc[driveways.link_id == driveway_id,["link_id", "id"]]
            driveways_out["terrain_suitability"] = driveways.loc[driveways.link_id == driveway_id, "geometry"].apply(worker)

            # get existing measurements
            if os.path.isfile(self.storage_directory + "/analysis/" + state_name + ".csv"):
                tmp = pd.read_csv(self.storage_directory + "/analysis/" + state_name + ".csv")
                # export table with mapping from link_id to terrain_suitability
                pd.concat([tmp[tmp.link_id != driveway_id], driveways_out]).\
                    to_csv(self.storage_directory + "/analysis/" + state_name + ".csv", index = False) 
            else:
                driveways_out.to_csv(self.storage_directory + "/analysis/" + state_name + ".csv", index = False)      

"""       
if __name__ == "__main__":
    analysis_DGM = analysis_DGM()
    analysis_DGM.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/BB_ML_0001_2017-08-29.nc", 
                         "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson")
"""