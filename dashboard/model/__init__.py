from abc import ABC, abstractmethod
from dataclasses import dataclass


class BaseModel(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        raise NotImplementedError()


@dataclass
class Report:
    overall_status: str
    score:          float

    def __str__(self):
        return f"status:{self.overall_status}:::score:{self.score:.3f}"

    def __call__(self, *args, **kwargs):
        return {"overall_status": self.overall_status, "score": self.score}
