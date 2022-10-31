import requests
from bs4 import BeautifulSoup
import re
import os 


class DownloadWind:
    def __init__(self, base_url="https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/"):
        self.base_url = base_url
        
    def get_links(self, base_url): 
        """Get all links which contain data on wind from base url."""
    
        # create response object 
        r = requests.get(base_url)
        
        # create beautiful-soup object 
        soup = BeautifulSoup(r.content,'html.parser') 
        
        # find all links on web-page 
        links = soup.findAll('a') 
        
        # find all links from web-page where wind data is contained 
        self.wind_links = [wind_data_url + link['href'] for link in links if bool(re.search("wind", link['href']))]  
        
    
    def download_files(self, wind_links): 
        """Download files from links with wind data."""
        
        # initialize empty dictionary 
        download_links = {}

        # loop over directories which contain wind data 
        for wind_link in wind_links: 
            
            directory_name = wind_link.split('/')[-2] 
            
            #create response object
            r = requests.get(wind_link)

            # create beautiful-soup object 
            soup = BeautifulSoup(r.content,'html.parser')

            # find all links on web-pag
            links = soup.findAll('a')
            
            # dictionary with download links as values and directory name as key 
            download_links[directory_name] = [wind_link + link['href'] for link in links if link['href'].endswith('.nc.gz')]
            
        # outer loop: wind links, i.e. wind speed and wind direction  
        for key in download_links: 
            # specify directory to store data to 
            directory = os.path.join('/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data', key)
            
            try:
                # try to make directory if it does not exist
                os.mkdir(directory)
            except:
                pass
            
            # inner loop: file links within wind links
            for link in download_links[key]:
                # obtain filename by splitting url and getting 
                # last string 
                file_name = link.split('/')[-1] 
                
                # check whether file exists in path. If false -> download file to path
                if not os.path.exists(os.path.join(directory, file_name)): 
                    # create response object 
                    r = requests.get(link, stream = True) 
                    
                    # start download  
                    with open(os.path.join(directory, file_name), 'wb') as f: 
                        for chunk in r.iter_content(chunk_size = 1024*1024): 
                            if chunk: 
                                f.write(chunk) 
                    
                    print( f"{file_name} downloaded.", end='\r')
                
                # if file exists pass 
                else:
                    pass
        
        print ("All files downloaded")
        
        
if __name__ == "__main__": 
    DownloadWind()

