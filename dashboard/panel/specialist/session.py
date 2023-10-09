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
from dashboard.plots.wordcloud import WordCould
from dashboard.plots.anotate import show_annotated


annotation_sensitivity = {
    "Off": None,
    "Low": 0.7,
    "Medium": 0.5,
    "High": 0.35,
    "Extreme": 0.25,
}


class Therapy:
    SPECIAL_COMMANDS = ["analyze"]

    def __init__(self):
        self.storage = StageStorage()
        self.conversations = [None, ] + ['. '.join([str(conv[0]), conv[1]]) for conv in self.storage.get_conversations()]
        self.conversation: Union[Conversation, None] = None
        self.mood = MoodModel("./dashboard/model/depecheMood/DepecheMood_english_token_full.tsv")
        self.need_sync = False

    def special(self, command):
        pass

    def analytics(self, active_tools):
        row1 = st.columns(2)
        row1_idx = 0
        for tool in active_tools:
            if "Emotion Gauge" == tool:
                emotion_gauge(
                    text=' '.join(msg.content for msg in self.conversation.messages if msg.role == Role.User),
                    model=self.mood,
                    ph=row1[row1_idx],
                )
                row1_idx += 1

            elif "Word Cloud" == tool:
                WordCould(
                    text=". ".join(msg.content for msg in self.conversation.messages if msg.role == Role.User),
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
                self.need_sync = True

        for idx in range(len(self.conversation.messages)):
            msg = self.conversation.messages[idx]()
            with st.chat_message(msg['role']):
                if msg['role'].lower() == 'user' and annotate_threshold is not None:
                    show_annotated(
                        text=msg['content'],
                        threshold=annotate_threshold,
                    )
                else:
                    st.markdown(msg['content'])

        # if command:
        #     with st.chat_message('assistant'):
        #         self.special(command)

    def menu(self):
        if self.conversation is None:
            return

        st.sidebar.markdown("### Tools")

        active_reports = st.sidebar.multiselect(
            "Select tools",
            VALID_REPORTS.keys(),
        )

        ann_ses = st.sidebar.select_slider(
            "Annotation Sensitivity",
            list(annotation_sensitivity.keys()),
        )

        self.show_chat(annotate_threshold=annotation_sensitivity[ann_ses])

        self.analytics(active_reports)

        ###### Report section ######
        if self.conversation.report is not None:
            return

        st.sidebar.divider()
        st.sidebar.markdown("### Report")

        useful_reports = st.sidebar.multiselect(
            "Select analyzers for report",
            list(VALID_REPORTS.keys()) + ["Notes"],
        )

        ph = st.sidebar.empty()
        end_session = ph.button("End Session")
        notes = ""
        if 'Notes' in useful_reports:
            st.text_area("Specialist's notes:")
        if end_session:

            # submit_end = ph.button("Submit note")

            if True:
                st.success("Report submitted and session ended successfully!")

                self.conversation.report = Report(
                    activeCharts=[VALID_REPORTS[chart] for chart in useful_reports],
                    specialistsNote=notes,
                )

                self.need_sync = True

    def activate(self):
        conv = st.sidebar.selectbox('Your Sessions', self.conversations)
        if conv is not None and (self.conversation is None or self.conversation.id != conv[0]):
            conv_id = int(conv[:conv.find('. ')])
            self.conversation = self.storage.get_conversation(id=conv_id)
        elif conv is None:
            self.conversation = None
            st.markdown("Please select a conversation to activate!")
            return
        st.sidebar.divider()

        st.header(f"{self.conversation.title}")

        self.menu()

        if self.need_sync and self.conversation is not None:
            self.storage.update_conversation(self.conversation)
            self.need_sync = False
            st.experimental_rerun()



