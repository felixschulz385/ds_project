from modules.analysis.analysis_abstract import analysis_abstract

import os
import re
import xarray
import xrspatial
import rioxarray
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

class analysis_DGM(analysis_abstract): #
    """
    A class implementing the analysis of height profiles in highway turnoffs

    Args:
        storage_directory (str): The path to the storage directory of DGM data
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/DGM"):
        
        self.storage_directory = storage_directory
        
    def analyze(self, imagery, polygons, inset = 12, crs = 25833):
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
            xr = xarray.combine_by_coords([rioxarray.open_rasterio(self.storage_directory + "/raw/dgm_" + grid.replace("_", "-")  + ".xyz") for grid in grids]).squeeze("band")
            xr.rio.write_crs("25833", inplace = True)
            
            # get road ID and state name
            driveway_id = re.search(re.compile("(?<=raw/)\w\w_\w\w_\w\w\w\w"), image).group(0)
            state_name = re.search(re.compile("(?<=raw/)\w\w"), image).group(0)
            
            ###
            # TERRAIN SUITABILITY DEFINITION
            ###
            def worker(x):
                # check if there is any geometry
                if x.geometry is not None:
                    # calculate the inset
                    inset_geometry = x.geometry.buffer(-inset)
                    # check if any area remains
                    if inset_geometry.area != 0:
                        try:
                            # cut the height profile with the polygon
                            tmp = xr.rio.clip([inset_geometry])
                            
                            # produce an image of the height profile
                            fig, ax = plt.subplots()
                            xarray.plot.imshow(tmp.squeeze().drop_vars(["band", "spatial_ref"]), ax = ax, add_colorbar = False)
                            ax.axis('off')
                            fig.savefig(self.storage_directory + "/analysis/imagery/" + x.link_id + "_" + str(int(x.id)) + ".png", bbox_inches = "tight", transparent = True)
                            plt.close()
                            
                            # return the terrain suitability measurement
                            return pd.Series(np.stack([xrspatial.slope(tmp).std().values, tmp.max().values, tmp.min().values]))
                        except:
                            pass
                return pd.Series([None] * 3)
            
            # apply definition to all polygons
            driveways_out = driveways.copy().loc[driveways.link_id == driveway_id,["link_id", "id"]]
            driveways_out[["terrain_roughness", "terrain_high", "terrain_low"]] = driveways.loc[driveways.link_id == driveway_id, :].apply(worker, axis = 1)

            # get existing measurements
            if os.path.isfile(self.storage_directory + "/analysis/" + state_name + "_" + str(inset) + ".csv"):
                tmp = pd.read_csv(self.storage_directory + "/analysis/" + state_name + "_" + str(inset) + ".csv")
                # export table with mapping from link_id to terrain_suitability
                pd.concat([tmp[tmp.link_id != driveway_id], driveways_out]).\
                    to_csv(self.storage_directory + "/analysis/" + state_name + "_" + str(inset) + ".csv", index = False) 
            else:
                driveways_out.to_csv(self.storage_directory + "/analysis/" + state_name + "_" + str(inset) + ".csv", index = False)      

"""       
if __name__ == "__main__":
    analysis_DGM = analysis_DGM()
    analysis_DGM.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/raw/BB_ML_0001_2017-08-29.nc", 
                         "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson")
"""