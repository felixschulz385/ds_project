"""
This class downloads the complete OSM source data at the smallest available file size for Germany
"""

from modules.data.data_abstract import data_abstract
import requests
import re
from os import makedirs
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from pandas import DataFrame, concat

class data_OSM(data_abstract):
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/borders"):
        self.storage_directory = storage_directory
    
    def query(self, spatial_bounds = "available", temporal_bounds = "available", crs = 25833):
        
        print("Preparing...")
        ## prepare a lookup table
        lookup_table = DataFrame(columns = ["subregion", "subsubregion", "path", "link"])
        
        ## get an overview on all available subregions
        # retrieve the Geofabrik overview page on Germany
        soup = BeautifulSoup(requests.get("https://download.geofabrik.de/europe/germany.html").content, "lxml")
        
        # extract all subregions 
        subregions = ["https://download.geofabrik.de/europe/" + subregion["href"] for subregion in soup.find_all("a", href = re.compile("germany/.*\.html"))]
        
        # iterate the subregions
        print("Downloading...")
        for subregion in subregions:
            
            # we add no subregion paths by default
            add_subregion_path = False
            
            # get the page for the subregion
            soup = BeautifulSoup(requests.get(subregion).content, "lxml")
            
            # check if there are no subsubregions
            if (len(soup.find_all("p", string = re.compile("No sub regions are defined for this region."))) > 0):
                add_subregion_path = True
                # add the entire subregion to the download query
                dl_links = [soup.find("a", href = re.compile(".*latest\.osm\.pbf$"))["href"]]
                
            else:
                # add all subsubregions to the download query
                dl_links = [subsubregion["href"] for subsubregion in soup.find_all("a", href = re.compile(".*/.*\.osm\.pbf$"))]
            
            # create the directory for the subsubregion
            makedirs(f"{self.storage_directory}/{re.search(r'^.*(?=/)|^.*(?=-latest)', dl_links[0]).group(0)}", exist_ok = True)
            
            # iterate over download links
            for dl_link in dl_links:
                # download the file
                if add_subregion_path:
                    urlretrieve(f"https://download.geofabrik.de/europe/germany/{dl_link}",
                                f"{storage_directory}/{re.search(r'^.*(?=/)|^.*(?=-latest)', dl_link).group(0)}/{dl_link}")
                else:
                    urlretrieve(f"https://download.geofabrik.de/europe/germany/{dl_link}",
                                f"{storage_directory}/{dl_link}")
            
            # add the subregion, subsubregions, path and link to the lookup table
            lookup_table = concat([lookup_table,
                                   DataFrame([{"subregion": re.search(r"^.*(?=/)|^.*(?=-latest)", dl_link).group(0),
                                                  "subsubregion": re.search(r"(?<=/)*.*(?=-regbez)*(?=-latest)", dl_link).group(0),
                                                  "path": f"{self.storage_directory}/{re.search(r'^.*(?=/)|^.*(?=-latest)', dl_link).group(0)}/{dl_link}",
                                                  "link": f"https://download.geofabrik.de/europe/germany/{dl_link}"} for dl_link in dl_links])])
            
            # store the lookup table
            lookup_table.to_csv(f"{self.storage_directory}/lookup.csv")