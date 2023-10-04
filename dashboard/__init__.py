import streamlit as st
import logging

from dashboard.panel.user.conversation import Session
from dashboard.panel.specialist.session import Therapy
from dashboard.panel.login import Login
from dashboard.storage.role import Role

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
        Login(),
        Session(),
        Therapy(),
    ]

    def __init__(self):
        logger.info("Initializing Dashboard...")
        self.panels = {panel.__class__.__name__: idx for idx, panel in enumerate(self.PANELS)}
        logger.info(f"Dashboard initialized with {self.panels} panels")
        self.current_user = (None, None)

    def run(self):
        self.current_user = self.PANELS[0].get_user()

        print(self.current_user)
        mode = self.current_user[0]

        if mode == Role.User:
            panel = self.PANELS[1]
        elif mode == Role.Specialist:
            panel = self.PANELS[2]
        else:
            panel = self.PANELS[0]

        if mode is not None:
            # st.sidebar.markdown(f"### {self.current_user[1]}")
            # st.sidebar.markdown(f"#### {self.current_user[0].title()}") # To show the Role
            # st.sidebar.markdown(f"#### {self.current_user[0].title()}: {self.current_user[1].title()}")
            st.sidebar.markdown(
                f'### {self.current_user[1].title()}  <font size="1"> ({self.current_user[0].name.title()}) </font>',
                unsafe_allow_html=True,
            )

        st.sidebar.divider()
        panel.activate()

        if self.current_user[0] is not None:
            st.sidebar.divider()
            logout_button = st.sidebar.button("Logout")
            if logout_button:
                self.current_user = (None, None)
                st.success("Logout Successfully!")
                self.PANELS[0].logout()
                st.experimental_rerun()

    def dump(self):
        pass
