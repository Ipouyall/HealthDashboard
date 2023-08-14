from itertools import count
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod


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


# class UserInput:
#     TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
#     COUNT = count()
#
#     def __init__(self, text: str, date=None, id=None, **kwargs):
#         self.text: str = text
#         if date is None:
#             self.date: datetime = datetime.now()
#         elif isinstance(date, datetime):
#             self.date: datetime = date
#         elif isinstance(date, str):
#             tf = self.TIME_FORMAT
#             if '.' in date:
#                 tf = self.TIME_FORMAT + ".%f"
#             self.date: datetime = datetime.strptime(date, tf)
#         else:
#             raise Exception("Unknown date format")
#         if id is None:
#             self.id = next(self.COUNT)
#         else:
#             next(self.COUNT)
#             self.id = id
#
#     def __str__(self):
#         return f"[{self.date.strftime(self.TIME_FORMAT)}]:::[{self.text}]"
#
#     def __eq__(self, other):
#         if isinstance(other, str):
#             return self.text == other
#         elif isinstance(other, UserInput):
#             return self.text == other.text and self.date == other.date
#         else:
#             raise NotImplementedError()
#
#     def __call__(self, *args, **kwargs):
#         return {
#             "id": self.id,
#             "text": self.text,
#             "date": self.date.strftime(self.TIME_FORMAT)
#         }
#
#
# @dataclass
# class Report:
#     overall_status: str
#     score:          float
#     text_id:        str
#     id:             int = field(default_factory=count().__next__, init=True)
#
#     def __str__(self):
#         return f"[status {self.overall_status}]:::[score {self.score:.3f}]"
#
#     def __call__(self, *args, **kwargs):
#         return {
#             "id": self.id,
#             "overall_status": self.overall_status,
#             "score": self.score,
#             "text_id": self.text_id
#         }
