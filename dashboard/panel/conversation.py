import random
import time

import streamlit as st

from dashboard.storage.role import Role
from dashboard.storage.storage import StageStorage
from dashboard.storage.conversation import Conversation, Message


class Conversation:
    MAX_DELAY = 0.1

    def __init__(self):
        self.storage = StageStorage()
        self.conversations = [None, ] + self.storage.get_conversations()
        self.conversation = None

    def analyze(self): pass

    def chat_page(self):
        if prompt := st.chat_input("How you feel today?"):
            with st.chat_message("user"):
                st.markdown(prompt)
            # Add user message to chat history
            msg = Message(
                id=len(self.conversation.messages),
                role=Role.User,
                content=prompt
            )
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

    def activate(self):
        conv = st.sidebar.selectbox('Active Conversation/Session', self.conversations)
        if conv is not None and (self.conversation is None or self.conversation.id != conv[0]):
            self.conversation = self.storage.get_conversation(id=conv[0])
        elif conv is None:
            self.conversation = None
            st.markdown("Please select a conversation to activate!")
            return

        st.header(f"{self.conversation.title}")

        self.chat_page()

