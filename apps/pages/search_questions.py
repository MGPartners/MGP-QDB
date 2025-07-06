import streamlit as st
import httpx
from app_configs import mappings, api_settings
from os import getenv

st.markdown("# Search Questions")

if st.session_state.get("logged_in"):
    uid = st.session_state.uid
    api_endpoint = api_settings.api_endpoints.local_endpoint if getenv("ENVIRONMENT_TYPE") == "dev" \
                    else api_settings.api_endpoints.main_endpoint

    def render_sidebar(uid: str) -> str:
        st.sidebar.text(f"User ID: {uid}")
        return st.sidebar.selectbox("Search type", ["ID", "Keyword", "All"])


    def main(uid: str):
        search_type = render_sidebar(uid)
        st.markdown(f"## Search type: {search_type}")
        if search_type == "ID":
            question_id = st.text_input("Question ID", key="question_id")
            show_json = st.checkbox("Show as JSON", key="show_json_id")
            if st.button("Search"):
                response = httpx.get(api_endpoint + "/show_question/" + question_id)
                if response.status_code == 200:
                    question_data = response.json()
                    qid = question_data.get('question_id', question_id)
                    st.markdown(f"**Question ID:** `{qid}`")
                    st.markdown(f"**Question:** {question_data.get('question', '')}")
                    st.markdown(f"**Additional:** {'; '.join(question_data.get('additional_instructions', [])) if question_data.get('additional_instructions') else ''}")
                    st.markdown(f"**Underlined:** {question_data.get('underlined', '')}")
                    st.markdown(f"**Min Words:** {question_data.get('min_words', '')}")
                    st.markdown(f"**Max Words:** {question_data.get('max_words', '')}")
                    if show_json:
                        import json
                        st.code(json.dumps(question_data, ensure_ascii=False, indent=2), language="json")
                else:
                    st.error("Question not found.")
        elif search_type == "Keyword":
            exam_grade = st.selectbox("Grade", ["３級", "準２級", "準2級プラス", "２級", "準１級", "１級"])
            question_type = st.selectbox("Question type", ["英作文", "英文要約", "Email"])
            data_map = mappings.Mappings().get_mappings()
            exam_grade = data_map["grade_map"][exam_grade]
            # Map 'Email' to 'email' for backend
            question_type = 'email' if question_type == 'Email' else data_map["question_type_map"][question_type]
            show_json = st.checkbox("Show as JSON", key="show_json_keyword")
            if st.button("Search"):
                response = httpx.get(f"{api_endpoint}/show_questions?exam_grade={exam_grade}&question_type={question_type}")
                if response.status_code == 200:
                    questions = response.json()
                    if questions:
                        for qid, qdata in questions.items():
                            st.markdown("---")
                            st.markdown(f"**Question ID:** `{qid}`")
                            st.markdown(f"**Question:** {qdata.get('question', '')}")
                            st.markdown(f"**Additional:** {'; '.join(qdata.get('additional_instructions', [])) if qdata.get('additional_instructions') else ''}")
                            st.markdown(f"**Underlined:** {qdata.get('underlined', '')}")
                            st.markdown(f"**Min Words:** {qdata.get('min_words', '')}")
                            st.markdown(f"**Max Words:** {qdata.get('max_words', '')}")
                            if show_json:
                                import json
                                st.markdown('```json')
                                st.markdown(json.dumps(qdata, ensure_ascii=False, indent=2))
                                st.markdown('```')
                    else:
                        st.info("No questions found.")
                else:
                    st.error("No questions found.")
        elif search_type == "All":
            if st.button("List all questions"):
                response = httpx.get(api_endpoint + "/list_all_questions")
                if response.status_code == 200:
                    questions = response.json()
                    if questions:
                        # Count by exam_grade and question_type
                        from collections import defaultdict
                        import pandas as pd
                        count_dict = defaultdict(lambda: defaultdict(int))
                        for q in questions:
                            exam_grade = q.get('exam_grade', 'N/A')
                            qtype = q.get('question_type', 'N/A')
                            count_dict[exam_grade][qtype] += 1
                        # Prepare data for DataFrame
                        rows = []
                        for exam_grade, qtype_dict in count_dict.items():
                            for qtype, count in qtype_dict.items():
                                rows.append({'Grade': exam_grade, 'Question Type': qtype, 'Count': count})
                        df = pd.DataFrame(rows)
                        if not df.empty:
                            df = df.sort_values(['Grade', 'Question Type'])
                            st.dataframe(df, hide_index=True)
                        else:
                            st.info("No questions found.")
                    else:
                        st.info("No questions found.")
                else:
                    st.error("No questions found.")
    main(uid)
else:
    st.warning("Please log in to access this page.")



