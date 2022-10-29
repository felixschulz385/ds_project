import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from modules.data.data_borders import data_borders

# Run a query for a single item
def test_query():
    imagery_downloader = data_borders()
    imagery_downloader.query()
    
if __name__ == "__main__":
    test_query()
    print("Everything passed")