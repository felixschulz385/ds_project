from modules.data.data_abstract import data_abstract
from urllib.request import urlretrieve
from zipfile import ZipFile
from os import system

class data_cartography(data_abstract):
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/orthography"):
        self.storage_directory = storage_directory
    
    def query(self, spatial_bounds = "available", temporal_bounds = "available", crs = 25833):
        
        print("Downloading...")
        urlretrieve("https://daten.gdz.bkg.bund.de/produkte/dlm/dlm250/aktuell/dlm250.utm32s.nas_bda.kompakt.zip",
            self.storage_directory + "/raw/dlm250.utm32s.nas_bda.kompakt.zip")
        
        print("Extracting...")
        with ZipFile(self.storage_directory + "/raw/dlm250.utm32s.nas_bda.kompakt.zip", "r") as zip_ref:
            zip_ref.extractall(self.storage_directory + "/raw")
            
        print("Reorganizing...")
        # filtering for some selected files
        filter_files = [f"mv {self.storage_directory}/raw/dlm250.utm32s.nas_bda.kompakt/dlm250_kompakt/BDA_{x}.xml " +
                        f"{self.storage_directory}/raw/BDA_{x}.xml" 
                        for x in [43001, 43002, 43004, 41010, 53002, 53007, 71006, 71007, 71011, 75009]]
        for command in filter_files:
            system(command)
        # removing zip and unzipped folder
        system("rm " + self.storage_directory + "/raw/dlm250.utm32s.nas_bda.kompakt.zip")
        system("rm -rf " + self.storage_directory + "/raw/dlm250.utm32s.nas_bda.kompakt")
        
        print("--- Download complete ---")