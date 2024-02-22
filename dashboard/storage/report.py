from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class ReportType(Enum):
    emoGauge = auto()
    sessionSentimentChanging = auto()
    WordCloud = auto()


VALID_REPORTS = {
    "Emotion Gauge": ReportType.emoGauge,
    "Session's Sentiment Trend": ReportType.sessionSentimentChanging,
    "Word Cloud": ReportType.WordCloud,
}


@dataclass()
class Report:
    activeCharts: List[ReportType]
    specialistsNote: str
