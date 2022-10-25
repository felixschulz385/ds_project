from modules.data.data_imagery import data_imagery
import xarray
import rioxarray

# Run a query for a single item
def test_query_single():
    imagery_downloader = data_imagery("brandenburg")
    imagery_downloader.add_query_bbox((394168.38, 5796138.69, 394388.69, 5796390.61), crs = 25833)
    imagery_downloader.establish_wms_connection()
    imagery_downloader.query_wms()
    imagery_downloader.export_downloads()
    
# TODO: Run a query for multiple items with different CRS
def test_query_multiple():
    imagery_downloader = data_imagery("brandenburg")
    imagery_downloader.add_query_bbox((394168.38, 5796138.69, 394388.69, 5796390.61), crs = 25833)
    imagery_downloader.establish_wms_connection()
    imagery_downloader.query_wms()
    imagery_downloader.export_downloads()

# Run a query for a single item
def test_results():
    file_1 = rioxarray.open_rasterio("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/brandenburg_394168.38_5796138.69_394388.69_5796390.61.nc")
    assert file_1.shape == (3, 1259, 1101), "File 1 should be (3, 1259, 1101)"

if __name__ == "__main__":
    test_query()
    test_results()
    print("Everything passed")