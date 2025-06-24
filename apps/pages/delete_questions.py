import streamlit as st
import httpx
from app_configs import mappings, api_settings
from os import getenv

st.markdown("# Delete Questions")

if st.session_state.get("logged_in"):
    uid = st.session_state.uid
    api_endpoint = api_settings.api_endpoints.local_endpoint if getenv("ENVIRONMENT_TYPE") == "dev" \
                    else api_settings.api_endpoints.main_endpoint

    search_type = st.sidebar.selectbox("Search type", ["ID", "Keyword"])
    question_id = None
    questions = None

    if search_type == "ID":
        question_id = st.text_input("Enter Question ID", key="delete_question_id")
        if st.button("Search by ID") and question_id:
            response = httpx.get(f"{api_endpoint}/show_question/{question_id}")
            if response.status_code == 200 and response.json():
                st.json(response.json())
            else:
                st.error("Question not found.")
    elif search_type == "Keyword":
        grade = st.selectbox("Grade", ["３級", "準２級", "準2級プラス", "２級", "準１級", "１級"])
        question_type = st.selectbox("Question type", ["英作文", "英文要約", "Ｅメール"])
        data_map = mappings.Mappings().get_mappings()
        grade = data_map["grade_map"][grade]
        question_type = data_map["question_type_map"][question_type]
        if st.button("Search by Keyword"):
            response = httpx.get(f"{api_endpoint}/show_questions?grade={grade}&question_type={question_type}")
            if response.status_code == 200 and response.json():
                questions = response.json()
                for qid, qdata in questions.items():
                    st.write(f"ID: {qid}")
                    st.json(qdata)
            else:
                st.error("No questions found.")

    st.markdown("---")
    delete_id = st.text_input("Enter Question ID to Delete", key="delete_id")
    if st.button("Delete Question") and delete_id:
        response = httpx.post(f"{api_endpoint}/delete_question", params={"question_id": delete_id})
        if response.status_code == 200:
            st.success(f"Question {delete_id} deleted successfully.")
        else:
            st.error(f"Failed to delete question {delete_id}.")
else:
    st.warning("Please log in to access this page.")
