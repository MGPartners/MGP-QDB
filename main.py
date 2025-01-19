import streamlit as st
from apps import authenticate, utils

st.title("MG Partners Question Database")

logged_in, uid = authenticate.login()

if logged_in:
    utils.init()

    utils.render_question_form(uid)
