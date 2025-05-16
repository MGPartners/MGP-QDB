import streamlit as st
from processors import utils
import main

st.markdown("# Add Questions")

if main.logged_in:
    utils.init()
    from main import uid
    utils.render_question_form(uid)
