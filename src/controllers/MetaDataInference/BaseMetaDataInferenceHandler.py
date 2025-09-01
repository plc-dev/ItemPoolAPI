from abc import ABC, abstractmethod
from typing import Any

class MetaDataInferenceHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def infer_metadata(self, obj: Any):
        return