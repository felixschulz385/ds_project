"""
MaStR data download & output to json
"""

from modules.data.data_abstract import data_abstract
import pandas as pd
from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
import requests
import re
from datetime import date
import json
import xmltodict
import xml.etree.ElementTree as ET

class data_MaStR(data_abstract):
    
    def __init__(self,
                 storage_directory = "/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data/mastr/"):
        self.storage_directory = storage_directory
    
    def query(self, spatial_bounds = "available", temporal_bounds = "available", crs = 25833):
        
        # get current URL
        URL = "https://ds.marktstammdatenregister.dev/Marktstammdatenregister"
        page = requests.get(self.URL)
        soup = BeautifulSoup(self.page.content, "html.parser")
        DataLink = self.soup.findAll('a', href = re.compile('^https://download.marktstammdatenregister.de/Gesamtdatenexport_'))[0]['href']
        
        # !!! Download takes ~15 minutes !!!
        
        print("Downloading...")
        # download file 
        req = requests.get(self.DataLink)
        # set filename
        datum = date.today()
        filename = f'MaStR_Gesamtdatenexport_{self.datum}.zip'
        # writing file to system
        with open(self.filename, 'wb') as output_file:
            self.output_file.write(req.content)        
        print("--- Download complete ---")
        
        # unzip folder and extract required data
        print("Start unzip...")
        Matches = []
        with ZipFile(self.storage_directory + self.filename, 'r') as ZipObject:
            for names in self.ZipObject.namelist():
                PVA = re.findall(r'^EinheitenSolar.*xml$', self.names)
                self.Matches.append(self.PVA)
                WKA = re.findall(r'^EinheitenWind.*xml$', self.names)
                self.Matches.append(self.WKA)
            while [] in self.Matches :
                self.Matches.remove([])
            self.Matches = [str(M) for M in self.Matches]
            for i in range(len(self.Matches)-1):
                Source_Name = self.Matches[i][2:-2]
                self.ZipObject.extract(
                    self.Source_Name, path = self.storage_directory
                )
        print("--- unzip complete ---")

        print("converting to json...")
        for i in range(len(self.Matches)-1):
            Source_Name = self.Matches[i][2:-2]
            Unit = self.storage_directory + Source_Name

        # transform into python dictionary        
        tree = ET.parse(self.WKA)
        xml_data = self.tree.getroot()
        xmlstr = ET.tostring(self.xml_data, encoding='latin-1', method='xml')

        data_dict = dict(xmltodict.parse(self.xmlstr))

        # transform into json
        json_data = json.dumps(self.data_dict)
        with open("WKA.json", "w") as json_file:
            self.json_file.write(self.json_data)