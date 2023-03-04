#from modules.analysis.analysis_abstract import analysis_abstract 
import os, re, shutil
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
    
    def analyze(self, polygons, economic_model, out_dir):
        """
        
        A function getting the best possible value for yearly irradiation from the SARAH data for each polygon

        Args:
            polygons (str): The path to the GeoJSON containing all turnoff polygons
            out_dir (str): The path to write the resulting file to
            
        """
        
        # get the driveway boundaries
        driveways = gpd.read_file(polygons)
        
        # clean
        driveways.drop(columns = ["group", "access", "area", "bicycle", "bicycle_road", "bridge", "busway", "cycleway", "foot", "footway", "highway", "int_ref", "junction", "lanes", "lit", "maxspeed", "motorcar", "motorroad", "motor_vehicle", "name", "oneway", "overtaking", "path", "passing_places", "psv", "ref", "service", "segregated", "sidewalk", "smoothness", "surface", "tracktype", "tunnel", "turn", "width", "timestamp", "version", "tags", "osm_type", "group_id"], inplace = True)
        
        # get the municipality boundaries
        municipalities = gpd.read_file(self.storage_directory + "/borders/gadm41_DEU_3.json")
        
        # fix names
        municipalities["NAME_3"] = municipalities["NAME_3"].replace({r"BernaubeiBerlin": "Bernau bei Berlin",
                                                   r"BrandenburganderHavel": "Brandenburg an der Havel",
                                                   r"KönigsWusterhausen": "Königs Wusterhausen",
                                                   r"MärkischeHeide": "Märkische Heide",
                                                   r"NeuenhagenbeiBerlin": "Neuenhagen bei Berlin",
                                                   r"RüdersdorfbeiBerlin": "Rüdersdorf bei Berlin",
                                                   r"GranseeundGemeinden": "Gransee und Gemeinden",
                                                   r"SchöneichebeiBerlin": "Schöneiche bei Berlin",
                                                   r"([a-zß])([A-Z]|\()": r"\1 \2"}, regex=True)
        
        # get state name
        state_name = driveways.link_id.str.extract(r"(\w\w(?=_))")[0].unique()[0]
        
         # read the kreis data
        kreis = gpd.read_file(self.storage_directory + "/borders/gadm41_DEU_2.json").to_crs(25833)
        
        # fix names
        kreis["NAME_2"] = kreis["NAME_2"].replace({r"([a-zß])([A-Z]|\()": r"\1 \2"}, regex = True)
        
        # filter for state
        kreis = kreis.loc[(kreis.HASC_2.str.extract(r'((?<=DE\.)..(?=\.))') == state_name)[0], :]
        
        # reset output directory
        if os.path.exists(f"{out_dir}/assets"):
            shutil.rmtree(f"{out_dir}/assets")
        os.makedirs(f"{out_dir}/assets")
            
        ##
        # get and combine analysis data
        if os.path.exists(f"{self.storage_directory}/SARAH/analysis/{state_name}_irradiation.csv"):
            irradiation_data = pd.read_csv(f"{self.storage_directory}/SARAH/analysis/{state_name}_irradiation.csv")
            driveways = pd.merge(driveways, irradiation_data, on = ["link_id", "id"], how = "left")
        if os.path.exists(f"{self.storage_directory}/OSM/analysis/{state_name}_ps_distances.csv"):
            ps_distances = pd.read_csv(f"{self.storage_directory}/OSM/analysis/{state_name}_ps_distances.csv")
            driveways = pd.merge(driveways, ps_distances, on = ["link_id", "id"], how = "left")
        if os.path.exists(f"{self.storage_directory}/imagery/analysis/{state_name}.csv"):
            land_cover = pd.read_csv(f"{self.storage_directory}/imagery/analysis/{state_name}.csv")
            driveways = pd.merge(driveways, land_cover, on = ["link_id", "id"], how = "left")
        if os.path.exists(f"{self.storage_directory}/DGM/analysis/{state_name}.csv"):
            terrain_suitability = pd.read_csv(f"{self.storage_directory}/DGM/analysis/{state_name}_12.csv")
            driveways = pd.merge(driveways, terrain_suitability, on = ["link_id", "id"], how = "left")

        ##
        # compute central variables
        # apply buffer to polygons
        driveways['geometry'] = driveways.geometry.apply(lambda x: x.buffer(-12) if x is not None else None)
        # get the overall area
        driveways['suitable_area'] = driveways['geometry'].area
        # get the irradiation score
        driveways["irradiation_score"] = driveways.irradiation.apply(lambda x: (142.19999695 - x) / (142.19999695 - 108.40000153))
        driveways["irradiation_rank"] = driveways.irradiation_score.rank(method = "min", na_option = "bottom", ascending = False)
        # get the distance score
        driveways["distance_score"] = driveways["distance_substation"].apply(lambda x: (driveways["distance_substation"].max() - x) / (driveways["distance_substation"].max() - driveways["distance_substation"].min()))
        driveways["distance_rank"] = driveways.distance_score.rank(method = "min", na_option = "bottom", ascending = False)
        # get the land cover score
        driveways[["lc_background", "lc_agriculture", "lc_forest", "lc_building", "lc_road", "lc_unknown"]] =\
            driveways[["lc_background", "lc_agriculture", "lc_forest", "lc_building", "lc_road", "lc_unknown"]].fillna(0)
        driveways["land_cover_total_pixels"] = driveways["lc_background"] + driveways["lc_agriculture"] + driveways["lc_forest"] + driveways["lc_building"] + driveways["lc_road"]
        driveways["land_cover_share_good"] = (driveways["lc_background"] + driveways["lc_agriculture"]) / driveways["land_cover_total_pixels"]
        driveways["land_cover_share_restricted"] = driveways["lc_forest"] / driveways["land_cover_total_pixels"]
        driveways["land_cover_share_prohibted"] = (driveways["lc_building"] + driveways["lc_road"]) / driveways["land_cover_total_pixels"]
        driveways["land_cover_score"] = driveways["land_cover_share_good"] + 0.2 * driveways["land_cover_share_restricted"]
        driveways["land_cover_rank"] = driveways.land_cover_score.rank(method = "min", na_option = "bottom", ascending = False)
        driveways["no_land_cover"] = (((driveways["land_cover_score"] == 0) | (driveways["land_cover_score"].isna())))
        # get the terrain score
        driveways[["terrain_roughness"]] = driveways[["terrain_roughness"]].fillna(0)
        driveways["terrain_score"] = (1 - driveways["terrain_roughness"] / 90)
        driveways["terrain_rank"] = driveways.terrain_score.rank(method = "min", na_option = "bottom", ascending = False)
        driveways["no_terrain"] = (((driveways["terrain_score"] == 1) | (driveways["terrain_score"].isna())))
        
        # get the overall score
        driveways["overall_score"] = 0
        driveways["overall_score"][((~driveways["no_land_cover"]) & (~driveways["no_terrain"]))] =\
            (economic_model["irradiation"] * driveways["irradiation_score"] + 
                            economic_model["distance"] * driveways["distance_score"] +
                            economic_model["terrain"] * driveways["terrain_score"] +
                            economic_model["land_cover"] * driveways["land_cover_score"])
        driveways["overall_score"][((~driveways["no_land_cover"]) & (driveways["no_terrain"]))] =\
            (economic_model["irradiation"] * driveways["irradiation_score"] + 
                            economic_model["distance"] * driveways["distance_score"] +
                            economic_model["land_cover"] * driveways["land_cover_score"]) /\
                                (economic_model["irradiation"] + economic_model["distance"] + economic_model["land_cover"])
        driveways["overall_score"][((driveways["no_land_cover"]) & (~driveways["no_terrain"]))] =\
            (economic_model["irradiation"] * driveways["irradiation_score"] + 
                            economic_model["distance"] * driveways["distance_score"] +
                            economic_model["terrain"] * driveways["terrain_score"]) /\
                                (economic_model["irradiation"] + economic_model["distance"] + economic_model["terrain"])
        driveways["overall_score"][((driveways["no_land_cover"]) & (driveways["no_terrain"]))] =\
            (economic_model["irradiation"] * driveways["irradiation_score"] + 
                            economic_model["distance"] * driveways["distance_score"]) /\
                                (economic_model["irradiation"] + economic_model["distance"])
        driveways["overall_rank"] = driveways.overall_score.rank(method = "min", na_option = "bottom", ascending = False)
        
        # add municipality information
        driveways = driveways.sjoin(municipalities[["geometry", "NAME_3"]], predicate = "intersects").drop(columns = "index_right").reset_index(drop = True)
        
        # export the results as polygons
        driveways.to_crs(4326).to_file(f"{out_dir}/assets/{state_name}_polygons_final.json")
        
        ##
        # merge and aggregate for kreise
        
        # Define a function to compute the weighted mean:
        def wm(x): 
            if (tmp.loc[x[~x.isna()].index, "suitable_area"].sum() != 0):
                return np.average(x[~x.isna()], weights = tmp.loc[x[~x.isna()].index, "suitable_area"])
        
        # get mean statistics
        tmp = gpd.sjoin(kreis, driveways, how = 'inner', predicate = 'intersects').reset_index()
        tmp["link_id_individual"] = tmp.link_id + "_" + str(tmp.id)
        kreis_stats = tmp.groupby('NAME_2', as_index = False).agg({'link_id_individual': "count",
                                                'terrain_score': wm, 
                                                'land_cover_score': wm, 
                                                'irradiation_score': wm, 
                                                'distance_score': wm,
                                                'overall_score': wm})
        # export
        pd.merge(kreis[["NAME_2", "HASC_2", "geometry"]], kreis_stats, on = 'NAME_2', how = 'left').\
            to_crs(4326).to_file(f"{out_dir}/assets/{state_name}_kreis_final.json", driver = 'GeoJSON')
        
        ##
        # merge and aggregate for gemeinde
        
        # get mean statistics
        driveways["link_id_individual"] = tmp.link_id + "_" + str(tmp.id)
        gemeinde_stats = driveways.groupby('NAME_3', as_index = False).agg({'suitable_area': "sum",
                                                                        'link_id_individual': "count",
                                                                        'terrain_score': wm, 
                                                                        'land_cover_score': wm, 
                                                                        'irradiation_score': wm, 
                                                                        'distance_score': wm,
                                                                        'overall_score': wm}).reset_index()
        # filter for brandenburg
        state_name_long = kreis.NAME_1.unique()[0]
        # filter for brandenburg and export
        pd.merge(municipalities[["NAME_3", "geometry"]][municipalities['NAME_1'] == state_name_long], gemeinde_stats, left_on = 'NAME_3', right_on = 'NAME_3', how = 'left').\
            to_crs(4326).to_file(f"{out_dir}/assets/{state_name}_gemeinde_final.json", driver = 'GeoJSON')
        
        # copy the axiliary distance information
        shutil.copy(f"{self.storage_directory}/OSM/analysis/{state_name}_ps_auxiliary.csv", 
                    f"{out_dir}/assets/{state_name}_ps_auxiliary.csv") 

        os.mkdir(f"{out_dir}/assets/imagery")
        # copy the height profile images
        os.mkdir(f"{out_dir}/assets/imagery/height_profile")
        shutil.copytree(f"{self.storage_directory}/DGM/analysis/imagery", 
                    f"{out_dir}/assets/imagery/height_profile", 
                    dirs_exist_ok = True)
        
        # copy the rgb images
        os.mkdir(f"{out_dir}/assets/imagery/rgb")
        shutil.copytree(f"{self.storage_directory}/imagery/analysis/imagery/rgb", 
                    f"{out_dir}/assets/imagery/rgb", 
                    dirs_exist_ok = True)
        
        # zip all results
        shutil.make_archive(f"{out_dir}/assets", "zip", f"{out_dir}/assets") 
"""       
if __name__ == "__main__":
    c_analysis_combine = analysis_combine()
    c_analysis_combine.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson",
                               "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders/gadm41_DEU_4.json",
                               {"irradiation": 0.15, "distance": 0.25, "terrain": .1, "land_cover": 0.5},
                               "/pfs/data5/home/tu/tu_tu/tu_zxobe27/ds_project/ds_project/modules/dashboard/data")
"""