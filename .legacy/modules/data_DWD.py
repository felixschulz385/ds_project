# imports 
import requests
from bs4 import BeautifulSoup
import re
import os 


# define base url 
wind_data_url = "https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/"


def get_links(): 
    """Get all links which contain data on wind from base url."""
    
    # create response object 
    r = requests.get(wind_data_url)
    
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content,'html.parser') 
    
    # find all links on web-page 
    links = soup.findAll('a')
    
    # specify data to consider 
    matches = ["wind", "pressure", "cloud"]
    parent_links = []   # initialize empty list 

    # loop over links and create list with links to download from 
    for link in links: 
        if any(x in link['href'] for x in matches):
            if "vapor" in link['href']:
                pass 
            else:
                parent_links.append(wind_data_url + link['href'])
     
    return parent_links 


def download_files(parent_links): 
    """Download files from links with wind data."""
    
    # initialize empty dictionary 
    download_links = {}

    # loop over directories which contain wind data 
    for parent_link in parent_links: 
        
        directory_name = parent_link.split('/')[-2] 
        
        #create response object
        r = requests.get(parent_link)

        # create beautiful-soup object 
        soup = BeautifulSoup(r.content,'html.parser')

        # find all links on web-pag
        links = soup.findAll('a')
        
        # dictionary with download links as values and directory name as key 
        download_links[directory_name] = [parent_link + link['href'] for link in links if link['href'].endswith('.nc.gz')]
        
    # outer loop: wind links, i.e. wind speed and wind direction  
    for key in download_links: 
        # specify directory to store data to 
        directory = os.path.join('/pfs/work7/workspace/scratch/tu_zxobe27-ds_project/data', key)
        
        try:
            # try to make directory if it does not exist
            os.mkdir(directory)
            print(f"{directory} created.")
        except:
            print(f"{directory} already exists.")
            pass
        
        # inner loop: file links within wind links
        for link in download_links[key]:
            # obtain filename by splitting url and getting 
            # last string 
            file_name = link.split('/')[-1]
            
            file_name.split('.')[0:-1]
            
            # check whether file exists in path. If false -> download file to path
            if not os.path.exists(os.path.join(directory, file_name)): 
                # create response object 
                r = requests.get(link, stream = True) 
                
                # start download  
                with open(os.path.join(directory, file_name), 'wb') as f: 
                    for chunk in r.iter_content(chunk_size = 1024*1024): 
                        if chunk: 
                            f.write(chunk) 
                
                print( f"{file_name} downloaded.")
                
                
            
            # if file exists pass 
            else:
                pass

    print ("All files downloaded.")
    

if __name__ == "__main__": 
  
    # getting all video links 
    parent_links = get_links()
    
    # download data and store files 
    download_files(parent_links=parent_links)
