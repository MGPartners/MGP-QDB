import streamlit as st
from typing import Tuple

def login() -> Tuple[bool, str]:

    left, middle, logout_button_column = st.columns([2, 1, 1])

    with left:
        user_info = st.experimental_user
        if user_info.get('name') is not None:
            st.write(f":rainbow[Hello] **{user_info.get('name')}** :sparkles:")
            logged_in = True
        else:
            st.write("#### Please login to continue")
            logged_in = False

    with middle:
        google_button = st.button("Google Login")

        if google_button:
            st.login(provider="google")


    with logout_button_column:
        logout_button = st.button("Logout")
        if logout_button:
            st.logout()
    
    return logged_in, user_info.get('email') if logged_in else None