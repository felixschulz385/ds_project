from abc import ABC, abstractmethod

# abstract class for data APIs
class analysis_abstract(ABC):

    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def analyze():
        pass