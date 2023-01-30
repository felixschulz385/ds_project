#from modules.preprocessing.preprocessing_abstract import preprocessing_abstract

import pandas as pd
import geopandas as gpd
import pyrosm as psm

class preprocessing_power_stations(): #preprocessing_abstract
    """
    This class uses OSM data to find driveway links and exports them as a
    shapefile of linestrings as well as internal poylgons
    """
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/"):

        self.storage_directory = storage_directory

        self.bundelaender = {"baden-wuerttemberg": ['freiburg-regbez', 'karlsruhe-regbez', 'stuttgart-regbez', 'tuebingen-regbez'],
            "bayern": ['mittelfranken', 'niederbayern', 'oberbayern', 'oberfranken', 'oberpfalz', 'schwaben', 'unterfranken'],
            "berlin": ['berlin'],
            "brandenburg": ['brandenburg'],
            "bremen": ['bremen'],
            "hamburg": ['hamburg'],
            "hessen": ['hessen'],
            "mecklenburg-vorpommern": ['mecklenburg-vorpommern'],
            "niedersachsen": ['niedersachsen'],
            "nordrhein-westfalen": ['arnsberg-regbez', 'detmold-regbez', 'duesseldorf-regbez', 'koeln-regbez', 'muenster-regbez'],
            "rheinland-pfalz": ['rheinland-pfalz'],
            "saarland": ['saarland'],
            "sachsen": ['sachsen'],
            "sachsen-anhalt": ['sachsen-anhalt'],
            "schleswig-holstein": ['schleswig-holstein'],
            "thueringen": ['thueringen']}

        self.bundelaender_umlaute = {"baden-wuerttemberg": "Baden-Württemberg",
            "bayern": "Bayern",
            "berlin": "Berlin",
            "brandenburg": "Brandenburg",
            "bremen": "Bremen",
            "hamburg": "Hamburg",
            "hessen": "Hessen",
            "mecklenburg-vorpommern": "Mecklenburg-Vorpommern",
            "niedersachsen": "Niedersachsen",
            "nordrhein-westfalen": "Nordrhein-Westfalen",
            "rheinland-pfalz": "Rheinland-Pfalz",
            "saarland": "Saarland",
            "sachsen": "Sachsen",
            "sachsen-anhalt": "Sachsen-Anhalt",
            "schleswig-holstein": "Schleswig-Holstein",
            "thueringen": "Thüringen"}
        
        self.bundeslaender_shorthands = {"baden-wuerttemberg": "BW",
            "bayern": "BY",
            "berlin": "BE",
            "brandenburg": "BB",
            "bremen": "HB",
            "hamburg": "HH",
            "hessen": "HE",
            "mecklenburg-vorpommern": "MV",
            "niedersachsen": "NI",
            "nordrhein-westfalen": "NW",
            "rheinland-pfalz": "RP",
            "saarland": "SL",
            "sachsen": "SN",
            "sachsen-anhalt": "ST",
            "schleswig-holstein": "SH",
            "thueringen": "TH"}
    
    def preprocess(self, bundesland, crs = 25833):
        """ Find driveways in a selected federal state of Germany.
        Arguments:
            bundesland (string):
                Chosen federal state of interest. Options:
                baden-wuerttemberg, bayern, berlin, brandenburg, bremen, hamburg, hessen, mecklenburg-vorpommern,
                niedersachsen, nordrhein-westfalen, rheinland-pfalz, saarland, sachsen, sachsen-anhalt, schleswig-holstein, thueringen
        """

        # --- CHECK ---
        # Correct specification of a German federal state
        if bundesland not in self.bundelaender:
            raise ValueError("ERROR - Please choose between the following options for bundesland: baden-wuerttemberg, bayern, berlin, brandenburg, bremen, hamburg, hessen, mecklenburg-vorpommern, niedersachsen, nordrhein-westfalen, rheinland-pfalz, saarland, sachsen, sachsen-anhalt, schleswig-holstein, thueringen.")
         
        # --- NOTES ---
        # Great federal states are divided into government districts. Therefore, each district is processed seperately.
        else:
            for idx, region in enumerate(self.bundelaender[bundesland]):
                total = len(self.bundelaender[bundesland])
                print("--- Your chosen federal state has "+str(total)+" government district(s). ---")
                if idx == 0:
                    grouped_substations = self.__region_preprocess(bundesland, region, crs)
                    print("---", str(idx+1), "of", total, "government districts are processed. ---")
                else:
                    next_grouped_driveways = self.__region_preprocess(bundesland, region, crs)
                    grouped_substations = pd.concat([grouped_driveways, next_grouped_driveways])
                    print("---", str(idx+1), "of", total, "government districts are processed. ---")
        
        # write result to disk
        grouped_substations.to_file(f"{self.storage_directory}OSM/processed/{bundesland}_substations.geojson", driver='GeoJSON')
                    
                    
    def __region_preprocess(self, bundesland, region, crs):

        # ----------------------------------------------
        # --- 1.) Load OSM Data and Filter Driveways ---
        # ----------------------------------------------
        print("Loading Regional Data...")

        # Initialize the OSM parser object
        osm = psm.OSM(self.storage_directory+"OSM/raw/"+bundesland+"/"+region+"-latest.osm.pbf")
        
        # Filter the OSM data for driveways
        substations = osm.get_data_by_custom_criteria(custom_filter = {"power": ["substation"]},
                                        # Keep data matching the criteria above
                                        filter_type="keep",
                                        # Do not keep nodes (point data)    
                                        keep_nodes=False, 
                                        keep_ways=True, 
                                        keep_relations=True)
        print("--- The OSM data has been loaded successfully. ---")

        # Project to correct CRS
        substations = substations.to_crs(crs)

        # Filter links
        substations_filtered = substations.loc[((~substations.substation.isna()) & (substations.osm_type == "way")),:].copy()

        # use centroid as location
        substations_filtered.geometry = substations_filtered.centroid
        
        return substations_filtered
    
if __name__ == "__main__":
    preprocessor_power_stations = preprocessing_power_stations()
    preprocessor_power_stations.preprocess("brandenburg")