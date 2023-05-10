import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("Stage")


class Stage(ABC):
    def __init__(self, *args, **kwargs) -> None:
        super(Stage, self).__init__()

    def activate(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def dump(self):
        raise NotImplementedError()

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


@dataclass
class UserInput:
    text: str
    date: datetime = datetime.now()

    def __str__(self):
        return f"[{self.date.strftime('%Y-%m-%d %H:%M:%S')}]:::{self.text}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other
        elif isinstance(other, UserInput):
            return self.text == other.text and self.date == other.date
        else:
            raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        return {"text": self.text, "date": self.date.strftime('%Y-%m-%d %H:%M:%S')}
