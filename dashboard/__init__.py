import streamlit as st
import logging

from dashboard.panel.conversation import Conversation

# from .types import Stage
# from .stage.inputStage import InputStage
# from .stage.reportStage import ReportStage
# from .stage.analysisStage import AnalysisStage
# from .stage.experiment import Experimental


logger = logging.getLogger(__name__)


class Dashboard:
    # __panels: dict[str, dict[str, Stage]] = {
    #     "User": {
    #         "Insert text": InputStage(),  # just inserting input
    #         # "Report": ReportStage(),  # get report with respect to input from user's new input(s)
    #         # "Analysis": AnalysisStage(),     # accumulated report from user's previous inputs
    #         "Experimental": Experimental(),
    #     },
    #     "Admin": {
    #         # "Insert text": InputStage(),  # just inserting input
    #         # "Report": ReportStage(),  # get report with respect to input from user's new input(s)
    #         # "Analysis": AnalysisStage(),     # accumulated report from user's previous inputs
    #         "Experimental": Experimental(),
    #     }
    # }
    PANELS = [
        Conversation()
    ]

    def __init__(self):
        self.panels = {panel.__class__.__name__: idx for idx, panel in enumerate(self.PANELS)}
        logger.info(f"Dashboard initialized with {self.panels} modes")
        self.state = None

    def run(self):
        mode = st.sidebar.selectbox("Mode", (None,) + tuple(self.panels.keys()))
        if mode is None:
            return

        idx = self.panels[mode]
        panel = self.PANELS[idx]
        panel.activate()

    def dump(self):
        pass
