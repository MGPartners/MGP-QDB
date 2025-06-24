import streamlit as st
from processors import utils

st.markdown("# Add Questions")

if st.session_state.get("logged_in"):
    utils.init()
    utils.render_question_form(st.session_state.uid)
else:
    st.warning("Please log in to access this page.")
