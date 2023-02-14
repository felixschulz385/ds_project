#from modules.preprocessing.preprocessing_abstract import preprocessing_abstract

import numpy as np
import pandas as pd
import warnings
from joblib import Parallel, delayed

import pyrosm as psm
import geopandas as gpd
import shapely
warnings.filterwarnings("ignore", category=shapely.errors.ShapelyDeprecationWarning) 
import momepy
import networkx as nx

class preprocessing_driveways(): #preprocessing_abstract
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
        
        self.link_types = ["motorway_link", "trunk_link"] #, "primary_link", "secondary_link", "tertiary_link"
        
        self.link_type_shorthands = {"motorway_link": "ML", "trunk_link": "TL"}

    
    def preprocess(self, bundesland, link_types = ["motorway_link", "trunk_link"], offset = 500, crs = 25833):
        """ Find driveways in a selected federal state of Germany.
        Arguments:
            bundesland (string):
                Chosen federal state of interest. Options:
                baden-wuerttemberg, bayern, berlin, brandenburg, bremen, hamburg, hessen, mecklenburg-vorpommern,
                niedersachsen, nordrhein-westfalen, rheinland-pfalz, saarland, sachsen, sachsen-anhalt, schleswig-holstein, thueringen
            link_types (list of strings):
                Chosen specification of link types with respect to OSM classifications. Options:
                motorway_link, trunk_link
            offset (int):
                Offset in meters for OSM driveway links that are grouped together.
        """

        # --- CHECK 1 ---
        # Correct specification of a German federal state
        if bundesland not in self.bundelaender:
            raise ValueError("ERROR - Please choose between the following options for bundesland: baden-wuerttemberg, bayern, berlin, brandenburg, bremen, hamburg, hessen, mecklenburg-vorpommern, niedersachsen, nordrhein-westfalen, rheinland-pfalz, saarland, sachsen, sachsen-anhalt, schleswig-holstein, thueringen.")
        
        # --- CHECK 2 ---
        # Correct specification of highway link types with respect to OSM classifications
        elif not all(x in self.link_types for x in link_types):
            raise ValueError("ERROR - Please choose between the following options for the list of link_types: motorway_link, trunk_link, primary_link, secondary_link, tertiary_link.")
        
        # --- NOTES ---
        # Great federal states are divided into government districts. Therefore, each district is processed seperately.
        else:
            for idx, region in enumerate(self.bundelaender[bundesland]):
                total = len(self.bundelaender[bundesland])
                print("--- Your chosen federal state has "+str(total)+" government district(s). ---")
                if idx == 0:
                    grouped_driveways = self.__region_preprocess(bundesland, region, link_types, crs, offset)
                    print("---", str(idx+1), "of", total, "government districts are processed. ---")
                else:
                    next_grouped_driveways = self.__region_preprocess(bundesland, region, link_types, crs, offset)
                    grouped_driveways = pd.concat([grouped_driveways, next_grouped_driveways])
                    print("---", str(idx+1), "of", total, "government districts are processed. ---")
            
            # get the link type per group
            type_mapping = grouped_driveways[grouped_driveways.highway.isin(self.link_types)].groupby("group")["highway"].unique().apply(lambda x: x[0])

            # add the link type per group to the data
            grouped_driveways["link_type"] = grouped_driveways["group"].apply(lambda x: self.link_type_shorthands[type_mapping[x]])
            
            # add a link ID comprised of state, link type and an arbitrary number
            grouped_driveways["link_id"] = grouped_driveways.apply(lambda x: self.bundeslaender_shorthands[bundesland] + "_" +
                                                            x["link_type"] + "_" +
                                                            str(x["group_id"]).zfill(4), axis = 1)
            
            # sort by id
            grouped_driveways.sort_values("link_id", inplace = True)
            
            # save to file
            grouped_driveways.to_file(self.storage_directory+"OSM/processed/"+bundesland+".geojson", driver='GeoJSON')
            
            ## calculate internal polygons
            # merge all geometries by id
            grouped_driveways = grouped_driveways.dissolve(by = "group", as_index = False)
            # get polygons
            grouped_driveways["polygons"] = grouped_driveways.geometry.apply(lambda x: list(shapely.ops.polygonize(x)))
            # focus DF on poylgons
            grouped_driveways = grouped_driveways.\
                drop(columns = "geometry").\
                    explode("polygons").\
                        set_geometry("polygons", crs = "EPSG:"+str(crs))
            # give polygons unique ids
            grouped_driveways.id = grouped_driveways.groupby('group_id')['group_id'].rank(method='first')
            # export
            grouped_driveways.to_file(f"{self.storage_directory}OSM/processed/{bundesland}_polygons.geojson", driver='GeoJSON')
                
                    
    def __region_preprocess(self, bundesland, region, link_types, crs, offset):

        # ----------------------------------------------
        # --- 1.) Load OSM Data and Filter Driveways ---
        # ----------------------------------------------
        print("Loading Regional Data...")

        # Initialize the OSM parser object
        osm = psm.OSM(self.storage_directory+"OSM/raw/"+bundesland+"/"+region+"-latest.osm.pbf")

        # assemble the necessary filter
        filter_dict = {"highway": link_types + ["motorway", "trunk", "primary", "secondary", "tertiary", "service"]}#
        
        # Filter the OSM data for driveways
        grid = osm.get_data_by_custom_criteria(custom_filter=filter_dict,
                                        # Keep data matching the criteria above
                                        filter_type="keep",
                                        # Do not keep nodes (point data)    
                                        keep_nodes=False, 
                                        keep_ways=True, 
                                        keep_relations=False)
        print("--- The OSM data has been loaded successfully. ---")

        # Project to correct CRS
        grid = grid.to_crs(crs)

        # Filter links
        grid_links = grid[grid['highway'].isin(link_types)].copy()

        # --- NOTES ---
        # The OSM data indicates a link where a acceleration/deceleration lane ends and the ramp takes its own direction.
        # Thus, motorway interchanges consist of several connection ramps and multiple indicated points.
        # As we are interested in the ear shape of the ramps, we need to group these points together.

        # -----------------------------------------
        # --- 2.) Identify Close Driveway Links ---
        # -----------------------------------------
        print("Reorganizing and Identification...")

        # Offset boxes by offset in meters
        bboxes_offset = grid_links.bounds
        bboxes_offset["minx"] = bboxes_offset["minx"] - offset
        bboxes_offset["miny"] = bboxes_offset["miny"] - offset
        bboxes_offset["maxx"] = bboxes_offset["maxx"] + offset
        bboxes_offset["maxy"] = bboxes_offset["maxy"] + offset

        # Turn the bboxes into polygons
        polygons = bboxes_offset.apply(lambda bbox: shapely.geometry.Polygon([(bbox[0], bbox[1]),
                          (bbox[0], bbox[3]),
                          (bbox[2], bbox[3]),
                          (bbox[2], bbox[1])]), axis = 1)
        
        # Create matrix of intersecting bounding boxes
        overlaps = np.zeros((polygons.shape[0], polygons.shape[0]))
        for i in range(polygons.shape[0]):
            for j in range(polygons.shape[0]):
                overlaps[i,j] = polygons.iloc[i].intersects(polygons.iloc[j]) 
        
        # define a function that recursively determines overlaps
        def add_trans(matrix, i, j, depth):
            # limit depth
            if depth == 100:
                return matrix
            else:
                depth += 1
            # count an overlap in row j at position i
            matrix[j, i] += 1
            # consider all rows that overlap with this
            for k in np.where(matrix[:, j] > 0)[0]:
                # proceed if already counted
                if (matrix[k, i] > 0): 
                    continue
                # recurse
                matrix = add_trans(matrix, i, k, depth)
            return matrix

        # Calculate the transitive overlaps
        for i in range(overlaps.shape[0]):
            for j in np.where(overlaps[i, :] > 0)[0]:
                overlaps = add_trans(overlaps, i, j, 0)
                
        # Create a dictionary of transitive overlaps
        outdict = [[]] * overlaps.shape[0]
        for i in range(overlaps.shape[0]):
            outdict[i] = np.where(overlaps[i,:] > 0)[0]

        # -----------------------------------------------
        # --- 3.) Group Close Driveway Links Together ---
        # -----------------------------------------------

        # Grouping
        grid_links["group"] = [str(x) for x in outdict]
        grid_grouped = grid_links.copy() #grid_links.dissolve(by = "group", as_index = False)
        
        # -----------------------------------------
        # --- 4.) Filter roads to state borders ---
        # -----------------------------------------

        # Cut data (e.g. Brandenburg vs. Brandenburg + Berlin)
        borders = gpd.read_file(self.storage_directory+"borders/gadm41_DEU_1.json")
        grid_grouped = grid_grouped[grid_grouped.within(borders.loc[borders["NAME_1"] == self.bundelaender_umlaute[bundesland], "geometry"].iloc[0])]
        
        print("---", grid_grouped.group.nunique(), "Driveways were found in the area of interest. ---")
        
        # --------------------------------------
        # --- 5.) Get pieces of adjunct road ---
        # --------------------------------------
        
        # Filter roads
        grid_ways = grid[(~grid['highway'].isin(link_types))].copy()
        
        # create bounding boxes for groups of link roads
        #links_dissolved = grid_grouped.dissolve(by = "group", as_index = False)
        link_bounds = grid_grouped.bounds.apply(lambda bbox: shapely.geometry.Polygon([(bbox[0], bbox[1]),
                          (bbox[0], bbox[3]),
                          (bbox[2], bbox[3]),
                          (bbox[2], bbox[1])]).buffer(100), axis = 1)

        # create a matrix of intersections between roads and links
        # the matrix is of size #links X #ways and is NA for no intersection OR the group of the intersecting link
        filtered = pd.concat([grid_ways.intersects(link_bounds[i]).map({True: grid_grouped.group[i], False: pd.NA}) 
                              for i in link_bounds.index], axis = 1)
        # get the first group per road and save as the road's group
        grid_ways["group"] = filtered.fillna(method='bfill', axis=1).iloc[:, 0]
        # filter for only those roads that intersect
        grid_ways = grid_ways.loc[~grid_ways["group"].isna(),:]
        
        print("-- ", grid_ways.shape[0], "intersecting roads were found in the area of interest. ---")
        
        # add intersecting highways only
        grid_grouped = pd.concat([grid_grouped, grid_ways])
        
        # replace grouping with geographically sorted id
        group_id_mapping = grid_grouped.dissolve(by = "group", as_index = False)
        group_id_mapping["c_x"] = group_id_mapping.centroid.apply(lambda x: x.x if x is not None else None)
        group_id_mapping["c_y"] = group_id_mapping.centroid.apply(lambda x: x.y if x is not None else None)
        group_id_mapping.sort_values(["c_x", "c_y"], inplace = True)
        group_id_mapping["group_id"] = group_id_mapping.reset_index().index

        grid_grouped = pd.merge(grid_grouped, group_id_mapping[["group", "group_id"]], on = "group")
        
        return grid_grouped
    
if __name__ == "__main__":
    preprocessor_driveways = preprocessing_driveways()
    preprocessor_driveways.preprocess("brandenburg")