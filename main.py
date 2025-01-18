import streamlit as st
from apps import authenticate, utils

api_endpoint = "http://192.168.77.84:8000"

st.title("MG Partners Question Database")

logged_in, uid = authenticate.login()

if logged_in:
    utils.init()

    utils.rander_question_form(uid)
