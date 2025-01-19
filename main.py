import streamlit as st
from apps import authenticate, utils

api_endpoint = "https://mgpta.asia-northeast2.run.app/"

st.title("MG Partners Question Database")

logged_in, uid = authenticate.login()

if logged_in:
    utils.init()

    utils.rander_question_form(uid)
