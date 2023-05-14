import streamlit as st

from . import logger
from dashboard.types import *
from dashboard.utils.history import *
from .storage import StageStorage, ObjectType
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression


class AnalysisStage(Stage):
    LOG_FILE = "logs/Analysis.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.storage = StageStorage()

        logger.info("AnalysisStage initialized")

    def activate(self) -> None:
        # Create a DataFrame from the Report and UserInput classes
        df = pd.DataFrame([
            (report.overall_status, report.score, user_input.text, user_input.date)
            for report, user_input in zip(
                self.storage.get_data(ObjectType.report),
                self.storage.get_data(ObjectType.userInput)
            )
        ], columns=['overall_status', 'score', 'text', 'date'])

        # Create a figure and axes
        fig, ax = plt.subplots()

        # Plot the data
        ax.scatter(
            df['date'], df['score'].values,
            c=df['overall_status'].map({'POSITIVE': 'red', 'NEUTRAL': 'yellow', 'NEGATIVE': 'blue'}),
            alpha=0.5
        )

        # Add a legend
        ax.legend({'POSITIVE': 'red', 'NEUTRAL': 'yellow', 'NEGATIVE': 'blue'},
                  loc='upper right')

        # Add a title and labels
        ax.set_title('Report Scores by Date')
        ax.set_xlabel('Date')
        ax.set_ylabel('Score')

        # Show the plot
        st.pyplot(fig)

    def dump(self):
        pass

    def __call__(self, *args, **kwargs):
        pass
