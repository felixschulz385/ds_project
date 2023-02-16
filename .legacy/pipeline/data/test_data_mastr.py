import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from modules.data.data_MaStR import data_MaStR

# Run a query for a single item
def test_query():
    mastr_downloader = data_MaStR()
    mastr_downloader.query()
    
if __name__ == "__main__":
    test_query()
    print("Everything passed")