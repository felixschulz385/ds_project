import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from modules.data.data_imagery import data_imagery

import xarray
import rioxarray

# Run a query for a single item
def test_query_single():
    imagery_downloader = data_imagery("brandenburg")
    imagery_downloader.query([(394168.38, 5796138.69, 394388.69, 5796390.61)], crs = 25833)
    #imagery_downloader.run_query()
    #imagery_downloader.export_query()
    
# TODO: Run a query for multiple items with different CRS

# Run a query for a single item
def test_results():
    file_1 = rioxarray.open_rasterio("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/brandenburg_394168.38_5796138.69_394388.69_5796390.61.nc")
    assert file_1.shape == (1, 1259, 1101), "File 1 should be (1, 3, 1259, 1101)"

if __name__ == "__main__":
    test_query_single()
    test_results()
    print("Everything passed")