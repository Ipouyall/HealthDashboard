import enum
from typing import Union, List, Iterable

from dashboard.types import *


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ObjectType(enum.Enum):
    userInput = enum.auto()
    report = enum.auto()


class StageStorage(metaclass=Singleton):
    def __init__(self):
        self.userInputs: list[UserInput] = []
        self.newUserInputIndex = 0
        self.sessionUserInputIndex = 0

        self.reports: list[Report] = []
        self.newReportIndex = 0
        self.sessionReportIndex = 0

    def restore(self, entities: list[Union[UserInput, Report]]):
        if not entities:
            return

        if isinstance(entities[0], UserInput):
            self.userInputs = entities.copy()
            self.sessionUserInputIndex = len(self.userInputs)
        elif isinstance(entities[0], Report):
            self.reports = entities.copy()
            self.sessionReportIndex = len(self.reports)
        else:
            raise Exception("Unknown type")

    def add_record(self, record: Union[UserInput, Report]):
        if isinstance(record, UserInput):
            if record not in self.userInputs:
                self.userInputs.append(record)
        elif isinstance(record, Report):
            if record not in self.reports:
                self.reports.append(record)
        else:
            raise Exception("Unknown type")

    def __get_dataset(self, ot: ObjectType, session_split=False, new_split=False) -> List[Union[UserInput, Report]]:
        if ot == ObjectType.userInput:
            if session_split:
                dataset = self.userInputs[self.sessionUserInputIndex:]
            elif new_split:
                dataset = self.userInputs[self.newUserInputIndex:]
                self.newUserInputIndex = len(self.userInputs)
            else:
                dataset = self.userInputs
        elif ot == ObjectType.report:
            if session_split:
                dataset = self.reports[self.sessionReportIndex:]
            elif new_split:
                dataset = self.reports[self.newReportIndex:]
                self.newReportIndex = len(self.reports)
            else:
                dataset = self.reports
        else:
            raise Exception("Unknown object type")

        return dataset

    def get_preview(self, ot: ObjectType):
        dataset: List[Union[UserInput, Report]] = self.__get_dataset(ot)

        for entity in dataset:
            text = str(entity)
            text = f"{text if len(text) < 60 else text[:60] + '...'}"
            yield text

    def entity_exists(self, entity: Union[UserInput, Report]):
        if isinstance(entity, (UserInput, str)):
            return entity in self.userInputs
        elif isinstance(entity, Report):
            return entity in self.reports
        else:
            raise Exception("Unknown type")

    def get_session_data(self, ot: ObjectType) -> Iterable[Union[UserInput, Report]]:
        dataset = self.__get_dataset(ot, session_split=True)

        for entity in dataset:
            yield entity

    def get_new_data(self, ot: ObjectType) -> Iterable[Union[UserInput, Report]]:
        dataset = self.__get_dataset(ot, new_split=True)

        for entity in dataset:
            yield entity

    def get_data(self, ot: ObjectType) -> Iterable[Union[UserInput, Report]]:
        dataset = self.__get_dataset(ot)

        for entity in dataset:
            yield entity


