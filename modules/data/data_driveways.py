"""
This class uses OSM data to find driveway links.
"""

from modules.data.data_abstract import data_abstract

import numpy as np
import pandas as pd

import pyrosm as psm
import geopandas as gpd
import shapely

class data_driveways(data_abstract):
    
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
        
        self.highway_links = ["motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"]
    
    def query(self, bundesland, link_types = ["motorway_link"], offset = 1000, spatial_bounds = "available", temporal_bounds = "available", crs = 25833):
        """ Find driveways in a selected federal state of Germany.
        Arguments:
            bundesland (string):
                Chosen federal state of interest. Options:
                baden-wuerttemberg, bayern, berlin, brandenburg, bremen, hamburg, hessen, mecklenburg-vorpommern,
                niedersachsen, nordrhein-westfalen, rheinland-pfalz, saarland, sachsen, sachsen-anhalt, schleswig-holstein, thueringen
            link_types (list of strings):
                Chosen specification of highway link types with respect to OSM classifications. Options:
                motorway_link, trunk_link, primary_link, secondary_link, tertiary_link
            offset (int):
                Offset in meters for OSM driveway links that are grouped together.
        """

        # --- CHECK 1 ---
        # Correct specification of a German federal state
        if bundesland not in self.bundelaender:
            raise ValueError("ERROR - Please choose between the following options for bundesland: baden-wuerttemberg, bayern, berlin, brandenburg, bremen, hamburg, hessen, mecklenburg-vorpommern, niedersachsen, nordrhein-westfalen, rheinland-pfalz, saarland, sachsen, sachsen-anhalt, schleswig-holstein, thueringen.")
        
        # --- CHECK 2 ---
        # Correct specification of highway link types with respect to OSM classifications
        elif not all(x in self.highway_links for x in link_types):
            raise ValueError("ERROR - Please choose between the following options for the list of link_types: motorway_link, trunk_link, primary_link, secondary_link, tertiary_link.")
        
        # --- NOTES ---
        # Great federal states are divided into government districts. Therefore, each district is processed seperately.
        else:
            for idx, region in enumerate(self.bundelaender['bundesland']):
                total = len(self.bundelaender['bundesland'])
                print("--- Your chosen federal state has"+str(total)+"government district(s). ---")
                if idx == 0:
                    grouped_driveways = self._region_query(self, bundesland, region, link_types, crs, offset)
                    print("---", str(idx+1), "of", total, "government districts are processed. ---")
                else:
                    next_grouped_driveways = self._region_query(self, bundesland, region, link_types, crs, offset)
                    grouped_driveways = np.append(grouped_driveways, next_grouped_driveways)
                    print("---", str(idx+1), "of", total, "government districts are processed. ---")
            
            return grouped_driveways
    
    def _region_query(self, bundesland, region, link_types, crs, offset):

        # ----------------------------------------------
        # --- 1.) Load OSM Data and Filter Driveways ---
        # ----------------------------------------------
        print("Downloading Regional Data...")

        # Initialize the OSM parser object
        osm = psm.OSM(self.storage_directory+"OSM/"+bundesland+"/"+region+"-latest.osm.pbf")

        # Filter the OSM data for driveways
        grid = osm.get_data_by_custom_criteria(custom_filter={"highway": self.highway_links},
                                        # Keep data matching the criteria above
                                        filter_type="keep",
                                        # Do not keep nodes (point data)    
                                        keep_nodes=False, 
                                        keep_ways=True, 
                                        keep_relations=True)
        print("--- The OSM data has been loaded successfully. ---")

        # Project to correct CRS
        grid = grid.to_crs(crs)

        # Filter driveway types
        grid_drive = grid[grid['highway'].isin(link_types)]

        # --- NOTES ---
        # The OSM data indicates a link where a acceleration/deceleration lane ends and the ramp takes its own direction.
        # Thus, motorway interchanges consist of several connection ramps and multiple indicated points.
        # As we are interested in the ear shaped by the ramps, we need to group these points together.

        # -----------------------------------------
        # --- 2.) Identify Close Driveway Links ---
        # -----------------------------------------
        print("Reorganizing and Identification...")

        # Offset boxes by offset in meters
        bboxes_offset = grid_drive.bounds
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

        # Create a dictionary of transitive overlaps
        outdict = [[]] * overlaps.shape[0]

        # Calculate the transitive overlaps
        for i in range(overlaps.shape[0]):
            outdict[i] = np.where((np.sum(overlaps[np.where(overlaps[i, :]), :], axis = 1) > 0))[1]

        # -----------------------------------------------
        # --- 3.) Group Close Driveway Links Together ---
        # -----------------------------------------------

        # Grouping
        grid_drive.loc[:,"group"] = [str(x) for x in outdict]
        grid_grouped = grid_drive.dissolve(by = "group")

        # Add information on borders of area of interest (e.g. Brandenburg vs. Brandenburg + Berlin)
        borders = gpd.read_file(self.storage_directory+"borders/gadm41_DEU_1.json")
        grid_grouped = grid_grouped[grid_grouped.within(borders.loc[borders["NAME_1"] == self.bundelaender_umlaute['bundesland'], "geometry"].iloc[0])]

        print("---", grid_grouped.shape[0], "Driveways were found in the area of interest. ---")
        return grid_grouped