from abc import ABC, abstractmethod

# abstract class for data APIs
class data_abstract(ABC):

    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def query(self, spatial_bounds, temporal_bounds, crs):
        pass
    