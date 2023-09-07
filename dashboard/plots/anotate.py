from annotated_text import annotation


def show_annotated(text, model, ph): pass
    # TODO: process text and prepare labels in here

    # Example of using to print it
    # ph.markdown(annotate_md(<the labeled text>), unsafe_allow_html=True)


def annotate_md(*text):
    """
    Annotate text with colors
    :param text: if is a token like (txt, label) would be colored
    currently, supported labels are: 'Angry', 'Sad', 'Happy'
    :return: markdown string
    You should then feed result to st.markdown with unsafe_allow_html=True parameter
    """
    BG_COLOR = {  # light red, light yellow, light green
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
