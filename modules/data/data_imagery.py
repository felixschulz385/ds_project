from modules.data.data_abstract import data_abstract
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from bs4 import BeautifulSoup
from numpy import asarray, expand_dims, arange
from io import BytesIO
from PIL import Image
from xarray import Dataset
from geopandas import GeoSeries
from shapely.geometry import Polygon


class data_imagery(data_abstract):
    
    # establishes a connection to the wms service           
    def __establish_wms_connection(self):
        self.wms = WebMapService(self.wms_service, version='1.1.1')
        print([self.wms.identification.title, self.wms.identification.abstract])
        
    # establishes a connection to the wfs service           
    def __establish_wfs_connection(self):
        self.wfs = WebFeatureService(self.wfs_service, version='1.1.0')
        print([self.wfs.identification.title, self.wfs.identification.abstract])
    
    # takes a bbox-list of format (xmin, ymin, xmax, ymax) and projects it
    def __project_bounding_box(self, bbox, bbox_crs):
        polygon = Polygon([(bbox[0], bbox[1]),
                                            (bbox[0], bbox[3]),
                                            (bbox[2], bbox[3]),
                                            (bbox[2], bbox[1])])
        return(GeoSeries(polygon).set_crs(bbox_crs).to_crs(self.import_crs).bounds)
    
    # calculates the output image size according to the provided density and bbox
    def __calculate_image_size(self, bbox):
        return([((bbox[2] - bbox[0]) / self.pixel_density), 
                ((bbox[3] - bbox[1]) / self.pixel_density)])
        
    
    # the constructor
    def __init__(self, state, 
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery"):
        self.state = state
        self.storage_directory = storage_directory
        
        # provide variables specific to the state
        # - pixel density is the resolution of each pixel in m
        # - import crs is the crs projection used for import
        # - wms_service is the URL of the service used for download
        match self.state:
            case "brandenburg":
                self.pixel_density = .2
                self.import_crs = 25833
                self.wms_service = "https://isk.geobasis-bb.de/mapproxy/dop20_2016_2018/service/wms?"
                self.wms_layer = "dop20_bebb_2016_2018_farbe"
                self.wfs_service = "https://isk.geobasis-bb.de/ows/aktualitaeten_wfs?"
                self.wfs_typename = "app:dop20rgbi_2016_2018_single"
                self.wfs_datepos = "app:creationdate"
        
        self.__establish_wms_connection()
        self.__establish_wfs_connection()
    
    # adds a bbox into the query stack
    def query(self, spatial_bounds, temporal_bounds = "available", crs = 25833):
        
        n = 0
        
        for bbox in spatial_bounds:
            
            # project the bbox if necessary
            if(crs != self.import_crs):
                query_bbox = self.__project_bounding_box(bbox, crs)
            else:
                query_bbox = bbox
            
            # query the imagery from the WMS service
            img = self.wms.getmap(
                layers = [self.wms_layer],
                srs = "EPSG:" + str(self.import_crs),
                bbox = query_bbox,
                size = self.__calculate_image_size(query_bbox),
                format = "image/jpeg").read()
            
            # query timestamp from the WFS service
            wfs_response = self.wfs.getfeature(typename = self.wfs_typename,
                                               bbox = query_bbox, 
                                               srsname = "EPSG:" + str(self.import_crs)).read()
            timestamp = BeautifulSoup(wfs_response, features = "xml").find(self.wfs_datepos).text
            
            # export as jpg first
            with open(self.storage_directory + "/" + self.state + 
                      "_" + "_".join([str(x) for x in query_bbox]) + "_" + timestamp + ".jpg", "wb") as file:
                file.write(img)
            
            # turn jpg into numpy array
            tmp_np = asarray(Image.open(BytesIO(img)))
            
            # create xarray
            tmp_xd = Dataset(data_vars = {"red": (["x", "y"], tmp_np[:,:,0]),
                                          "green": (["x", "y"], tmp_np[:,:,1]),
                                          "blue": (["x", "y"], tmp_np[:,:,2])},
                             coords = {"x": (["x"], arange(tmp_np.shape[0]) * .2 + query_bbox[0]),
                                       "y": (["y"], arange(tmp_np.shape[1]) * .2 + query_bbox[1])})
            # convert type
            tmp_xd = tmp_xd.astype("int")
            # set output crs
            tmp_xd.rio.write_crs(25833, inplace = True)
            tmp_xd.rio.set_spatial_dims(x_dim = "x", y_dim = "y", inplace = True)
            tmp_xd.rio.write_coordinate_system(inplace = True)
            tmp_xd.rio.write_transform(inplace = True)
            # export the nc
            with open(self.storage_directory + "/" + self.state + 
                      "_" + "_".join([str(x) for x in query_bbox]) + "_" + timestamp + ".nc", "wb") as file:
                tmp_xd.to_netcdf(file)
                
            n += 1
            
        print("Successfully queried and exported " + str(n) + " images")