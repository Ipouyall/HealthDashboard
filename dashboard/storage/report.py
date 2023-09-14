from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class ReportType(Enum):
    emoGauge = auto()
    msgSentiment = auto()
    sessionEmotionChanging = auto()


@dataclass()
class Report:
    activeCharts: List[ReportType]
    specialistsNote: str
