"""
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from modules.preprocessing.preprocessing_cartography import preprocessing_cartography

# Run a preprocess for a single item
def test_preprocess():
    cartography_downloader = preprocessing_cartography()
    cartography_downloader.preprocess()
    
if __name__ == "__main__":
    test_preprocess()
    print("Everything passed")
    print("Test")