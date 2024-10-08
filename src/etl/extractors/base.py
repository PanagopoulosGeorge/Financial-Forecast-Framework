from abc import ABC, abstractmethod

class Extractor(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def extract_publications(self):
        pass
    
