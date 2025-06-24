import streamlit as st
from processors import utils

st.markdown("# Add Questions")

if st.session_state.get("logged_in"):
    utils.init()
    subject, grade, question_type, user_type, official = utils.mapping_data(st.session_state.uid)
    docs_id = utils.generate_id(subject, grade, question_type, user_type, st.session_state.uid)

    # Use unified form logic from utils
    question_dict = utils.create_question_form(question_type)

    utils.render_question_preview(question_type, question_dict)

    if st.button("Submit"):
        utils.submit_question_form(docs_id, question_dict, subject, grade, question_type, st.session_state.uid, user_type, official)

    st.markdown("---")
    st.header("Batch Add Questions (JSON)")
    st.info("Input must be valid JSON (use double quotes, not single quotes). Example: [{\"question\": \"...\"}]")
    batch_json = st.text_area("Paste JSON array or object of questions here", key="batch_json_input", height=200)
    if st.button("Batch Submit"):
        import json
        if batch_json.strip().startswith("{") and "'" in batch_json and '"' not in batch_json:
            st.error("Input looks like a Python dict. Please use valid JSON with double quotes.")
            st.stop()
        try:
            questions = json.loads(batch_json)
            if isinstance(questions, dict):
                questions = [questions]
            assert isinstance(questions, list)
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
            st.stop()
        results = []
        for idx, q in enumerate(questions):
            try:
                # Fix typo and normalize fields
                if "officials" in q:
                    q["official"] = q.pop("officials")
                # Always use current session info for created_by, user_type, etc.
                docs_id = utils.generate_id(subject, grade, question_type, user_type, st.session_state.uid)
                q["created_by"] = st.session_state.uid
                q["user_type"] = user_type
                q["subject"] = subject
                q["grade"] = grade
                q["question_type"] = question_type
                q["official"] = bool(q.get("official", official))
                q["created_at"] = None  # Let backend set this if possible
                q["question_id"] = docs_id
                # Ensure required fields exist, fill with defaults if missing
                q.setdefault("min_words", 40)
                q.setdefault("max_words", 60)
                q.setdefault("underlined", "")
                if q.get("additional_instructions") is None:
                    q["additional_instructions"] = []
                q.setdefault("question", "")
                # Submit
                utils.submit_question_form(docs_id, q, subject, grade, question_type, st.session_state.uid, user_type, q["official"])
                results.append((idx+1, "Success"))
            except Exception as e:
                results.append((idx+1, f"Failed: {e}"))
        st.markdown("### Batch Results")
        for idx, res in results:
            st.write(f"Question {idx}: {res}")
else:
    st.warning("Please log in to access this page.")
