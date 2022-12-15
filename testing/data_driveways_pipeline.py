import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from modules.data.data_imagery import data_imagery
from modules.preprocessing.preprocessing_driveways import preprocessing_driveways

import geopandas as gpd

def preprocess_driveways(bundesland):
    driveways_processor = preprocessing_driveways()
    driveways_processor.preprocess("brandenburg", offset = 50)
    
def image_query(bundesland):
    # get the boundaries for brandenburg roads
    driveways = gpd.read_file(f"{base_path}OSM/processed/{bundesland}.geojson").\
        dissolve(by = "link_id", as_index = False)
    # query the images
    imagery_downloader = data_imagery(bundesland)
    imagery_downloader.query(driveways.loc[driveways.link_id == "BB_ML_0045",:].bounds.values, driveways.loc[driveways.link_id == "BB_ML_0045", "link_id"].reset_index(drop = True))

if __name__ == "__main__":
    
    base_path = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/"
    bundeslander = ["brandenburg"]
    
    ## update OSM data
    # TODO
    
    for bundesland in bundeslander:
        ## process the OSM data
        # filter and turn into geojson
        #preprocess_driveways(bundesland)
        ## get the imagery (takes very long and needs 64GB+ of RAM)
        image_query(bundesland)