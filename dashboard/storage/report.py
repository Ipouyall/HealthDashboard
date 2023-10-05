from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class ReportType(Enum):
    emoGauge = auto()
    sessionSentimentChanging = auto()


VALID_REPORTS = {
    "Emotion Gauge": ReportType.emoGauge,
    "Session's Sentiment Trend": ReportType.sessionSentimentChanging,
}


@dataclass()
class Report:
    activeCharts: List[ReportType]
    specialistsNote: str
