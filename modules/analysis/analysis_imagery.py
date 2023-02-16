#from modules.analysis.analysis_abstract import analysis_abstract 

import os, re
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely
import xarray
import rioxarray
import PIL
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import torch
import torch.nn as nn
import torch.optim as optim
import albumentations as A
from albumentations.pytorch import ToTensorV2

from torchvision.models.segmentation.deeplabv3 import DeepLabHead
from torchvision.models.segmentation.fcn import FCNHead
from torchvision.models.segmentation import DeepLabV3_ResNet101_Weights
from torchvision import models

class analysis_imagery(): #analysis_abstract
    """
    A class implementing the analysis of land cover within turnoff polygons based on a neural network
    
    Args:
        storage_directory (str): The path to the storage directory of OSM data
        
    Methods:
        analyze: Calculates relative land cover within the turnoff
    """
    
    def __get_image_trans(state):
        if state == "brandenburg":
            return 2
            
    def __build_transforms(self): 
            
        return A.Compose([
            A.Normalize(mean=(0.485, 0.456, 0.406), 
                        std=(0.229, 0.224, 0.225)),
            ToTensorV2(),
            ],)
        
    def __get_splits(self, pic_size):
        """
        
        A function calculating square splits ready to be segmented by a model

        Args:
            pic_size (iterable): a tuple of size 2 (x,y) of the image size

        """
        
        lim_x = 800
        lim_y = 800
    
        xmax = pic_size[0]
        ymax = pic_size[1]
        
        n = 0
        out = [(None, None)] * ((xmax // lim_x + 1) * (ymax // lim_y + 1))

        for xsplit in range(xmax // lim_x + 1):
            for ysplit in range(ymax // lim_y + 1):
                
                ## initialize ignoring limits
                # splits
                xsplit_lower = xsplit * lim_x
                xsplit_upper = (xsplit + 1) * lim_x
                ysplit_lower = ysplit * lim_y
                ysplit_upper = (ysplit + 1) * lim_y
                # writes
                xwrite_lower = xsplit * lim_x
                xwrite_upper = (xsplit + 1) * lim_x
                ywrite_lower = ysplit * lim_y
                ywrite_upper = (ysplit + 1) * lim_y
                # reads
                xread_lower = 0
                xread_upper = lim_x
                yread_lower = 0
                yread_upper = lim_y
                
                ## if exceeding limit, set to limit
                # splits
                if xmax < (xsplit + 1) * lim_x:
                    xsplit_lower = xmax - lim_x
                    xsplit_upper = xmax
                if ymax < (ysplit + 1) * lim_y:
                    ysplit_lower = ymax - lim_y
                    ysplit_upper = ymax
                # writes
                if xmax < (xsplit + 1) * lim_x:
                    xwrite_lower = xsplit * lim_x
                    xwrite_upper = xmax
                if ymax < (ysplit + 1) * lim_y:
                    ywrite_lower = ysplit * lim_y
                    ywrite_upper = ymax
                # reads
                if xmax < (xsplit + 1) * lim_x:
                    xread_lower = xread_upper - (xmax - xsplit * lim_x)
                if ymax < (ysplit + 1) * lim_y:
                    yread_lower = yread_upper - (ymax - ysplit * lim_y)
                    
                ## write to out
                out[n] = ([xsplit_lower, ysplit_lower, xsplit_upper, ysplit_upper], 
                        [xwrite_lower, ywrite_lower, xwrite_upper, ywrite_upper],
                        [xread_lower, yread_lower, xread_upper, yread_upper])
                n += 1
                
        return out
    
    def __correct_overshot(self, splits, bbox, bbox_image):
        """
        
        A function dynamically extending the image in case the turnoffs boundary is smaller than one predicted image

        Args:
            pic_size (iterable): a tuple of size 2 (x,y) of the image size

        """
        
        
        # test if x range is overshot
        f_xover = any(any([x[0] < 0, x[2] < 0]) for x in splits[0])
        # test if y range is overshot
        f_yover = any(any([x[1] < 0, x[3] < 0]) for x in splits[0])
        #
        f_problem = False
        
        if f_xover:
            # get range above x
            a_xover = - splits[0][0][0]
            # get potential exceeding space from bboxes
            p_xupper = bbox_image["maxx"] - bbox["maxx"]
            p_xlower = bbox["minx"] - bbox_image["minx"]
            # check if the upper potential covers the range
            if p_xupper >= a_xover:
                # extend the queried range above only
                bbox["maxx"] += a_xover
            else:
                # extend the queried range above as much as possible
                bbox["maxx"] += p_xupper
                # check if the lower potential covers the remaining range
                if p_xlower >= a_xover - p_xupper:
                    # further extend the queried range below as much as possible
                    bbox["minx"] -= a_xover - p_xupper
                else:
                    # if both upper and lower combined do not suffice, flag an error
                    f_problem = True
        if f_yover:
            # get range above y
            a_yover = - splits[0][0][1]
            # get potential exceeding space from bboxes
            p_yupper = bbox_image["maxy"] - bbox["maxy"]
            p_ylower = bbox["miny"] - bbox_image["miny"]
            # check if the upper potential covers the range
            if p_yupper >= a_yover:
                # extend the queried range above only
                bbox["maxy"] += a_yover
            else:
                # extend the queried range above as much as possible
                bbox["maxy"] += p_yupper
                # check if the lower potential covers the remaining range
                if p_ylower >= a_yover - p_yupper:
                    # further extend the queried range below as much as possible
                    bbox["miny"] -= a_yover - p_yupper
                else:
                    # if both upper and lower combined do not suffice, flag an error
                    f_problem = True
        
        return f_problem, bbox
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery"):
        self.storage_directory = storage_directory                
    
    def analyze(self, imagery, polygons, model, inset = 12, model_pixel_density = .3):
        """
        
        A function calculating relative land cover for a set of images given polygons and a model for prediction

        Args:
            imagery (str): The paths to the files containing imagery (can be either .jpg or .nc)
            polygons (str): The path to the GeoJSON containing all turnoff polygons
            model (str): The path to the stored model for prediction
            inset (int): the inset from street center to take values from
            model_pixel_density (float): the pixel density of the data used in the model

        """
        
        # get the driveway boundaries
        driveways = gpd.read_file(polygons)
        
        # handle single image
        if not isinstance(imagery, list):
            imagery = [imagery]
            
        ## load the model 
        # define device to load to
        if torch.cuda.is_available():
            print("--- Using GPU ---")
            device = torch.device("cuda")
            torch.set_default_tensor_type(torch.cuda.FloatTensor)
        else:
            print("--- Using CPU ---")
            device = torch.device("cpu")
            torch.set_default_tensor_type(torch.FloatTensor)
            
        # define function to load checkpoint
        def load_checkpoint(checkpoint, model):
            print("=> Loading checkpoint")
            model.load_state_dict(checkpoint["state_dict"])
            
        # define model architecture
        trained_model = models.segmentation.deeplabv3_resnet101()
        trained_model.classifier = DeepLabHead(2048, 6)
        trained_model.aux_classifier = None
        # move the model to the defined device
        trained_model = trained_model.to(device = device)
        # load the checkpoint
        load_checkpoint(torch.load(model, map_location=torch.device(device)), trained_model)
        
        for idx, image_path in enumerate(imagery):
            
            print(f"--- Processing image {idx + 1} ---")
            
            # get image
            image = rioxarray.open_rasterio(image_path)
            
            # get bbox of image
            bbox_image = {"minx": np.floor(image.x.min().values), "miny": np.floor(image.y.min().values), 
                          "maxx": np.ceil(image.x.max().values), "maxy": np.ceil(image.y.max().values)}
            
            # get road ID and state name
            driveway_id = re.compile("(?<=raw/)\w\w_\w\w_\w\w\w\w").search(image_path).group(0)
            state_name = re.compile("(?<=raw/)\w\w").search(image_path).group(0)
            
            ###
            # GET AGGREGATE MEASUREMENTS
            ###
            def worker(x):
                
                # get necesarry transforms
                val_transform = self.__build_transforms()
                
                # skip if area too small
                if x.geometry.buffer(-inset).area == 0:
                    return pd.Series([0] * 6, index = ["lc_unknown", "lc_background", "lc_building", "lc_road",
                                                       "lc_forest", "lc_agriculture"])
                
                # get bounds
                bbox = gpd.GeoSeries(x.geometry, crs = 25833).bounds.iloc[0]
                bbox = {"minx": np.floor(bbox["minx"]), "miny": np.floor(bbox["miny"]), 
                        "maxx": np.ceil(bbox["maxx"]), "maxy": np.ceil(bbox["maxy"])}
                
                # get submatrix
                pic = image.rio.clip_box(bbox["minx"], bbox["miny"], bbox["maxx"], bbox["maxy"])
                
                # resize with factor
                pic_resized = pic.interp(x = np.arange(pic["x"].values[0], pic["x"].values[-1] + 1, model_pixel_density),
                                         y = np.arange(pic["y"].values[-1], pic["y"].values[0] + 1, model_pixel_density), method = "nearest")
                
                # get splits
                splits = self.__get_splits([pic_resized.dims["x"], pic_resized.dims["y"]])
                
                # correct potential overshot
                f_problem, bbox = self.__correct_overshot(splits, bbox, bbox_image)
                
                # get corrected submatrix
                pic = image.rio.clip_box(bbox["minx"], bbox["miny"], bbox["maxx"], bbox["maxy"])
                
                # resize with factor
                pic_resized = pic.interp(x = np.arange(pic["x"].values[0], pic["x"].values[-1] + 1, model_pixel_density),
                                         y = np.arange(pic["y"].values[-1], pic["y"].values[0] + 1, model_pixel_density), method = "nearest")
                
                # get corrected splits
                splits = self.__get_splits([pic_resized.dims["x"], pic_resized.dims["y"]])
                    
                """
                # get splits for classification
                splits = ((pic_resized.dims["x"] // 1000 + 1), (pic_resized.dims["y"] // 1000 + 1))
                
                # pad with NA to allow splits
                pic_resized = pic_resized.pad(x = [0, (splits[0] * 1000 - pic_resized.dims["x"])], 
                                              y = [0, (splits[1] * 1000 - pic_resized.dims["y"])])
                
                # replace NA with white
                pic_resized = pic_resized.fillna(255)
                """
                
                # create output matrix
                pic_resized = pic_resized.assign(classification = lambda x: x.red * 0)
                
                for p_split in splits:
                        
                    # get subset with exact size and fill NA at border of interpolation
                    split = pic_resized.isel(x = range(p_split[0][0], p_split[0][2]), y = range(p_split[0][1], p_split[0][3])).ffill("y").ffill("x")
                    # transform image
                    # RGB, x, y
                    cut_transformed = val_transform(image = np.stack([np.squeeze(split[dim].to_numpy()) for dim in ["red", "green", "blue"]]).transpose())["image"].to(device)
                    
                    # get predictions
                    trained_model.eval()
                    with torch.no_grad():
                        # Use image + pretend batch size of 1
                        cut_transformed = cut_transformed.unsqueeze(0)

                        # Compute probabilities
                        probs = torch.nn.Softmax(trained_model(cut_transformed)['out']).dim
                        # probs = torch.nn.Softmax(model(pic)).dim
                        
                        # Get predictions by choosing highest probability 
                        preds = torch.argmax(probs, axis = 1).squeeze(0)
                        
                        # write predictions to the data
                        pic_resized.classification[0, range(p_split[1][1], p_split[1][3]), range(p_split[1][0], p_split[1][2])] = xarray.DataArray(preds.transpose(1,0).cpu())[range(p_split[2][1], p_split[2][3]), range(p_split[2][0], p_split[2][2])]
                        
                        del cut_transformed
                
                # cut out relevant values and get stats   
                #u, counts = np.unique(pic_resized.classification.sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).rio.clip([x.geometry.buffer(-inset)]).values, return_counts = True)
                
                # write original image
                xarray.plot.imshow(pic_resized.sel(band=1).drop_vars("classification").to_array("band").sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).rio.clip([x.geometry]).drop_vars("spatial_ref").fillna(255).astype("int"), rgb = "band", figsize = (5, 5))
                plt.axis('off')
                plt.savefig(self.storage_directory + "/analysis/imagery/rgb/" + x.link_id + "_" + str(int(x.id)) + ".png", bbox_inches = "tight")
                plt.close()
                
                # write prediction image
                xarray.plot.imshow(pic_resized.classification.sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).rio.clip([x.geometry]).squeeze("band", drop = True).drop_vars("spatial_ref"), 
                                   add_colorbar = True, 
                                   cmap = ListedColormap([[x/255 for x in y] + [1] for y in [(0, 0, 0), (255, 255, 225), (255,  0, 255),
                                                                                             (255, 0, 0), (0, 130, 0), (255, 200, 0)]]),
                                   vmin = 0, vmax = 5, levels = 6, extend = "max")
                plt.gca().images[0].colorbar.set_ticklabels(["unknown", "background", "building", "road",
                                                              "forest", "agriculture"])  
                plt.axis('off')
                plt.savefig(self.storage_directory + "/analysis/imagery/predictions/" + x.link_id + "_" + str(int(x.id)) + ".png", bbox_inches = "tight", transparent = True)
                plt.close()
                
                # group stats and return
                tmp = pd.Series(pic_resized.classification.sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).rio.clip([x.geometry.buffer(-inset)]).values.flatten()).value_counts()
                tmp.index = tmp.index.map({0: "lc_unknown", 1: "lc_background", 2: "lc_building", 3: "lc_road",
                                           4: "lc_forest", 5: "lc_agriculture"})
                return tmp

                """
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(1, 2, figsize=(10, 5))
                #xarray.plot.imshow(pic_resized.red.sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).squeeze("band", drop = True), ax = ax[0])
                xarray.plot.imshow(pic_resized.sel(band=1).drop_vars("classification").to_array("band").astype("int").sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).rio.clip([x.geometry]), rgb = "band", ax = ax[0])
                xarray.plot.imshow(pic_resized.classification.sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).rio.clip([x.geometry]).squeeze("band", drop = True), ax = ax[1],
                add_colorbar = False, 
                                   cmap = ListedColormap([[x/255 for x in y] + [1] for y in [(0, 0, 0), (255, 255, 225), (255,  0, 255), (255, 0, 0),
                                                                                             (0,  0,  255), (128, 128, 128), (0, 130, 0), (255, 200, 0)]]),
                                   vmin = 0, vmax = 7, levels = 8, extend = "max")
                fig.savefig("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/analysis/test.png")
                
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(1, 2, figsize=(10, 5))
                xarray.plot.imshow(pic_resized.sel(band=1).drop_vars("classification").to_array("band").astype("int").sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()), rgb = "band", ax = ax[0])
                xarray.plot.imshow(pic_resized.classification.sel(x=pic_resized.x.notnull(), y = pic_resized.y.notnull()).squeeze("band", drop = True), ax = ax[1])
                fig.savefig("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/analysis/test.png")
                
                xarray.plot.imshow(split.sel(band=1).drop_vars("classification").to_array("band").astype("int").sel(x=split.x.notnull(), y = split.y.notnull()).rio.clip([x.buffer(-12)]), rgb = "band")
                plt.savefig("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/analysis/test.png") 
                """
            
            # apply definition to all polygons
            driveways_out = driveways.copy().loc[driveways.link_id == driveway_id,["link_id", "id"]]
            driveways_out = driveways_out.join(driveways.loc[driveways.link_id == driveway_id, :].apply(worker, axis = 1))

            # get existing measurements
            if os.path.isfile(self.storage_directory + "/analysis/" + state_name + ".csv"):
                tmp = pd.read_csv(self.storage_directory + "/analysis/" + state_name + ".csv")
                # export table with mapping from link_id to land cover
                pd.concat([tmp[tmp.link_id != driveway_id], driveways_out]).\
                    to_csv(self.storage_directory + "/analysis/" + state_name + ".csv", index = False) 
            else:
                # export table with mapping from link_id to land cover
                driveways_out.to_csv(self.storage_directory + "/analysis/" + state_name + ".csv", index = False)      

#"""
# --- For testing outside the workflow ---   
if __name__ == "__main__":
    c_analysis_imagery = analysis_imagery()
    c_analysis_imagery.analyze("/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/imagery/raw/BB_ML_0001_2017-08-29.nc", 
                         "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/OSM/processed/brandenburg_polygons.geojson",
                         "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/trained_models/love_checkpoint_DLV3_6classes.pth.tar")
#"""