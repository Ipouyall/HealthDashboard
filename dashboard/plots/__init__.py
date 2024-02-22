import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download(["vader_lexicon", "punkt"])
sia = SentimentIntensityAnalyzer()
