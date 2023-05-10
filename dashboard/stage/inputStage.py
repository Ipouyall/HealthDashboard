import streamlit as st

from . import logger
from dashboard.types import *
from dashboard.utils.history import *
from .storage import StageStorage, ObjectType


class InputStage(Stage):
    LOG_FILE = "logs/UserInputs.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.storage = StageStorage()

        history = get_json_file_data(self.LOG_FILE)
        prev_inputs = [UserInput(**entity) for entity in history]
        self.storage.restore(prev_inputs)

        logger.info("InputStage initialized")

    def __call__(self, *args, **kwargs):
        pass

    def activate(self) -> None:
        cols = st.columns(2)
        txt = cols[0].text_input("Text input:")  # also test st.test_area

        cols2 = cols[0].columns(2)

        add = cols2[0].button("Add")
        analyze = cols2[1].button("Analyze")

        cols[1].text("Your inputs:")
        for preview in self.storage.get_preview(ObjectType.userInput):
            cols[1].text(preview)

        if add and len(txt.strip()) > 0 and not self.storage.entity_exists(txt):
            data = UserInput(text=txt)
            self.storage.add_record(data)
            st.experimental_rerun()

        if analyze:
            st.experimental_rerun()

    def dump(self):
        j_data = (entity() for entity in self.storage.get_session_data(ObjectType.userInput))
        add_to_json_file(self.LOG_FILE, *j_data)
