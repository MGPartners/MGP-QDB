import streamlit as st
from processors import authenticate


def show_login_page():
    st.markdown("## MG Partners")
    st.markdown("### Question Database Management System")
    st.markdown("#### Please log in to access the system.")


def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.uid = None
        st.session_state.name = None

    if not st.session_state.logged_in:
        logged_in, uid, name = authenticate.login()
        if logged_in:
            st.session_state.logged_in = True
            st.session_state.uid = uid
            st.session_state.name = name
        else:
            show_login_page()
            return
    # ...add main app logic here...


if __name__ == "__main__":
    main()
