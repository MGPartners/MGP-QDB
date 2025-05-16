import streamlit as st
from processors import authenticate

logged_in, uid, name = authenticate.login()

# if not logged_in:
#     st.markdown("## MG Partners")
#     st.markdown("### Question Database Management System")
#     st.markdown("#### Please log in to access the system.")
