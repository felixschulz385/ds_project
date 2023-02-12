#from modules.analysis.analysis_abstract import analysis_abstract 
import os, re
import numpy as np
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
    
    def analyze(self, polygons, municipalities, economic_model, out_dir):
        """
        
        A function getting the best possible value for yearly irradiation from the SARAH data for each polygon

        Args:
            polygons (str): The path to the GeoJSON containing all turnoff polygons
            out_dir (str): The path to write the resulting file to
            
        """
        
        # get the driveway boundaries
        driveways = gpd.read_file(polygons)
        
        # get the municipality boundaries
        municipalities = gpd.read_file(municipalities)
        
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
            terrain_suitability = pd.read_csv(f"{self.storage_directory}/DGM/analysis/{state_name}_12.csv")
            driveways = pd.merge(driveways, terrain_suitability, on = ["link_id", "id"])

        ##
        # compute central variables
        # apply buffer to polygons
        driveways['geometry'] = driveways.geometry.apply(lambda x: x.buffer(-12) if x is not None else None)
        # get the overall area
        driveways['suitable_area'] = driveways['geometry'].area
        # get the irradiation score
        driveways["irradiation_score"] = driveways.irradiation.apply(lambda x: (driveways.irradiation.max() - x) / (driveways.irradiation.max() - driveways.irradiation.min()))
        driveways["irradiation_rank"] = driveways.irradiation_score.rank(method = "dense", ascending = False)
        # get the distance score
        driveways["distance_score"] = driveways["distance_substation"].apply(lambda x: (driveways["distance_substation"].max() - x) / (driveways["distance_substation"].max() - driveways["distance_substation"].min()))
        driveways["distance_rank"] = driveways.distance_score.rank(method = "dense", ascending = False)
        # get the terrain score
        driveways["terrain_score"] = 1 - (driveways["terrain_roughness"] / 90)
        driveways["terrain_rank"] = driveways.terrain_score.rank(method = "dense", ascending = False)

        # get the overall score
        driveways["overall_score"] = (economic_model["irradiation"] * driveways["irradiation_score"] + 
                            economic_model["distance"] * driveways["distance_score"] +
                            economic_model["terrain"] * driveways["terrain_score"])
        driveways["overall_rank"] = driveways.overall_score.rank(method = "dense", ascending = False)
        
        # add municipality information
        driveways = driveways.sjoin(municipalities[["geometry", "NAME_4"]], predicate = "intersects")
        
        # fix names
        driveways.NAME_4 = driveways.NAME_4.replace({r"BernaubeiBerlin": "Bernau bei Berlin",
                                                     r"([a-zß])([A-Z]|\()": r"\1 \2"}, regex=True)
        
        # export the results as polygons
        driveways.to_crs(4326).to_file(f"{out_dir}/{state_name}_polygons_final.json")
        
        ##
        # merge and aggregate for kreise
        
        # Define a function to compute the weighted mean:
        def wm(x): 
            if (tmp.loc[x[~x.isna()].index, "suitable_area"].sum() != 0):
                return np.average(x[~x.isna()], weights = tmp.loc[x[~x.isna()].index, "suitable_area"])
        
        # read the kreis data
        kreis = gpd.read_file(self.storage_directory + "/borders/gadm41_DEU_2.json").to_crs(25833)
        # filter for brandenburg
        kreis = kreis.loc[(kreis.HASC_2.str.extract(r'((?<=DE\.)..(?=\.))') == state_name)[0], :]
        # get mean statistics
        tmp = gpd.sjoin(kreis, driveways, how = 'inner', predicate = 'intersects').reset_index()
        tmp["link_id_individual"] = tmp.link_id + "_" + str(tmp.id)
        #
        kreis_stats = tmp.groupby('NAME_2').agg({'link_id_individual': "count",
                                                'terrain_score': wm, 
                                                'irradiation_score': wm, 
                                                'distance_score': wm,
                                                'overall_score': wm}).reset_index()
        # export
        pd.merge(kreis[["NAME_2", "HASC_2", "geometry"]], kreis_stats, left_on = 'NAME_2', right_on = 'NAME_2', how = 'left').to_crs(4326).to_file(f"{out_dir}/{state_name}_kreis_final.json", driver = 'GeoJSON')
        
        ##
        # merge and aggregate for gemeinde
        
        # read the kreis data
        gemeinde = gpd.read_file(self.storage_directory + "/borders/gadm41_DEU_3.json").to_crs(25833)
        # filter for brandenburg
        state_name_long = kreis.NAME_1.unique()[0]
        gemeinde = gemeinde[gemeinde['NAME_1'] == state_name_long]
        # get mean statistics
        tmp = gpd.sjoin(gemeinde, driveways, how = 'inner', predicate = 'intersects').reset_index()
        tmp["link_id_individual"] = tmp.link_id + "_" + str(tmp.id)
        gemeinde_stats = tmp.groupby('NAME_3').agg({'suitable_area': "sum",
                                                    'link_id_individual': "count",
                                                'terrain_score': wm, 
                                                'irradiation_score': wm, 
                                                'distance_score': wm,
                                                'overall_score': wm}).reset_index()
        pd.merge(gemeinde[["NAME_3", "geometry"]], gemeinde_stats, left_on = 'NAME_3', right_on = 'NAME_3', how = 'left').to_crs(4326).to_file(f"{out_dir}/{state_name}_gemeinde_final.json", driver = 'GeoJSON')

#"""       
if __name__ == "__main__":
    c_analysis_combine = analysis_combine()
    c_analysis_combine.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson",
                               "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders/gadm41_DEU_4.json",
                               {"irradiation": 0.2, "distance": 0.25, "terrain": .05},
                               "/pfs/data5/home/tu/tu_tu/tu_zxobe27/ds_project/ds_project/modules/dashboard/data")
#"""