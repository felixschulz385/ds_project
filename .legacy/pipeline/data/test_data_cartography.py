import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from modules.data.data_cartography import data_cartography

# Run a query for a single item
def test_query():
    cartography_downloader = data_cartography()
    cartography_downloader.query()
    
if __name__ == "__main__":
    test_query()
    print("Everything passed")