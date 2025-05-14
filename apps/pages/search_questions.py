import streamlit as st
import httpx
from app_configs import mappings, api_settings
from os import getenv
import main
from importlib import reload
reload(main)

st.markdown("# Search Questions")

if main.logged_in:
    from main import uid

    api_endpoint = api_settings.api_endpoints.local_endpoint if getenv("ENVIRONMENT_TYPE") == "dev" else api_settings.api_endpoints.main_endpoint

    def render_sidebar(uid: str) -> tuple:
        st.sidebar.text(f"User ID: {uid}")
        return st.sidebar.selectbox("Search type", ["ID", "Keyword", "All"])


    def main(uid: str):
        search_type = render_sidebar(uid)
        st.markdown(f"## Search type: {search_type}")
        if search_type == "ID":
            question_id = st.text_input("Question ID", key="question_id")
            if st.button("Search"):
                response = httpx.get(api_endpoint + "/show_question/" + question_id)
                if response.status_code == 200:
                    question_data = response.json()
                    st.json(question_data)
                else:
                    st.error("Question not found.")
        elif search_type == "Keyword":
            grade = st.selectbox("Grade", ["３級", "準２級", "２級", "準１級", "１級"])
            question_type = st.selectbox("Question type", ["英作文", "英文要約", "Ｅメール"])
            data_map = mappings.Mappings().get_mappings()
            grade = data_map["grade_map"][grade]
            question_type = data_map["question_type_map"][question_type]
            if st.button("Search"):
                response = httpx.get(f"{api_endpoint}/show_questions?grade={grade}&question_type={question_type}")
                if response.status_code == 200:
                    questions = response.json()
                    st.write(questions)
                else:
                    st.error("No questions found.")
        elif search_type == "All":
            if st.button("List all questions"):
                response = httpx.get(api_endpoint + "/list_all_questions")
                if response.status_code == 200:
                    questions = response.json()
                    st.write(questions)
                else:
                    st.error("No questions found.")
    main(uid)



