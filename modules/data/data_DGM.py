from modules.data.data_abstract import data_abstract
import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd

class data_DGM(data_abstract):
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/DGM"):
        self.storage_directory = storage_directory
    
    def query(self, spatial_bounds = "available", temporal_bounds = "available", crs = 25833):
        
        print("Getting files...")
        # get the page of links
        page = requests.get("https://data.geobasis-bb.de/geobasis/daten/dgm/xyz/")
        # turn into queryable soup
        soup = BeautifulSoup(page.content)
        # extract links
        links = [elem["href"] for elem in soup.find_all("a", href = True, string = re.compile("dgm.*zip"))]
        # get raw file names
        filenames = [re.search(re.compile(".*(?=\.zip)"), link).group(0) for link in links]
        
        print("Downloading...")
        for link in links:
            if not os.path.isfile(self.storage_directory + "/raw/" + link):
                urlretrieve("https://data.geobasis-bb.de/geobasis/daten/dgm/xyz/" + link,
                            self.storage_directory + "/raw/" + link)

        print("Extracting...")
        for index, link in enumerate(links):
            if not os.path.isfile(self.storage_directory + "/raw/" + filenames[index] + ".xyz"):
                try:
                    with ZipFile(self.storage_directory + "/raw/" + link, "r") as zip_ref:
                        zip_ref.extractall(self.storage_directory + "/raw")
                except:
                    pass
            
        print("Getting lookup table...")
        # a function to extract the extent from the xml
        def worker(file):
            out = pd.read_xml(file, xpath = "//Extent/sw|//Extent/se|//Extent/nw|//Extent/ne")
            out["id"] = file
            out["pos"] = ["sw", "se", "nw", "ne"]
            return out
        pd.concat([worker(file) for file in [self.storage_directory + "/raw/" + name + ".xml" for name in filenames]]).to_csv(self.storage_directory + "/lookup_table.csv")
        
        print("--- Download complete ---")