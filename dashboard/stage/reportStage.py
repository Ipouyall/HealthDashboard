import streamlit as st

from . import logger
from dashboard.types import *
from dashboard.utils.history import *
from .storage import StageStorage, ObjectType
from dashboard.model.util import get_model
from dashboard.model import BaseModel
from dashboard import config


class ReportStage(Stage):
    LOG_FILE = config.ANALYZED_DUMP_FILE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model: BaseModel = get_model(config.DEPRESSION_MODEL)

        self.storage = StageStorage()

        logger.info("ReportStage initialized")

    def analyze(self, analyze, re_analyze):
        if analyze:
            entries = self.storage.get_new_data(ObjectType.userInput)
        elif re_analyze:
            entries = self.storage.get_data(ObjectType.userInput)
        else:
            raise NotImplementedError()

        for entry in entries:
            result = self.model.predict(**entry())
            report = Report(overall_status=result["label"], score=result["score"], text_id=entry.id)
            self.storage.add_record(report)

    def activate(self) -> None:
        cols = st.columns(5)

        cols[0].header("Date")
        cols[1].header("Text")
        cols[2].header("Status")

        analyze = cols[4].button("Analyze")
        re_analyze = cols[4].button("Re-Analyze")

        st.divider()

        if analyze or re_analyze:
            self.analyze(analyze, re_analyze)

        itr = zip(
            self.storage.get_data(ObjectType.userInput),
            self.storage.get_data(ObjectType.report)
        )
        for inp, rep in itr:
            cols = st.columns(5)
            cols[0].empty()
            cols[0].text(inp.date.strftime("%Y-%m-%d %H:%M"))
            cols[1].empty()
            cols[1].text(inp.text)
            status = rep.overall_status.title()
            if status == "Positive":
                score = int((rep.score-0.5)*200)
            elif status == "Negative":
                score = int((0.5-rep.score)*200)
            else:
                score = 0
            cols[2].progress(score, f"{status} ({score}%)")

            st.divider()

    def __call__(self, *args, **kwargs):
        pass

    def dump(self):
        pass
        j_data = (entity() for entity in self.storage.get_session_data(ObjectType.report))
        add_to_json_file(self.LOG_FILE, *j_data)
