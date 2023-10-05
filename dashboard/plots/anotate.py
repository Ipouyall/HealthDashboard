from annotated_text import annotation
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import nltk
from typing import Literal
import streamlit as st

nltk.download(["vader_lexicon", "punkt"])
sia = SentimentIntensityAnalyzer()



def annotate_md(*text, mode:Literal['word', 'sentence']):
    """
    Annotate text with colors
    :param text: if is a token like (txt, label) would be colored
    currently, supported labels are: 'Angry', 'Sad', 'Happy'
    :return: markdown string
    You should then feed result to st.markdown with unsafe_allow_html=True parameter
    """
    if mode == 'word':
        BG_COLOR = {  # light red, light yellow, light green
            'Angry': '#ffcccc',
            'Sad': '#ffffcc',
            'Happy': '#ccffcc',
        }
    elif mode == 'sentence':
        BG_COLOR = {  # light yellow, light green
            'neg': '#ffffcc',
            'pos': '#ccffcc',
        }
    else:
        print(f"Unknown mode for annotation: {mode}")
        raise Exception()

    comp_text = ""
    for t in text:
        if isinstance(t, tuple):
            comp_text += str(annotation(*t, background_color=BG_COLOR[t[1]], color='black'))
        elif isinstance(t, str):
            comp_text += t
        else:
            raise TypeError(f"Expected str or tuple, got {type(t)}")
        comp_text += " "
    return comp_text


def show_annotated(text, threshold):
    sentences_tok = sent_tokenize(text)
    sentences = []
    for sentence in sentences_tok:
        scores = sia.polarity_scores(sentence)
        if scores['neu'] > max(scores['neg'], scores['pos']):
            sentences.append(sentence)
        elif scores['neg'] > scores['pos'] and scores['neg'] >= threshold:
            sentences.append(tuple([sentence, 'neg']))
        elif scores['pos'] > scores['neg'] and scores['pos'] >= threshold:
            sentences.append(tuple([sentence, 'pos']))
        else:
            sentences.append(sentence)

    st.markdown(
        annotate_md(*sentences, mode="sentence"),
        unsafe_allow_html=True
    )
