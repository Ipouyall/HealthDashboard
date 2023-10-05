from dashboard.storage.conversation import *
from dashboard.storage.report import *


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
                id=1,
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
                id=2,
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
                        content="Sounds good!"),
                    Message(
                        id=3,
                        role=Role.User,
                        content="But you know, I've been feeling a bit overwhelmed lately."),
                    Message(
                        id=4,
                        role=Role.Specialist,
                        content="I'm here to listen. What's been bothering you?"),
                    Message(
                        id=5,
                        role=Role.User,
                        content="Well, work has been really stressful, and I've been having trouble sleeping."),
                    Message(
                        id=6,
                        role=Role.Specialist,
                        content="I'm sorry to hear that. Stress can take a toll on your mental and physical health. Have you tried any relaxation techniques?"),
                    Message(
                        id=7,
                        role=Role.User,
                        content="I've tried deep breathing exercises, but they only help temporarily."),
                    Message(
                        id=8,
                        role=Role.Specialist,
                        content="Deep breathing is a good start. We can explore more coping strategies to manage stress. Would you like some suggestions?"),
                    Message(
                        id=9,
                        role=Role.User,
                        content="Yes, please! I'm open to any suggestions that can help me relax."),
                    Message(
                        id=10,
                        role=Role.Specialist,
                        content="Great! Let's start with progressive muscle relaxation. It's a technique where you tense and then relax different muscle groups to reduce physical tension. Would you like me to guide you through it?"),
                    Message(
                        id=11,
                        role=Role.User,
                        content="Sure, I'll give it a try."),
                    Message(
                        id=12,
                        role=Role.Specialist,
                        content="Excellent. Let's start with your toes. Tense them for a few seconds, then release. Now, move to your calf muscles. Tense and release. Continue up through your body, focusing on each muscle group. Take your time."),
                    Message(
                        id=13,
                        role=Role.User,
                        content="That actually helped me relax a bit. Thanks for the suggestion!"),
                    Message(
                        id=14,
                        role=Role.Specialist,
                        content="You're welcome! Remember, managing stress is an ongoing process, and there are many techniques to explore. If you ever need more advice or just want to talk, I'm here for you."),
                    Message(
                        id=15,
                        role=Role.User,
                        content="I appreciate that. Lately, I've also been feeling anxious about social situations."),
                    Message(
                        id=16,
                        role=Role.Specialist,
                        content="Social anxiety is common. One approach is exposure therapy, where you gradually face feared situations. Would you like to discuss this further?"),
                    Message(
                        id=17,
                        role=Role.User,
                        content="Yes, I think exposure therapy might help. Can you explain how it works?"),
                    Message(
                        id=18,
                        role=Role.Specialist,
                        content="Certainly! Exposure therapy involves facing social situations that make you anxious in a controlled and gradual manner. The goal is to desensitize your anxiety response over time. We can create a plan tailored to your specific triggers and comfort level."),
                    Message(
                        id=19,
                        role=Role.User,
                        content="That sounds promising. Let's work on a plan together."),
                    Message(
                        id=20,
                        role=Role.Specialist,
                        content="Great! We'll start with small, manageable steps. Overcoming social anxiety is a journey, and I'll be here to support you every step of the way."),
                    Message(
                        id=21,
                        role=Role.User,
                        content="Thank you for your support. I really appreciate it."),
                    Message(
                        id=22,
                        role=Role.Specialist,
                        content="You're welcome! Remember, progress takes time, so be patient with yourself. Whenever you're ready to start, we can begin creating your exposure plan."),
                    # 1 more message to reach a total of 23
                    Message(
                        id=23,
                        role=Role.User,
                        content="I'm feeling more hopeful already. Let's start working on that plan!")
                ],
                report=Report(
                    activeCharts=[ReportType.emoGauge, ReportType.sessionSentimentChanging],
                    specialistsNote="This is a sample note from the specialist",
                ),
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
                id = int(id)
                if conv.id == id:
                    return conv
            elif conv.title is not None and conv.title == title:
                return conv
