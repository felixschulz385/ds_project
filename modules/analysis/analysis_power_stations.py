from modules.analysis.analysis_abstract import analysis_abstract 
import re
import pandas as pd
import geopandas as gpd

class analysis_power_stations(analysis_abstract): #
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
    
    def analyze(self, polygons, substations, municipalities):
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
        
        # read the data on municipalities
        municipalities_polygons = gpd.read_file(municipalities)
        
        # a function to get the minimum distance to any substation
        def worker(x):
            if x is not None:
                # get a copy of all grid connections
                tmp = grid_connections.copy()
                # compute distances
                tmp["distance_substation"] = tmp.distance(x)
                # get the three closest substations
                tmp = tmp.iloc[tmp["distance_substation"].sort_values().head(3).index,:]
                # compile a Data Frame
                return pd.DataFrame(tmp.loc[:,["substation", "id", "geometry", "tags", "distance_substation"]].rename(columns = {"id": "id_substation", "geometry": "point_substation", "tags": "tags_substation"}).reset_index(drop = True))

        # apply the function on all polygons
        substations_stats = pd.concat({idx: worker(x) for idx, x in enumerate(driveways_polygons.geometry)})

        # get shortest distance for computation of score
        driveways_polygons['distance_substation'] = substations_stats.groupby(level = 0).agg({"distance_substation": "first"})
        
        # get state name
        state_name = driveways_polygons.link_id.str.extract(r"(\w\w(?=_))")[0].unique()[0]
        
        # write the results for further analysis to disk
        driveways_polygons.loc[:,["link_id", "id", "distance_substation"]].to_csv(self.storage_directory + "/analysis/" + state_name + "_ps_distances.csv", index = False)
        
        # merge link_id, id and geometry of polygon back into stats
        driveways_auxiliary = pd.merge(driveways_polygons.loc[:,["link_id", "id", "geometry"]].reset_index(names = "link_idx"), substations_stats.reset_index(0, names = "link_idx"), on = "link_idx")
        
        # get centroids of driveways
        driveways_auxiliary["geometry"] = driveways_auxiliary.centroid
        
        # spatial join with borders of municipalities to get names
        driveways_auxiliary = driveways_auxiliary.set_geometry("point_substation").rename(columns = {"geometry": "point_driveway"}).sjoin(municipalities_polygons.loc[:,["NAME_4", "geometry"]], how = "left", predicate = "intersects")
        
        # project
        driveways_auxiliary = driveways_auxiliary.set_geometry("point_driveway").to_crs(4326).set_geometry("point_substation").to_crs(4326)
        
        # extract coordinates
        def worker(x):
            tmp = re.compile(r"(\d+.\d+)").findall(str(x))
            return pd.Series([tmp[1], tmp[0]], index = ["lat", "lon"])
        driveways_auxiliary[["lat_driveway", "lon_driveway"]] = driveways_auxiliary.point_driveway.apply(worker)
        driveways_auxiliary[["lat_substation", "lon_substation"]] = driveways_auxiliary.point_substation.apply(worker)
        
        # write auxiliary file to disk
        driveways_auxiliary.loc[:,["link_id", "id", "substation", "distance_substation", "lat_driveway", "lon_driveway", "lat_substation", "lon_substation", "NAME_4"]].rename(columns = {"NAME_4": "municipality"}).to_csv(self.storage_directory + "/analysis/" + state_name + "_ps_auxiliary.csv", index = False)
        
"""       
if __name__ == "__main__":
    analysis_power_stations = analysis_power_stations()
    analysis_power_stations.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson", 
                                    "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_substations.geojson",
                                    "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders/gadm41_DEU_4.json")
"""