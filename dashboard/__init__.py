import streamlit as st
import logging

from dashboard.panel.user.conversation import Session
from dashboard.panel.login import Login

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
        Session(),
    ]

    def __init__(self):
        self.panels = {panel.__class__.__name__: idx for idx, panel in enumerate(self.PANELS)}
        logger.info(f"Dashboard initialized with {self.panels} panels")
        self.current_user = Login.run()

    def run(self):
        print(self.current_user)
        mode = ['specialist', 'specialist', None][0]
        mode = self.current_user[0]

        if mode == 'patient':
            panel = self.PANELS[0]
        elif mode == 'specialist':
            panel = self.PANELS[0]
        else:
            # self.current_user = Login.run()
            return

        st.sidebar.header(self.current_user[1])
        st.sidebar.subheader(self.current_user[0].title())
        panel.activate()

        logout_button = st.sidebar.button("Logout")
        if logout_button:
            self.current_user = (None, None)
            st.success("Logout Successfully!")
            st.experimental_rerun()

    def dump(self):
        pass
