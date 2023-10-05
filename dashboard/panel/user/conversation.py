import random
import time
from typing import Union

import streamlit as st
from streamlit_echarts import st_echarts, JsCode

from dashboard.storage.role import Role
from dashboard.storage.storage import StageStorage
from dashboard.storage.conversation import Conversation, Message
from dashboard.storage.report import Report, ReportType
from dashboard.model.mood import MoodModel
from dashboard.plots.gauge import emotion_gauge


class Session:
    MAX_DELAY = 0.1
    SPECIAL_COMMANDS = ["emotion"]

    def __init__(self):
        self.storage = StageStorage()
        self.conversations = [None, ] + ['. '.join([str(conv[0]), conv[1]]) for conv in self.storage.get_conversations()]
        self.conversation: Union[Conversation, None] = None
        self.mood = MoodModel("./dashboard/model/depecheMood/DepecheMood_english_token_full.tsv")

    def special(self, command):
        if command == 'emotion':
            prompt = '. '.join([p.content for p in self.conversation.messages if p.role == Role.User])
            emo = self.mood.predict(prompt)
            option = {
                "series": [
                    {
                        "type": "gauge",
                        "startAngle": 90,
                        "endAngle": -270,
                        "pointer": {"show": False},
                        "progress": {
                            "show": True,
                            "overlap": False,
                            "roundCap": True,
                            "clip": False,
                            "itemStyle": {"borderWidth": 1, "borderColor": "#464646"},
                        },
                        "axisLine": {"lineStyle": {"width": 40}},
                        "splitLine": {"show": False, "distance": 0, "length": 10},
                        "axisTick": {"show": False},
                        "axisLabel": {"show": False, "distance": 50},
                        "data": [
                            {
                                "value": round(emo.happy, 2),
                                "name": "Happiness",
                                "title": {"offsetCenter": ["0%", "-50%"]},
                                "detail": {"offsetCenter": ["0%", "-40%"]},
                            },
                            {
                                "value": round(emo.angry, 2),
                                "name": "Anger",
                                "title": {"offsetCenter": ["0%", "-20%"]},
                                "detail": {"offsetCenter": ["0%", "-10%"]},
                            },
                            {
                                "value": round(emo.sad, 2),
                                "name": "Sadness",
                                "title": {"offsetCenter": ["0%", "10%"]},
                                "detail": {"offsetCenter": ["0%", "20%"]},
                            },
                            {
                                "value": round(emo.afraid, 2),
                                "name": "Frightened",
                                "title": {"offsetCenter": ["0%", "40%"]},
                                "detail": {"offsetCenter": ["0%", "50%"]},
                            },
                        ],
                        "title": {"fontSize": 14},
                        "detail": {
                            "width": 50,
                            "height": 14,
                            "fontSize": 14,
                            "color": "auto",
                            "borderColor": "auto",
                            "borderRadius": 20,
                            "borderWidth": 1,
                            "formatter": "{value}%",
                        },
                    }
                ]
            }

            st_echarts(option, height="500px", key="echarts")

    def analytics(self):
        if self.conversation is None:
            return
        if self.conversation.report is None:
            return

        report = self.conversation.report

        row = st.columns(2 if len(report.activeCharts) > 1 else 1)
        idx = 0
        if ReportType.emoGauge in report.activeCharts:
            emotion_gauge(
                text=' '.join(msg.content for msg in self.conversation.messages if msg.role == Role.User),
                model=self.mood,
                ph=row[idx],
            )

        ### Place holder for seccond chart ###

        if report.specialistsNote:
            st.markdown("# Specialist's Note")

            specialists_note = report.specialistsNote
            st.markdown(specialists_note)

    def chat_page(self):
        command = ''
        if self.conversation is None or self.conversation.report is not None:
            pass
        elif prompt := st.chat_input("How you feel today?"):
            # Add user message to chat history
            msg = Message(
                id=len(self.conversation.messages),
                role=Role.User,
                content=prompt
            )

            if prompt.lower() in self.SPECIAL_COMMANDS:
                command = prompt.lower()
            else:
                self.conversation.messages.append(msg)

        # Display chat messages from history on app rerun
        for idx in range(len(self.conversation.messages)):
            msg = self.conversation.messages[idx]()
            with st.chat_message(msg['role']):
                message_placeholder = st.empty()
                if not msg['shown']:
                    full_response = ""
                    for chunk in msg['content'].split():
                        full_response += chunk + " "
                        delay = random.random() * self.MAX_DELAY
                        time.sleep(delay)
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(msg['content'])

        if command:
            with st.chat_message('assistant'):
                self.special(command)

        if self.conversation.report is not None:
            self.analytics()

    def activate(self):
        conv = st.sidebar.selectbox('Active Session', self.conversations)
        if conv is not None and (self.conversation is None or self.conversation.id != conv[0]):
            conv_id = int(conv[:conv.find('. ')])
            self.conversation = self.storage.get_conversation(id=conv_id)
        elif conv is None:
            self.conversation = None
            st.markdown("Please select a conversation to activate!")
            return

        st.header(f"{self.conversation.title}")

        self.chat_page()
