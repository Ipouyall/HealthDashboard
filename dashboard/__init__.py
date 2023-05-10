import streamlit as st
import logging

from .types import Stage
from .stage.inputStage import InputStage
from .stage.reportStage import ReportStage
from dashboard.model.util import get_model_initializer


logger = logging.getLogger(__name__)


class Dashboard:
    __name = "Online Dashboard"
    __panels: dict[str, Stage] = {
        "Insert text": InputStage(),  # just inserting input
        "Report": ReportStage(model_initializer=get_model_initializer('basic')),
                  # get report with respect to input from user's new input(s)
        "Analysis": None,     # accumulated report from user's previous inputs
        "Feedback": None,     # for specialists and give them more power and to teach model
    }

    def __init__(self):
        self.tabs_title = list(self.__panels.keys())
        logger.info(f"Dashboard initialized with {self.tabs_title} tabs")
        self.state = None

        st.set_page_config(page_title=self.__name, layout="wide")
        st.title(self.__name)

    def run(self):
        active_tabs = st.tabs(self.tabs_title)

        # TODO: Fix this messy codes
        data = self.__panels["Insert text"]("request session data")
        if data:
            self.__panels["Report"](session_data=data)

        for idx, tab in enumerate(self.tabs_title):
            if self.__panels[tab] is None:
                continue
            with active_tabs[idx]:
                self.__panels[tab].activate()

    def dump(self):
        for panel in self.__panels:
            if self.__panels[panel] is not None:
                self.__panels[panel].dump()
