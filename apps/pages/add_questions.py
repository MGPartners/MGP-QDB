import streamlit as st
from processors import utils

st.markdown("# Add Questions")

if st.session_state.get("logged_in"):
    utils.init()
    # Use original Japanese labels for selectbox
    subject = st.sidebar.selectbox("Subject", ["英検"])
    exam_grade = st.sidebar.selectbox("Grade", ["３級", "準２級", "２級", "準１級", "１級"])
    question_type_label = st.sidebar.selectbox("Question type", ["英作文", "英文要約", "Ｅメール"])
    user_type = st.sidebar.selectbox("User type", ["Teacher", "Student"])
    official = st.sidebar.checkbox("Official", value=False)
    # Map 'Ｅメール' to 'email' for backend
    data_map = utils.mappings.Mappings().get_mappings()
    subject = data_map["subject_map"][subject]
    exam_grade = data_map["grade_map"][exam_grade]
    question_type = 'email' if question_type_label == 'Ｅメール' else data_map["question_type_map"][question_type_label]
    user_type = data_map["user_type_map"][user_type]
    docs_id = utils.generate_id(subject, exam_grade, question_type, user_type, st.session_state.uid)

    # Use unified form logic from utils
    question_dict = utils.create_question_form(question_type)

    # Show the question text in the preview
    st.markdown("---")
    st.markdown("#### Preview")
    st.markdown(f"**Question:** {question_dict.get('question', '')}")
    utils.render_question_preview(question_type, question_dict)

    if st.button("Submit"):
        utils.submit_question_form(docs_id, question_dict, subject, exam_grade, question_type, st.session_state.uid, user_type, official)
else:
    st.warning("Please log in to access this page.")
