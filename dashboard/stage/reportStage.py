import streamlit as st

from . import Stage, logger, UserInput
from dashboard.model import Report, BaseModel
from dashboard.utils.history import add_to_json_file


class ReportStage(Stage):
    LOG_FILE = "logs/AnalyzeResults.json"

    def __init__(
            self,
            model: BaseModel = None,
            model_initializer=None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.model: [BaseModel, None] = model
        self.model_initializer = model_initializer

        assert self.model is not None or self.model_initializer is not None, \
               "you should specify model_initializer or model"

        self.session_data: list[UserInput] = []
        self.reports: list[Report] = []
        self.last_processed = 0
        logger.info("ReportStage initialized")


    def analyze(self):
        new_entry = self.session_data[self.last_processed:]
        if len(new_entry) == 0:
            return
        self.last_processed = len(self.session_data)

        if self.model is None:
            self.model = self.model_initializer()

        for entry in new_entry:
            result = self.model.predict(**entry())
            report = Report(overall_status=result["label"], score=result["score"])
            self.reports.append(report)

    def activate(self) -> None:
        self.analyze()

        for entry, report in zip(self.session_data, self.reports):
            entry_text = str(entry)
            report_text = str(report)
            st.text(f"{(entry_text if len(entry_text) < 50 else entry_text[:50]+'...')+' ':-<50}--> {report_text}")

    def __call__(self, *args, **kwargs):
        if "session_data" in kwargs:
            for entity in kwargs["session_data"]:
                self.session_data.append(entity)

    def dump(self):
        j_data = (entity() for entity in self.reports)
        add_to_json_file(self.LOG_FILE, *j_data)


# TODO: add some functionality to be able to add new data of a session uniquely and process them once
