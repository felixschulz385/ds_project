#from modules.analysis.analysis_abstract import analysis_abstract 
import pandas as pd
import geopandas as gpd

class analysis_power_stations(): #
    """
    A class implementing the analysis of distance to nearest power station
    
    Args:
        storage_directory (str): The path to the storage directory of OSM data
        
    Methods:
        analyze: Calculates closest distances to power substations for polygons
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM"):
        self.storage_directory = storage_directory
    
    def analyze(self, polygons, substations):
        """
        
        A function calculating the closest distance (in meters) to any power substation.
        The result is written to disk.

        Args:
            polygons (str): The path to the GeoJSON listing polygons for which distances are to be calculated
            substations (str): The path to the GeoJSON listing all power substations

        """
        
        # read the data on driveways
        driveways_polygons = gpd.read_file(polygons)
        
        # read the data on substations
        grid_connections = gpd.read_file(substations)
        
        # a function to get the minimum distance to any substation
        def worker(x):
            if x is not None:
                return grid_connections.distance(x).min()  
            
        # apply the function on all polygons
        driveways_polygons["distance"] = driveways_polygons.geometry.apply(worker)
        
        # get state name
        state_name = driveways_polygons.link_id.str.extract(r"(\w\w(?=_))")[0].unique()[0]
        
        # write the results to disk
        driveways_polygons.loc[:,["link_id", "id", "distance"]].to_csv(self.storage_directory + "/analysis/" + state_name + "_ps_distances.csv")
        
"""       
if __name__ == "__main__":
    analysis_power_stations = analysis_power_stations()
    analysis_power_stations.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson", 
                                    "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_substations.geojson")
"""