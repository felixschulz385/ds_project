from abc import ABC, abstractmethod

# abstract class for data APIs
class preprocessing_abstract(ABC):

    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def preprocess():
        pass