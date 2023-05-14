import streamlit as st

from . import logger
from dashboard.types import *
from dashboard.utils.history import *
from .storage import StageStorage, ObjectType
from dashboard.model import BaseModel


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

        self.storage = StageStorage()

        logger.info("ReportStage initialized")

    def analyze(self):
        new_entry = self.storage.get_new_data(ObjectType.userInput)

        for entry in new_entry:
            if self.model is None:
                self.model = self.model_initializer()

            result = self.model.predict(**entry())
            report = Report(overall_status=result["label"], score=result["score"], text_id=entry.id)
            self.storage.add_record(report)

    def activate(self) -> None:
        self.analyze()

        itr = zip(
            self.storage.get_preview(ObjectType.userInput),
            self.storage.get_preview(ObjectType.report)
        )
        for entry_text, report_text in itr:
            st.text(f"{entry_text + ' ':-<70}--> {report_text}")

    def __call__(self, *args, **kwargs):
        pass

    def dump(self):
        j_data = (entity() for entity in self.storage.get_session_data(ObjectType.report))
        add_to_json_file(self.LOG_FILE, *j_data)
