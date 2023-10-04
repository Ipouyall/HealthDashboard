from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class ReportType(Enum):
    emoGauge = auto()
    msgSentiment = auto()
    sessionEmotionChanging = auto()


VALID_REPORTS = {
    "Emotion Gauge": ReportType.emoGauge,
    "Message Sentiment": ReportType.msgSentiment,
    "Session Emotion Changing": ReportType.sessionEmotionChanging,
}


@dataclass()
class Report:
    activeCharts: List[ReportType]
    specialistsNote: str
