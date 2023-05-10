import streamlit as st

from . import Stage, logger, UserInput
from dashboard.utils.history import add_to_json_file


class InputStage(Stage):
    LOG_FILE = "logs/UserInputs.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session_inputs: list[UserInput] = []
        self.last_returned_idx = 0
        self.return_till = 0
        logger.info("InputStage initialized")

    def get_session_data(self):
        idx = self.last_returned_idx
        self.last_returned_idx = self.return_till
        return self.session_inputs[idx: self.return_till]

    def __call__(self, *args, **kwargs):
        if "request session data":
            return self.get_session_data()

    def activate(self) -> None:
        cols = st.columns(2)
        txt = cols[0].text_input("Text input:")  # also test st.test_area

        cols2 = cols[0].columns(2)

        add = cols2[0].button("Add")
        analyze = cols2[1].button("Analyze")

        cols[1].text("This session's inputs:")
        for entity in self.session_inputs:
            text = str(entity)
            cols[1].text(text)

        if add and len(txt.strip()) > 0 and txt not in self.session_inputs:
            data = UserInput(text=txt)
            self.session_inputs.append(data)
            st.experimental_rerun()

        if analyze:
            self.return_till = len(self.session_inputs)
            st.experimental_rerun()

    def dump(self):
        j_data = (entity() for entity in self.session_inputs)
        add_to_json_file(self.LOG_FILE, *j_data)
