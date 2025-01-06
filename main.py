import streamlit as st
from os import environ
import requests
from datetime import datetime
from random import getrandbits

# api_endpoint = "http://192.168.77.84:8000"

st.title("MG Partners Question Database")

st.markdown(
    r"""
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

def generate_id(subject: str, level: str, question_type: str, user_type: str, uid: str) -> str:
    date = datetime.now().strftime("%Y%m%d")

    return f"{subject}-{level}-{question_type}-{user_type}-{uid}-{date}-{getrandbits(16)}"

st.markdown("""Test""")
qdb_subject = st.sidebar.selectbox("Subject", ["英検"])
qdb_level =  st.sidebar.selectbox("Level", ["３級", "準２級", "２級", "準１級", "１級"])
qdb_question_type = st.sidebar.selectbox("Question type", ["英作文", "英文要約", "Ｅメール"])
qdb_uid = st.sidebar.text_input("User ID", value="aya@gracekyoto.com")
qdb_user_type = st.sidebar.selectbox("User type", ["student", "teacher"])

qdb_subject_map = {
    "英検": "eiken"
}

qdb_level_map = {
    "３級": "3",
    "準２級": "pre2",
    "２級": "2",
    "準１級": "pre1",
    "１級": "1"
}

qdb_question_type_map = {
    "英作文": "composition",
    "英文要約": "summary",
    "Ｅメール": "email"
}

dqb_user_type_map = {
    "student": "S",
    "teacher": "T"
}

qdb_subject = qdb_subject_map[qdb_subject]
qdb_level = qdb_level_map[qdb_level]
qdb_question_type = qdb_question_type_map[qdb_question_type]
qdb_user_type = dqb_user_type_map[qdb_user_type]

docs_id = generate_id(qdb_subject, qdb_level, qdb_question_type, qdb_user_type, qdb_uid)
st.markdown(docs_id)
            
qdb_question = st.text_area("Question")
qdb_question_point = st.text_area("Question Point")
qdb_instruction = st.text_area("Instruction")
qdb_min_words = st.text_input("Min Words", value="40")
qdb_max_words = st.text_input("Max Words", value="50")

st.markdown("""---""")
st.markdown("""### Preview""")
st.markdown(f"""#### Question ID: 
            {docs_id}""")
st.markdown(f"""
            {qdb_question}
""")
st.markdown(f"""- {qdb_question_point}""")
st.markdown(f"""- {qdb_instruction}""")
st.markdown(f"""- {qdb_min_words}""")
st.markdown(f"""- {qdb_max_words}""")
st.markdown("""---""")
st.markdown("""### Submit""")
if st.button("Submit"):
    data = {
        "id": docs_id,
        "question": qdb_question,
        "question_point": qdb_question_point,
        "instruction": qdb_instruction,
        "min_words": qdb_min_words,
        "max_words": qdb_max_words,
        "subject": qdb_subject,
        "level": qdb_level,
        "question_type": qdb_question_type,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "created_by": qdb_uid,
        "user_type": qdb_user_type
    }
    st.markdown(data)
    # response = requests.post(f"{api_endpoint}/add_question", json=data)
    # if response.status_code == 200:
    #     st.markdown("Question added successfully")
    # else:
    #     st.markdown("Error adding question")



# store_to_firestore(
#             project_name=environ.get("GCP_PROJECT_ID"),
#             collection_name="assignments_responses",
#             document_id=data["id"],
#             data=data
#         )