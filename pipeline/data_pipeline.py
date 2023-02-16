import os, sys, re
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
"""
from modules.data.data_imagery import data_imagery
from modules.preprocessing.preprocessing_driveways import preprocessing_driveways
from modules.preprocessing.preprocessing_power_stations import preprocessing_power_stations
from modules.analysis.analysis_irradiation import analysis_irradiation
from modules.analysis.analysis_power_stations import analysis_power_stations
from modules.analysis.analysis_DGM import analysis_DGM
"""
from modules.analysis.analysis_imagery import analysis_imagery
from modules.analysis.analysis_combine import analysis_combine


bundeslaender_shorthands = {"baden-wuerttemberg": "BW",
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


def f_data_imagery(bundesland, base_path):
    """
    Get the imagery (takes very long and needs 64GB+ of RAM)
    
    Args:
        bundesland (str): name of German state to query
    """
    import geopandas as gpd
    # get the boundaries for brandenburg roads
    driveways = gpd.read_file(f"{base_path}/OSM/processed/{bundesland}_polygons.geojson").\
        dissolve(by = "link_id", as_index = False)
    driveways["geometry"] = driveways.geometry.apply(lambda x: x.buffer(201) if x is not None else None)
    # query the images
    imagery_downloader = data_imagery(bundesland)
    imagery_downloader.query(driveways.bounds.values, driveways.link_id.reset_index(drop = True))


def f_preprocess_driveways(bundesland):
    """
    Parse the OSM data for driveways (turnoffs and nearby roads)
    
    Args:
        bundesland (str): name of German state to query
    """
    preprocessor_driveways = preprocessing_driveways()
    preprocessor_driveways.preprocess(bundesland, offset = 500)
    
def f_preprocess_power_stations(bundesland):
    """
    Parse the OSM data for power stations
    
    Args:
        bundesland (str): name of German state to query
    """
    preprocessor_power_stations = preprocessing_power_stations()
    preprocessor_power_stations.preprocess(bundesland)

def f_analysis_DGM(bundesland, base_path):
    """
    Processing the height profiles. Works image-by-image using the Grid information stored in image download
    
    Args:
        bundesland (str): name of German state to query
    """
    
    # assemble file names of all NetCDF files containing information on BB standard grids containing a turnoff
    imagery = os.listdir(base_path + "/imagery/raw/")
    regexp = re.compile(bundeslaender_shorthands[bundesland] + ".*\.nc")
    imagery = [(base_path + "/imagery/raw/" + file) for file in imagery if regexp.search(file)]
    
    # assemble file name of GeoJSON containing driveway polygons for the German state
    driveways = f"{base_path}/OSM/processed/{bundesland}_polygons.geojson"
    
    c_analysis_DGM = analysis_DGM()
    c_analysis_DGM.analyze(imagery, driveways)
    
def f_analysis_imagery(bundesland, base_path):
    """
    Processing the satellite imagery. Works image-by-image using the trained Deep Neural Network
    
    Args:
        bundesland (str): name of German state to query
    """
    
    # assemble file names of all NetCDF files containing information on BB standard grids containing a turnoff
    imagery = os.listdir(base_path + "/imagery/raw/")
    regexp = re.compile(bundeslaender_shorthands[bundesland] + ".*\.nc")
    imagery = [(base_path + "/imagery/raw/" + file) for file in imagery if regexp.search(file)]
    
    # assemble file name of GeoJSON containing driveway polygons for the German state
    driveways = f"{base_path}/OSM/processed/{bundesland}_polygons.geojson"
    
    c_analysis_imagery = analysis_imagery()
    c_analysis_imagery.analyze(imagery, driveways, model = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/trained_models/love_checkpoint_DLV3biased_75acc.pth.tar")

def f_analysis_power_stations(bundesland, base_path):
    """
    Processing the data on power stations to get closest distances to all driveway polygons
    
    Args:
        bundesland (str): name of German state to query
    """
    
    # assemble file name of GeoJSON containing driveway polygons for the German state
    driveways = f"{base_path}/OSM/processed/{bundesland}_polygons.geojson"
    
    # assemble file name of GeoJSON containing substations
    substations = f"{base_path}/OSM/processed/{bundesland}_substations.geojson"
    
    c_analysis_power_stations = analysis_power_stations()
    c_analysis_power_stations.analyze(driveways, substations,
                                    "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders/gadm41_DEU_4.json")
    
def f_analysis_irradiation(bundesland, base_path):
    """
    Processing the data on annual irradiation to get single best value for each driveway polygon
    
    Args:
        bundesland (str): name of German state to query
    """
    # assemble file name of GeoJSON containing driveway polygons for the German state
    driveways = f"{base_path}/OSM/processed/{bundesland}_polygons.geojson"
    
    c_analysis_irradiation = analysis_irradiation()
    c_analysis_irradiation.analyze(driveways)
    
def f_analysis_combine(bundesland, base_path):
    """
    Combining all processed data and producing all final files for the dashboard
    
    Args:
        bundesland (str): name of German state to query
    """
    c_analysis_combine = analysis_combine()
    c_analysis_combine.analyze(f"{base_path}/OSM/processed/{bundesland}_polygons.geojson",
                               f"{base_path}/borders/gadm41_DEU_4.json",
                               economic_model = {"irradiation": 0.15, "distance": 0.25, "terrain": .1, "land_cover": 0.5},
                               out_dir = "/pfs/data5/home/tu/tu_tu/tu_zxobe27/ds_project/ds_project/modules/dashboard/deployment")



def main(bundeslander = ["brandenburg"], base_path = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data",
         data_borders = False, data_DGM = False, data_iradiation = False, data_imagery = False, data_OSM = False,
         preprocessing_driveways = False, preprocessing_power_stations = False,
         analysis_DGM = False, analysis_imagery = False, analysis_power_stations = False, analysis_irradiation = False, analysis_combine = False):
    """
    A function defining the pipeline encompassing data procurement, preprocessing and analysis.
    
    Notes:
        - Since borders, DGM and iradiation data is continously changing and data sources are large, it is NOT RECOMMENDED to update these sources of data.
    """
    
    # iterate over states
    for bundesland in bundeslander:
        # perform step on request
        if preprocessing_driveways:
            f_preprocess_driveways(bundesland)
        if data_imagery:
            f_data_imagery(bundesland, base_path)
        if preprocessing_power_stations:
            f_preprocess_power_stations(bundesland)
        if analysis_DGM:
            f_analysis_DGM(bundesland, base_path)        
        if analysis_imagery:
            f_analysis_imagery(bundesland, base_path)
        if analysis_power_stations:
            f_analysis_power_stations(bundesland, base_path)
        if analysis_irradiation:
            f_analysis_irradiation(bundesland, base_path)
        if analysis_combine:
            f_analysis_combine(bundesland, base_path)

if __name__ == "__main__":
    main(analysis_combine=True)