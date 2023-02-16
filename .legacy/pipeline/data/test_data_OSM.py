import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from modules.data.data_OSM import data_OSM

# Run a query for a single item
def test_query():
    OSM_downloader = data_OSM()
    OSM_downloader.query()
    
if __name__ == "__main__":
    test_query()
    print("Everything passed")