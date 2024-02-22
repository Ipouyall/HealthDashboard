import streamlit as st
from streamlit_echarts import st_echarts
import nltk
from nltk.stem.porter import PorterStemmer
from functools import reduce

stemmer = PorterStemmer()


def __preprocess(sentence):
    tokens = nltk.word_tokenize(sentence)
    tokens = [token for token in tokens if token.isalpha()]
    stems = [stemmer.stem(token) for token in tokens]
    freqs = nltk.FreqDist(stems)

    return freqs


def WordCould(text, ph):
    freqs = __preprocess(text)

    option = {
        "tooltip": {},
        "series": [
            {
                "type": "wordCloud",
                "data": [{"name": stem, "value": freq} for stem, freq in freqs.items()],
            }
        ]
    }

    with ph:
        st_echarts(options=option, height="400px")



