#from modules.data.data_abstract import data_abstract
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from bs4 import BeautifulSoup
from numpy import array, asarray, unique, expand_dims, arange, ceil, floor, float64
from time import sleep
from io import BytesIO
from os import listdir
from re import compile
from PIL import Image
from xarray import Dataset
import rioxarray
from geopandas import GeoSeries, read_file
from shapely.geometry import Polygon

class data_imagery(): #data_abstract
    
    # establishes a connection to the imagery wms service           
    def __establish_wms_connection(self):
        self.wms = WebMapService(self.wms_service, version='1.3.0')
        print([self.wms.identification.title, self.wms.identification.abstract])
        
    # establishes a connection to the imagery wfs service           
    def __establish_wfs_connection(self):
        self.wfs = WebFeatureService(self.wfs_service, version='1.1.0')
        print([self.wfs.identification.title, self.wfs.identification.abstract])
        
    # establishes a connection to the height wms service
    def __establish_height_wms_connection(self):
        self.height_wms = WebMapService(self.height_wms_service, version='1.3.0')
        print([self.height_wms.identification.title, self.height_wms.identification.abstract])
        
    # establishes a connection to the grid wfs service
    def __establish_grid_wfs_connection(self):
        self.wfs_grid = WebFeatureService(self.grid_wfs_service, version='1.1.0')
        print([self.wfs_grid.identification.title, self.wfs_grid.identification.abstract])
    
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
    
    # calculate parameters for chunked query
    def __get_split_parameters(self, bbox):
        # calculate image size
        xlim = (bbox[2] - bbox[0]) / self.pixel_density
        ylim = (bbox[3] - bbox[1]) / self.pixel_density
        
        # catch the special case when a null query would be sent
        if xlim % self.size_restriction[0] == 0: xlim += 10
        if ylim % self.size_restriction[1] == 0: ylim += 10
        
        ## get the relative image sizes for the splits
        # calculate lower edges
        # these start at 0 and increase by the maximum pixel amount for as many times as necessary
        x_mins = [x * self.size_restriction[0] for x in range(int(xlim // self.size_restriction[0]) + 1)]
        y_mins = [y * self.size_restriction[1] for y in range(int(ylim // self.size_restriction[1]) + 1)]
        # calculate upper edges
        # these are the lower edges and the actual upper edge
        x_maxs = [x * self.size_restriction[0] for x in range(int(xlim // self.size_restriction[0]) + 1)][1:] +\
          [(xlim // self.size_restriction[0]) * self.size_restriction[0] + (xlim % self.size_restriction[0])]
        y_maxs = [y * self.size_restriction[1] for y in range(int(ylim // self.size_restriction[1]) + 1)][1:] +\
          [(ylim // self.size_restriction[1]) * self.size_restriction[1] + (ylim % self.size_restriction[1])]
        
        # turn into bbox format
        splits = array([[[None] * 4] * len(y_mins)] * len(x_mins))
        for i in range(len(x_mins)):
            for j in range(len(y_mins)):
                splits[i][j] = [x_mins[i], y_mins[j], x_maxs[i], y_maxs[j]]
           
        # offset and fix to bboxes
        query_bboxes = [[[splits[i][j][0] * self.pixel_density + bbox[0],
                          splits[i][j][1] * self.pixel_density + bbox[1],
                          splits[i][j][2] * self.pixel_density + bbox[0],
                          splits[i][j][3] * self.pixel_density + bbox[1]] for j in range(len(y_mins))] for i in range(len(x_mins))]
        
        # bring splits into PIL format (origin in top-left)
        PIL_coords = array([[[None] * 2] * len(y_mins)] * len(x_mins))
        for i in range(len(x_mins)):
            for j in range(len(y_mins)):
                PIL_coords[i][j] = [splits[i][j][0], ylim - splits[i][j][3]]
                
        # return query shape
        query_shape = (len(x_mins), len(y_mins))
        
        return(PIL_coords, query_bboxes, query_shape)
    
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
                self.size_restriction = (5999, 5999) # actual limits are at 8000,8000; for tiling purposes decreased to 6000,6000
                self.wfs_service = "https://isk.geobasis-bb.de/ows/aktualitaeten_wfs?"
                self.wfs_typename = "app:dop20rgbi_2016_2018_single"
                self.wfs_datepos = "app:creationdate"
                self.grid_wfs_service = "https://isk.geobasis-bb.de/ows/blattschnitte_wfs?"
                self.grid_wfs_typename = "app:kachelung1km"
                self.wfs_gridpos = "app:kachelnummer"
        
        self.__establish_wms_connection()
        self.__establish_wfs_connection()
        self.__establish_grid_wfs_connection()
        #self.__establish_height_wms_connection()
    
    def query(self, spatial_bounds, ids, offset = 20, crs = 25833):
        
        n = 0
        
        # get a list of existing imagery
        existing_files = listdir(self.storage_directory + "/raw/")
        
        # get state borders to identify problematic cases spanning two states
        state_borders = read_file("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders/gadm41_DEU_1.json").to_crs("25833")
        
        for bbox in spatial_bounds:
            
            if (len([x for x in [compile(ids[n]).search(x) for x in existing_files] if x is not None]) > 0):
                print("--- Skipping already downloaded image ---")
                n += 1
                continue
            
            # turn bbox into shapely polygon
            tmp_pol = Polygon([(bbox[0], bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3]), (bbox[2], bbox[1])])
            
            if (state_borders.intersects(GeoSeries([tmp_pol] * state_borders.shape[0], crs = "25833")).sum()) > 1:
                print("--- Skipping problematic case across state borders ---")
                n += 1
                continue
            
            print(f"--- Querying for image {n+1} ---")
            
            try:
            
                # project the bbox if necessary
                if(crs != self.import_crs):
                    query_bbox = self.__project_bounding_box(bbox, crs)
                else:
                    query_bbox = bbox
                
                # extend image boundaries
                query_bbox[[0,1]] = floor(query_bbox[[0,1]] - offset)
                query_bbox[[2,3]] = ceil(query_bbox[[2,3]] + offset)
                
                # calculate total size
                total_size = self.__calculate_image_size(query_bbox)
                
                # calculate splits if necessary
                PIL_coords, query_bboxes, query_shape = self.__get_split_parameters(query_bbox)
                
                print(query_shape)
                
                # prepare output vectors
                imgs = array([[None] * query_shape[1]] * query_shape[0])
                timestamps = array([[None] * query_shape[1]] * query_shape[0])
                grids = []

                for i in range(query_shape[0]):
                    for j in range(query_shape[1]):
                        
                        print(str(i) + "_" + str(j))
                        
                        sleep(.5)
                        
                        query_bbox = query_bboxes[i][j]
                        
                        # query the imagery from the WMS service
                        imgs[i][j] = self.wms.getmap(
                            layers = [self.wms_layer],
                            srs = "EPSG:" + str(self.import_crs),
                            bbox = query_bbox,
                            size = self.__calculate_image_size(query_bbox),
                            format = "image/jpeg").read()
                        
                        # query timestamp from the WFS service
                        wfs_response = self.wfs.getfeature(typename = self.wfs_typename,
                                                        bbox = tuple(query_bbox), 
                                                        srsname = "EPSG:" + str(self.import_crs)).read()
                        timestamps[i][j] = BeautifulSoup(wfs_response, features = "xml").find(self.wfs_datepos).text
                        
                        # query grids from the WFS service
                        wfs_response = self.wfs_grid.getfeature(typename = self.grid_wfs_typename,
                                                        bbox = tuple(query_bbox), 
                                                        srsname = "EPSG:" + str(self.import_crs)).read()
                        for x in BeautifulSoup(wfs_response, features = "xml").find_all(self.wfs_gridpos): 
                            if x is not None: 
                                grids.append(x.text)
                        
                ###
                ## Imagery
                    
                # concat the queried images
                outimage = Image.new('RGB', tuple([int(x) for x in total_size]))
                for i in range(query_shape[0]):
                    for j in range(query_shape[1]):
                        outimage.paste(Image.open(BytesIO(imgs[i][j])), tuple([int(x) for x in PIL_coords[i][j]]))
                
                # export as jpg first
                outimage.save(self.storage_directory + "/raw/" + 
                            ids[n] + "_" + timestamps.flat[0] + ".jpg")
                
                # turn jpg into numpy array
                tmp_np = asarray(outimage, dtype = float64)[::-1]
                
                # create xarray
                tmp_xd = Dataset(data_vars = {"red": (["y", "x"], tmp_np[:,:,0]),
                                            "green": (["y", "x"], tmp_np[:,:,1]),
                                            "blue": (["y", "x"], tmp_np[:,:,2])},
                                #data_vars = {"rgb": (["x", "y"], tmp_np)},
                                coords = {"y": (["y"], arange(tmp_np.shape[0]) * self.pixel_density + bbox[1]),
                                        "x": (["x"], arange(tmp_np.shape[1]) * self.pixel_density + bbox[0])},
                                attrs = {"grids": unique(grids)})
                
                # convert type
                # set output crs
                tmp_xd.rio.write_crs(25833, inplace = True)
                tmp_xd.rio.set_spatial_dims(x_dim = "x", y_dim = "y", inplace = True)
                tmp_xd.rio.write_coordinate_system(inplace = True)
                tmp_xd.rio.write_transform(inplace = True)
                # export the nc
                tmp_xd.to_netcdf(self.storage_directory + "/raw/" + ids[n] +  "_" + timestamps.flat[0] + ".nc")
            
            except:
                pass
            
            finally:
                n += 1
            
        print("--- Successfully queried and exported " + str(n) + " images ---")
  
"""       
if __name__ == "__main__":
    import geopandas as gpd
    driveways = gpd.read_file("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg.geojson").\
        dissolve(by = "link_id", as_index = False)
    imagery_downloader = data_imagery("brandenburg")
    imagery_downloader.query(driveways.bounds.values[[1]], driveways.link_id[[1]].reset_index(drop = True))
    print(driveways.link_id[[1]].reset_index(drop = True))
"""