import atexit

import streamlit as st
from dashboard import Dashboard


__author__ = "Pouya Sadeghi"
__contact__ = "https://github.com/ipouyall"
__copyright__ = "Copyright 2023,"
__deprecated__ = False
__license__ = "None"
__app_name__ = "Online Dashboard"

st.set_page_config(page_title=__app_name__, layout="wide")
st.title(__app_name__)

if "app" not in st.session_state:
    st.session_state.app = Dashboard()
    atexit.register(st.session_state.app.dump)
    # st.experimental_rerun()

st.session_state.app.run()
