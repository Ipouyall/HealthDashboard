from abc import ABC, abstractmethod
from dataclasses import dataclass


class BaseModel(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        raise NotImplementedError()
