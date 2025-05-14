import streamlit as st
from importlib import reload
from processors import utils
import main
reload(main)

st.markdown("# Add Questions")

if main.logged_in:
    utils.init()
    from main import uid
    utils.render_question_form(uid)
