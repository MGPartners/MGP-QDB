import streamlit as st
from processors import utils

st.markdown("# Add Questions")

if st.session_state.get("logged_in"):
    utils.init()
    subject, exam_grade, question_type, user_type, official = utils.mapping_data(st.session_state.uid)
    docs_id = utils.generate_id(subject, exam_grade, question_type, user_type, st.session_state.uid)

    # Use unified form logic from utils
    question_dict = utils.create_question_form(question_type)

    utils.render_question_preview(question_type, question_dict)

    if st.button("Submit"):
        utils.submit_question_form(docs_id, question_dict, subject, exam_grade, question_type, st.session_state.uid, user_type, official)
else:
    st.warning("Please log in to access this page.")
