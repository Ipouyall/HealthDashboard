import streamlit as st
from annotated_text import annotation

from . import logger
from dashboard.types import *
from dashboard.utils.history import *
from dashboard.storage.storage import StageStorage, ObjectType
from dashboard import config


class InputStage(Stage):
    LOG_FILE = config.USER_INPUT_DUMP_FILE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.storage = StageStorage()

        history = get_json_file_data(self.LOG_FILE)
        prev_inputs = [UserInput(**entity) for entity in history]
        self.storage.restore(prev_inputs)

        logger.info("InputStage initialized")

    def __call__(self, *args, **kwargs):
        pass

    def activate(self) -> None:
        cols = st.columns(2)

        txt = cols[0].text_input("Text input:")  # also test st.test_area

        cols2 = cols[0].columns(2)

        add = cols2[0].button("Add")

        cols[1].text("Your inputs:")
        for preview in self.storage.get_preview(ObjectType.userInput):
            cols[1].text(preview)

        if add and len(txt.strip()) > 0 and not self.storage.entity_exists(txt):
            data = UserInput(text=txt)
            self.storage.add_record(data)
            st.experimental_rerun()

        cols[0].markdown(
            annotate_md('Lorem',
             ('ipsum', 'Happy'),
             'dolor',
             'sit',
             'amet,',
             ('consectetur', 'Happy'),
             'adipiscing',
             ('elit.', 'Sad'),
             'Nullam',
             'nec',
             'aliquam',
             ('neque.', 'Sad'),
             ('Mauris', 'Happy'),
             ('pellentesque', 'Happy'),    'elit',    ('nec', 'Angry'),    'risus',    ('varius,', 'Sad'),    'ut',    ('interdum', 'Happy'),    'ipsum',    ('vestibulum.', 'Sad'),    'Sed',    ('vitae', 'Happy'),    'augue',    ('vel', 'Angry'),    'odio',    ('consectetur', 'Happy'),    'aliquet.',    ('Donec', 'Angry'),    'eget',    ('turpis', 'Happy'),    'mauris.',    ('Vivamus', 'Happy'),    'condimentum',    ('dolor', 'Happy'),    'quis',    ('urna', 'Happy'),    'rhoncus,',    ('vel', 'Happy'),    'egestas',    ('neque', 'Sad'),    'laoreet.'),
            unsafe_allow_html=True,
        )

    def dump(self):
        j_data = (entity() for entity in self.storage.get_session_data(ObjectType.userInput))
        add_to_json_file(self.LOG_FILE, *j_data)


def annotate_md(*text):
    BG_COLOR = { # light red, light yellow, light green
        'Angry': '#ffcccc',
        'Sad': '#ffffcc',
        'Happy': '#ccffcc',
    }
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