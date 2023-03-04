#from modules.data.data_abstract import data_abstract
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from bs4 import BeautifulSoup
from numpy import array, asarray, unique, expand_dims, arange, ceil, floor, float64, isnan
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
        return(GeoSeries(polygon).set_crs(bbox_crs).to_crs(self.import_crs).bounds.values[0])
    
    # calculates the output image size according to the provided density and bbox
    def __calculate_image_size(self, bbox):
        return([((bbox[2] - bbox[0]) / self.pixel_density), 
                ((bbox[3] - bbox[1]) / self.pixel_density)])
    
    # calculate parameters for chunked query
    def __get_split_parameters(self, bbox):
        # calculate image size
        xlim = (bbox[2] - bbox[0]) / self.pixel_density
        ylim = (bbox[3] - bbox[1]) / self.pixel_density
        
        # enforce minimum image size
        #xlim = min(xlim, 1000)
        #ylim = min(ylim, 1000)
        
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
        if self.state == "brandenburg":
            self.pixel_density = .2
            self.import_crs = 25833
            self.query_wms = True
            self.wms_service = "https://isk.geobasis-bb.de/mapproxy/dop20_2016_2018/service/wms?"
            self.wms_layer = "dop20_bebb_2016_2018_farbe"
            self.size_restriction = (5999, 5999) # actual limits are at 8000,8000; for tiling purposes decreased to 6000,6000
            self.query_wfs = True
            self.wfs_service = "https://isk.geobasis-bb.de/ows/aktualitaeten_wfs?"
            self.wfs_typename = "app:dop20rgbi_2016_2018_single"
            self.wfs_datepos = "app:creationdate"
            self.query_grid_wfs = True
            self.grid_wfs_service = "https://isk.geobasis-bb.de/ows/blattschnitte_wfs?"
            self.grid_wfs_typename = "app:kachelung1km"
            self.wfs_gridpos = "app:kachelnummer"
            self.handle_watermark = False
            self.sleep_time = 1
            
        if self.state == "berlin":
            self.pixel_density = .2
            self.import_crs = 25833
            self.query_wms = True
            self.wms_service = "https://isk.geobasis-bb.de/mapproxy/dop20_2016_2018/service/wms?"
            self.wms_layer = "dop20_bebb_2016_2018_farbe"
            self.size_restriction = (5999, 5999) # actual limits are at 8000,8000; for tiling purposes decreased to 6000,6000
            self.query_wfs = False
            self.query_grid_wfs = True
            self.grid_wfs_service = "https://isk.geobasis-bb.de/ows/blattschnitte_wfs?"
            self.grid_wfs_typename = "app:kachelung1km"
            self.wfs_gridpos = "app:kachelnummer"
            self.handle_watermark = False
            self.sleep_time = 1
            
        if self.state == "mecklenburg-vorpommern":
            self.pixel_density = .1
            self.import_crs = 25833
            self.query_wms = True
            self.wms_service = "https://www.geodaten-mv.de/dienste/adv_dop?"
            self.wms_layer = "mv_dop"
            self.size_restriction = (4190, 4190) # just below maxmimum of server
            self.query_wfs = False
            self.query_grid_wfs = False
            self.handle_watermark = True
            self.handle_watermark_pos = "top-left"
            self.watermark_shape = [x * self.pixel_density for x in (100, 20)]
            self.sleep_time = 1
            
        if self.state == "sachsen-anhalt":
            self.pixel_density = .2
            self.import_crs = 25833
            self.query_wms = True
            self.wms_service = "https://www.geodatenportal.sachsen-anhalt.de/wss/service/ST_LVermGeo_GDI_DOP20/guest?"
            self.wms_layer = "lsa_lvermgeo_dop20"
            self.size_restriction = (4000, 4000)
            self.query_wfs = False
            self.query_grid_wfs = False
            self.handle_watermark = True
            self.handle_watermark_pos = "bottom-right"
            self.watermark_shape = [x * self.pixel_density for x in (250, 50)]
            self.sleep_time = 1
            
        if self.state == "schleswig-holstein":
            self.pixel_density = .2
            self.import_crs = 25833
            self.query_wms = True
            self.wms_service = "https://service.gdi-sh.de/WMS_SH_DOP20col_OpenGBD?"
            self.wms_layer = "sh_dop20_rgb"
            self.size_restriction = (2000, 2000) # the service is slow, small sizes minimize timeout errors
            self.query_wfs = False
            self.query_grid_wfs = False
            self.handle_watermark = False
            self.sleep_time = 5
            
        if self.state == "niedersachsen":
            self.pixel_density = .2
            self.import_crs = 25832 #!
            self.query_wms = True
            self.wms_service = "https://www.geobasisdaten.niedersachsen.de/doorman/noauth/wms_ni_dop?"
            self.wms_layer = "dop20"
            self.size_restriction = (4000, 4000)
            self.query_wfs = False
            self.query_grid_wfs = False
            self.handle_watermark = False
            self.sleep_time = 1

        if self.state == "hamburg":
            self.pixel_density = .2
            self.import_crs = 25832 #!
            self.query_wms = True
            self.wms_service = "https://geodienste.hamburg.de/HH_WMS_DOP_belaubt?"
            self.wms_layer = "DOP_belaubt_highres"
            self.size_restriction = (4000, 4000)
            self.query_wfs = False
            self.query_grid_wfs = False
            self.handle_watermark = False
            self.sleep_time = 1
                        
        if self.query_wms:
            self.__establish_wms_connection()
        if self.query_wfs:
            self.__establish_wfs_connection()
        if self.query_grid_wfs:
            self.__establish_grid_wfs_connection()
    
    def query(self, spatial_bounds, ids, offset = 20, crs = 25833):
        
        n = 0
        
        # get a list of existing imagery
        existing_files = listdir(self.storage_directory + "/raw/")
        
        # get state borders to identify problematic cases spanning two states
        state_borders = read_file("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders/gadm41_DEU_1.json").to_crs("25833")
        
        for bbox in spatial_bounds:
            
            if all([isnan(x) for x in bbox]):
                print("--- Skipping unbounded polygon ---")
                n += 1
                continue
            
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
            
            if (tmp_pol.area > 16000000):
                print("--- Skipping large query ---")
                n += 1
                continue
            
            print(f"--- Querying for image {n+1} ---")
            
            error = True
            while error:
            
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
                    
                    print(f"*** SHAPE: {query_shape} ***")
                    
                    # prepare output vectors
                    imgs = array([[None] * query_shape[1]] * query_shape[0])
                    timestamps = array([[None] * query_shape[1]] * query_shape[0])
                    watermark_imgs = array([[None] * query_shape[1]] * query_shape[0])
                    grids = []

                    for i in range(query_shape[0]):
                        for j in range(query_shape[1]):
                            
                            print(f"*** Row: {str(i)}, Column: {str(j)} ***")
                            
                            sleep(self.sleep_time)
                            
                            query_bbox = [round(x) for x in query_bboxes[i][j]]
                            
                            if self.query_wms:
                                # query the imagery from the WMS service
                                imgs[i][j] = self.wms.getmap(
                                    layers = [self.wms_layer],
                                    srs = "EPSG:" + str(self.import_crs),
                                    bbox = query_bbox,
                                    size = [round(x) for x in self.__calculate_image_size(query_bbox)],
                                    format = "image/jpeg").read()
                                
                            if self.handle_watermark:
                                if (self.handle_watermark_pos == "top-left"):
                                    tmp = query_bbox
                                    tmp[2] = tmp[0] + self.watermark_shape[0]
                                    tmp[0] -= self.watermark_shape[0]
                                    tmp[1] = tmp[3] - self.watermark_shape[1]
                                if (self.handle_watermark_pos == "bottom-right"):
                                    tmp = query_bbox
                                    tmp[0] = tmp[2] - self.watermark_shape[0]
                                    tmp[2] += self.watermark_shape[0]
                                    tmp[3] = tmp[1] + self.watermark_shape[1]
                                # query the imagery from the WMS service
                                watermark_imgs[i][j] = self.wms.getmap(
                                    layers = [self.wms_layer],
                                    srs = "EPSG:" + str(self.import_crs),
                                    bbox = [int(x) for x in tmp],
                                    size = [round(x) for x in self.__calculate_image_size(tmp)],
                                    format = "image/jpeg").read()
                            
                            if self.query_wfs:
                                # query timestamp from the WFS service
                                wfs_response = self.wfs.getfeature(typename = self.wfs_typename,
                                                                bbox = tuple(query_bbox), 
                                                                srsname = "EPSG:" + str(self.import_crs)).read()
                                timestamps[i][j] = BeautifulSoup(wfs_response, features = "xml").find(self.wfs_datepos).text
                            
                            if self.query_grid_wfs:
                            # query grids from the WFS service
                                wfs_response = self.wfs_grid.getfeature(typename = self.grid_wfs_typename,
                                                                bbox = tuple(query_bbox), 
                                                                srsname = "EPSG:" + str(self.import_crs)).read()
                                for x in BeautifulSoup(wfs_response, features = "xml").find_all(self.wfs_gridpos): 
                                    if x is not None: 
                                        grids.append(x.text)
                            
                    ###
                    ## Imagery
                    
                    if self.query_wms:
                        # concat the queried images
                        outimage = Image.new('RGB', tuple([int(x) for x in total_size]))
                        for i in range(query_shape[0]):
                            for j in range(query_shape[1]):
                                outimage.paste(Image.open(BytesIO(imgs[i][j])), 
                                               tuple([int(x) for x in PIL_coords[i][j]]))
                                
                        if self.handle_watermark:
                            if (self.handle_watermark_pos == "top-left"):
                                for i in range(query_shape[0]):
                                    for j in range(query_shape[1]):
                                        outimage.paste(Image.open(BytesIO(watermark_imgs[i][j])).crop(((self.watermark_shape[0] / self.pixel_density),
                                                                                                    0,
                                                                                                    (self.watermark_shape[0] / self.pixel_density) * 2,
                                                                                                    (self.watermark_shape[1] / self.pixel_density))), 
                                                    tuple([int(x) for x in PIL_coords[i][j]]))
                            if (self.handle_watermark_pos == "bottom-right"):
                                for i in range(query_shape[0]):
                                    for j in range(query_shape[1]):
                                        tile_size = Image.open(BytesIO(imgs[i][j])).size
                                        outimage.paste(Image.open(BytesIO(watermark_imgs[i][j])).crop((0,
                                                                                                    0,
                                                                                                    (self.watermark_shape[0] / self.pixel_density),
                                                                                                    (self.watermark_shape[1] / self.pixel_density))), 
                                                    tuple([int(x) for x in [PIL_coords[i][j][0] + tile_size[0] - (self.watermark_shape[0] / self.pixel_density),
                                                                            PIL_coords[i][j][1] + tile_size[1] - (self.watermark_shape[1] / self.pixel_density)]]))
                               
                        """
                        Image.open(BytesIO(watermark_imgs[i][j])).crop(((self.watermark_shape[0] / self.pixel_density),
                                                                                                    0,
                                                                                                    (self.watermark_shape[0] / self.pixel_density) * 2,
                                                                                                    (self.watermark_shape[1] / self.pixel_density))).save("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/test.jpg")
                        outimage.crop((PIL_coords[i][j][0] + tile_size[0] - 250,
                                       PIL_coords[i][j][1] + tile_size[1] - 50,
                                       PIL_coords[i][j][0] + tile_size[0],
                                       PIL_coords[i][j][1] + tile_size[1])).save("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/test.jpg")
                        Image.open(BytesIO(watermark_imgs[i][j])).crop(((self.watermark_shape[0] / self.pixel_density),
                                                                                                    0,
                                                                                                    (self.watermark_shape[0] / self.pixel_density) * 2,
                                                                                                    (self.watermark_shape[1] / self.pixel_density))).save("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/test.jpg")
                        outimage.save("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/test.jpg")"""
                        
                        # export as jpg first
                        if self.query_wfs:
                            outimage.save(self.storage_directory + "/raw/" + ids[n] + "_" + timestamps.flat[0] + ".jpg")
                        else:
                            outimage.save(self.storage_directory + "/raw/" + ids[n] + ".jpg")
                            
                        # turn jpg into numpy array
                        tmp_np = asarray(outimage, dtype = float64)[::-1]
                        
                        # create xarray
                        if self.query_grid_wfs:
                            tmp_xd = Dataset(data_vars = {"red": (["y", "x"], tmp_np[:,:,0]),
                                                          "green": (["y", "x"], tmp_np[:,:,1]),
                                                          "blue": (["y", "x"], tmp_np[:,:,2])},
                                            coords = {"y": (["y"], arange(tmp_np.shape[0]) * self.pixel_density + bbox[1]),
                                                      "x": (["x"], arange(tmp_np.shape[1]) * self.pixel_density + bbox[0])},
                                            attrs = {"grids": unique(grids)})
                        else:
                            tmp_xd = Dataset(data_vars = {"red": (["y", "x"], tmp_np[:,:,0]),
                                                        "green": (["y", "x"], tmp_np[:,:,1]),
                                                        "blue": (["y", "x"], tmp_np[:,:,2])},
                                            coords = {"y": (["y"], arange(tmp_np.shape[0]) * self.pixel_density + bbox[1]),
                                                      "x": (["x"], arange(tmp_np.shape[1]) * self.pixel_density + bbox[0])})
                            
                        # convert type
                        # set output crs
                        tmp_xd.rio.write_crs(25833, inplace = True)
                        tmp_xd.rio.set_spatial_dims(x_dim = "x", y_dim = "y", inplace = True)
                        tmp_xd.rio.write_coordinate_system(inplace = True)
                        tmp_xd.rio.write_transform(inplace = True)
                        # export the nc
                        if self.query_wfs:
                            tmp_xd.to_netcdf(self.storage_directory + "/raw/" + ids[n] +  "_" + timestamps.flat[0] + ".nc")
                        else:
                            tmp_xd.to_netcdf(self.storage_directory + "/raw/" + ids[n] + ".nc")
                            
                        error = False
                        n += 1
                
                except:
                    sleep(5)
            
        print("--- Successfully queried and exported " + str(n) + " images ---")
  
"""       
if __name__ == "__main__":
    import geopandas as gpd
    driveways = gpd.read_file("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/schleswig-holstein_polygons.geojson").\
        dissolve(by = "link_id", as_index = False)
    imagery_downloader = data_imagery("schleswig-holstein")
    imagery_downloader.query(driveways.bounds.values, driveways.link_id)
"""