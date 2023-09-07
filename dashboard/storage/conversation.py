import datetime
from dashboard.storage.role import Role
from dataclasses import dataclass

from typing import Union


@dataclass()
class Message:
    id: int
    role: Role
    content: str
    date: Union[datetime.date, None] = None
    shown: bool = False
    analyzed: bool = False

    def __post_init__(self):
        if self.date is None:
            self.date = datetime.datetime.now()

        if self.role == Role.User:
            self.shown = True
        elif self.role == Role.Analytic:
            self.analyzed = True

    def __call__(self, option: str = 'show'):
        shown, analyzed = self.shown, self.analyzed
        if option == 'show':
            self.shown = True
        elif option == 'analyze':
            self.analyzed = True
        return {
            "role": self.role.name,
            "content": self.content,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "shown": shown,
            "analyzed": analyzed
        }


@dataclass()
class Conversation:
    id: int
    title: str
    messages: list[Message]
    ended: bool = False
    analytic_note: str = ""


