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


annotation_sensitivity = {
    "Off": None,
    "Low": 0.5,
    "Medium": 0.35,
    "High": 0.2,
}


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

    def show_chat(self, annotate_threshold=0.3):
        """If annotate_threshold is None, then no annotation will be shown"""
        if self.conversation is None:
            return

        command = ''
        if prompt := st.chat_input("Type for conversation..."):
            msg = Message(
                id=len(self.conversation.messages),
                role=Role.Specialist,
                content=prompt
            )

            if prompt.lower() in self.SPECIAL_COMMANDS:
                command = prompt.lower()
            else:
                self.conversation.messages.append(msg)

        for idx in range(len(self.conversation.messages)):
            msg = self.conversation.messages[idx]()
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])

        # if command:
        #     with st.chat_message('assistant'):
        #         self.special(command)

    def menu(self):
        if self.conversation is None:
            return

        st.sidebar.markdown("### Tools")

        active_reports = st.sidebar.multiselect(
            "Select analyzers",
            VALID_REPORTS.keys(),
        )

        ann_ses = st.sidebar.select_slider(
            "Annotation Sensitivity",
            list(annotation_sensitivity.keys()),
        )

        self.show_chat(annotate_threshold=annotation_sensitivity[ann_ses])
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
        st.sidebar.divider()

        st.header(f"{self.conversation.title}")

        self.menu()





