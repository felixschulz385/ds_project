from modules.analysis.analysis_abstract import analysis_abstract 
import os, re
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray
import rioxarray
import PIL

class analysis_power_stations(analysis_abstract): #
    """
    A class implementing the analysis of land cover within turnoff polygons based on a neural network
    
    Args:
        storage_directory (str): The path to the storage directory of OSM data
        
    Methods:
        analyze: Calculates relative land cover within the turnoff
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery"):
        self.storage_directory = storage_directory
    
    def analyze(self, imagery, polygons, model):
        """
        
        A function calculating relative land cover for a set of images given polygons and a model for prediction

        Args:
            imagery (str): The paths to the files containing imagery (can be either .jpg or .nc)
            polygons (str): The path to the GeoJSON containing all turnoff polygons
            model (str): The path to the stored model for prediction

        """
        
        # get the driveway boundaries
        driveways = gpd.read_file(polygons)
        
        # handle single image
        if not isinstance(imagery, list):
            imagery = [imagery]
        
        for idx, image in enumerate(imagery):
            
            print(f"--- Processing image {idx + 1} ---")
            
            # get file type
            file_type = re.compile("(?<=\.).*$").search(image).group(0)
            
            # if file is larger than 10GB, get jpg instead
            if ((os.path.getsize(image) > 10e12) & file_type == "nc"):
                image = re.compile("(?<=\.)nc").sub("jpg", image)
                
            if file_type == "jpg":
                # read jpg
                image = np.asarray(PIL.open(image))
            
            elif file_type == "nc":
                image = rioxarray.open_rasterio(image)
            
            else:
                print("!!! File type not compatible !!!")
                continue
            
            # get road ID and state name
            driveway_id = re.search(re.compile("(?<=raw/)\w\w_\w\w_\w\w\w\w"), image).group(0)
            state_name = re.search(re.compile("(?<=raw/)\w\w"), image).group(0)
            
            ###
            # GET AGGREGATE MEASUREMENTS
            ###
            def worker(x):
                # predict and aggregate
                return high_vegetation, low_vegetation, buildings
            
            # apply definition to all polygons
            driveways_out = driveways.copy().loc[driveways.link_id == driveway_id,["link_id", "id"]]
            driveways_out["high_vegetation", "low_vegetation", "buildings"] = driveways.loc[driveways.link_id == driveway_id, "geometry"].apply(worker)

            # get existing measurements
            if os.path.isfile(self.storage_directory + "/analysis/" + state_name + ".csv"):
                tmp = pd.read_csv(self.storage_directory + "/analysis/" + state_name + ".csv")
                # export table with mapping from link_id to land cover
                pd.concat([tmp[tmp.link_id != driveway_id], driveways_out]).\
                    to_csv(self.storage_directory + "/analysis/" + state_name + ".csv", index = False) 
            else:
                # export table with mapping from link_id to land cover
                driveways_out.to_csv(self.storage_directory + "/analysis/" + state_name + ".csv", index = False)      

"""       
if __name__ == "__main__":
    analysis_DGM = analysis_DGM()
    analysis_DGM.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/BB_ML_0001_2017-08-29.nc", 
                         "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson")
"""