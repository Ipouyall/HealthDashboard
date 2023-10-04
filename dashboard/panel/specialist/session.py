import random
import time
from typing import Union

import streamlit as st
from streamlit_echarts import st_echarts, JsCode

from dashboard.storage.role import Role
from dashboard.storage.storage import StageStorage
from dashboard.storage.conversation import Conversation, Message
from dashboard.storage.report import Report, VALID_REPORTS, ReportType
from dashboard.storage.report import Report, ReportType
from dashboard.model.mood import MoodModel
from dashboard.plots.gauge import emotion_gauge
from dashboard.plots.anotate import show_annotated


class Therapy:
    SPECIAL_COMMANDS = ["analyze"]

    def __init__(self):
        self.storage = StageStorage()
        self.conversations = [None, ] + self.storage.get_conversations()
        self.conversation: Union[Conversation, None] = None
        self.mood = MoodModel("./dashboard/model/depecheMood/DepecheMood_english_token_full.tsv")

    def special(self, command):
        pass

    def analytics(self, active_tools):
        row1 = st.columns(2)
        row1_idx = 0
        if "Emotion Gauge" in active_tools:
            emotion_gauge(
                text=' '.join(msg.content for msg in self.conversation.messages if msg.role == Role.User),
                model=self.mood,
                ph=row1[row1_idx],
            )
            row1_idx += 1

        # TODO: Implement emotion changing

    def menu(self):
        if self.conversation is None:
            return

        st.sidebar.markdown("### Analyzers")

        active_reports = st.sidebar.multiselect(
            "Select analyzers",
            VALID_REPORTS.keys(),
        )

        # TODO: show chan and annotation if needed

        self.analytics(active_reports)

        # TODO: add a section for control the annotation threshold

        # TODO: if session not ended, we need a section to end it

    def activate(self):
        conv = st.sidebar.selectbox('Your Sessions', self.conversations)
        if conv is not None and (self.conversation is None or self.conversation.id != conv[0]):
            self.conversation = self.storage.get_conversation(id=conv[0])
        elif conv is None:
            self.conversation = None
            st.markdown("Please select a conversation to activate!")
            return

        st.header(f"{self.conversation.title}")

        self.menu()





