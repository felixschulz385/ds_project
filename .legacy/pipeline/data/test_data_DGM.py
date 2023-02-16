import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from modules.data.data_DGM import data_DGM

# Run a query for a single item
def test_query():
    DGM_downloader = data_DGM()
    DGM_downloader.query()
    
if __name__ == "__main__":
    test_query()
    print("Everything passed")
    
# sbatch --job-name="download.job" --output="download.out" --export=ALL --partition=single --ntasks=1 --cpus-per-task=1 --mem-per-cpu=8000 --time=480 download.sbatch