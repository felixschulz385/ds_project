#from modules.analysis.analysis_abstract import analysis_abstract 
import os, re
import pandas as pd
import geopandas as gpd

class analysis_combine(): #analysis_abstract
    """
    A class combining all previously gathered data for use in the final dashboard
    
    Args:
        storage_directory (str): The path to the storage directory of OSM data
        
    Methods:
        analyze: Calculates average 
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data"):
        self.storage_directory = storage_directory
    
    def analyze(self, polygons, out_dir):
        """
        
        A function getting the best possible value for yearly irradiation from the SARAH data for each polygon

        Args:
            polygons (str): The path to the GeoJSON containing all turnoff polygons
            out_dir (str): The path to write the resulting file to
            
        """
        
        # get the driveway boundaries
        driveways = gpd.read_file(polygons)
        
        # get state name
        state_name = driveways.link_id.str.extract(r"(\w\w(?=_))")[0].unique()[0]

        ##
        # get and combine analysis data
        if os.path.exists(f"{self.storage_directory}/SARAH/analysis/{state_name}_irradiation.csv"):
            irradiation_data = pd.read_csv(f"{self.storage_directory}/SARAH/analysis/{state_name}_irradiation.csv")
            driveways = pd.merge(driveways, irradiation_data, on = ["link_id", "id"])
        if os.path.exists(f"{self.storage_directory}/OSM/analysis/{state_name}_ps_distances.csv"):
            ps_distances = pd.read_csv(f"{self.storage_directory}/OSM/analysis/{state_name}_ps_distances.csv")
            driveways = pd.merge(driveways, ps_distances, on = ["link_id", "id"])
        if os.path.exists(f"{self.storage_directory}/imagery/analysis/{state_name}_land_cover.csv"):
            land_cover = pd.read_csv(f"{self.storage_directory}/imagery/analysis/{state_name}_land_cover.csv")
            driveways = pd.merge(driveways, land_cover, on = ["link_id", "id"])
        if os.path.exists(f"{self.storage_directory}/DGM/analysis/{state_name}.csv"):
            terrain_suitability = pd.read_csv(f"{self.storage_directory}/DGM/analysis/{state_name}.csv")
            driveways = pd.merge(driveways, terrain_suitability, on = ["link_id", "id"])
        
        # export the results as polygons
        driveways.to_file(f"{out_dir}/{state_name}_final.json")

#"""       
if __name__ == "__main__":
    c_analysis_combine = analysis_combine()
    c_analysis_combine.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson",
                               "/pfs/data5/home/tu/tu_tu/tu_zxobe27/ds_project/ds_project/modules/dashboard/data")
#"""