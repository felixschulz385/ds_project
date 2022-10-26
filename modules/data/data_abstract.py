from abc import ABC, abstractmethod

# abstract class for data APIs
class data_abstract(ABC):

    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def push_query(self, spatial_bounds, temporal_bounds, crs):
        pass
    
    @abstractmethod
    def run_query(self):
        pass
    
    @abstractmethod
    def export_query(self):
        pass