import streamlit as st
from apps import authenticate, utils
import os

# Debug logic to check paths
file_path = "/app/main.py"
if os.path.exists(file_path):
    st.write(f"File exists: {file_path}")
else:
    st.write(f"File does not exist: {file_path}")

# List all files in the directory
directory_path = "/usr/src/app/"
if os.path.isdir(directory_path):
    st.write(f"Directory exists: {directory_path}")
    files = os.listdir(directory_path)
    st.write("Files in directory:")
    for file in files:
        st.write(file)
else:
    st.write(f"Directory does not exist: {directory_path}")

directory_path = "/"
if os.path.isdir(directory_path):
    st.write(f"Directory exists: {directory_path}")
    files = os.listdir(directory_path)
    st.write("Files in directory:")
    for file in files:
        st.write(file)
else:
    st.write(f"Directory does not exist: {directory_path}")


api_endpoint = "https://mgpta.asia-northeast2.run.app/"

st.title("MG Partners Question Database")

logged_in, uid = authenticate.login()

if logged_in:
    utils.init()

    utils.rander_question_form(uid)
