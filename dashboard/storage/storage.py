from dashboard.storage.role import *
from dashboard.storage.conversation import *


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StageStorage(metaclass=Singleton):  # TODO: connect to a database
    def __init__(self):
        self.conversations = [
            Conversation(
                id=0,
                title="Conversation 1",
                messages=[
                    Message(
                        id=0,
                        role=Role.User,
                        content="Hi!"),
                    Message(
                        id=1,
                        role=Role.Specialist,
                        content="Hello!"),
                    Message(
                        id=2,
                        role=Role.User,
                        content="I am so depressed such as I want to die!"),
                    ],
                ),
            Conversation(
                id=1,
                title="Conversation 2",
                messages=[
                    Message(
                        id=0,
                        role=Role.User,
                        content="Such a lovely day!"),
                    Message(
                        id=1,
                        role=Role.User,
                        content="I am so happy!"),
                    Message(
                        id=2,
                        role=Role.Specialist,
                        content="sound good!"),
                    ],
            ),
        ]

    def get_conversations(self):
        convs = []
        for conv in self.conversations:
            convs.append((conv.id, conv.title))
        return convs

    def get_conversation(self, title=None, id=None):
        for conv in self.conversations:
            if id is not None:
                if conv.id == id:
                    return conv
            elif conv.title is not None and conv.title == title:
                return conv


