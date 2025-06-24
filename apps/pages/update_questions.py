import streamlit as st
import httpx
from app_configs import api_settings
from os import getenv

st.markdown("# Update Questions")

if st.session_state.get("logged_in"):
    api_endpoint = api_settings.api_endpoints.local_endpoint if getenv("ENVIRONMENT_TYPE") == "dev" \
                    else api_settings.api_endpoints.main_endpoint

    question_id = st.text_input("Enter Question ID", key="update_question_id")
    if 'selected_qdata' not in st.session_state:
        st.session_state.selected_qdata = None

    if st.button("Search by ID") and question_id:
        response = httpx.get(f"{api_endpoint}/show_question/{question_id}")
        if response.status_code == 200 and response.json():
            st.session_state.selected_qdata = response.json()
            st.session_state.selected_qid = question_id
        else:
            st.error("Question not found.")
            st.session_state.selected_qdata = None
            st.session_state.selected_qid = None

    selected_qdata = st.session_state.selected_qdata
    selected_qid = st.session_state.get('selected_qid', question_id)

    if selected_qdata:
        st.markdown("---")
        st.write(f"Editing Question ID: {selected_qid}")
        new_question = st.text_area("Question", value=selected_qdata.get("question", ""), key="update_new_question")
        new_additional = st.text_area(
            "Additional Instructions",
            value="\n".join(selected_qdata.get("additional_instructions", [])) if selected_qdata.get("additional_instructions") else "",
            key="update_new_additional"
        )
        new_underlined = st.text_input("Underlined", value=selected_qdata.get("underlined", ""), key="update_new_underlined")
        new_min_words = st.number_input("Min Words", min_value=0, value=int(selected_qdata.get("min_words", 0)), key="update_new_min_words")
        new_max_words = st.number_input("Max Words", min_value=0, value=int(selected_qdata.get("max_words", 0)), key="update_new_max_words")
        if st.button("Update Question"):
            update_data = {
                "question": new_question,
                "additional_instructions": new_additional.split("\n") if new_additional else [],
                "underlined": new_underlined,
                "min_words": int(new_min_words),
                "max_words": int(new_max_words)
            }
            response = httpx.post(
                f"{api_endpoint}/update_question",
                params={"question_id": selected_qid},
                json=update_data
            )
            if response.status_code == 200:
                st.session_state.update_success = f"Question {selected_qid} updated successfully."
                st.session_state.selected_qdata = None
                st.session_state.selected_qid = None
                st.rerun()
            else:
                st.error(f"Failed to update question {selected_qid}.")

    # Show success message after rerun if present
    if st.session_state.get("update_success"):
        st.success(st.session_state.update_success)
        del st.session_state["update_success"]
else:
    st.warning("Please log in to access this page.")
