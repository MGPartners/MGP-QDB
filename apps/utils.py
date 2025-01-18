import streamlit as st
from datetime import datetime
from random import getrandbits
from .configs.mappings import Mappings

def generate_id(subject: str, level: str, question_type: str, user_type: str, uid: str) -> str:
        date = datetime.now().strftime("%Y%m%d")
        return f"{subject}-{level}-{question_type}-{user_type}-{uid.split('@')[0]}-{date}-{getrandbits(16)}"

def init() -> None:
    st.markdown(
        r"""
        <style>
        .stAppDeployButton {
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True
    )

def render_sidebar(uid: str) -> tuple:
    st.sidebar.markdown(f"User ID: {uid}")
    subject = st.sidebar.selectbox("Subject", ["英検"])
    level = st.sidebar.selectbox("Level", ["３級", "準２級", "２級", "準１級", "１級"])
    question_type = st.sidebar.selectbox("Question type", ["英作文", "英文要約", "Ｅメール"])
    user_type = st.sidebar.selectbox("User type", ["Teacher", "Student"])
    return subject, level, question_type, user_type

def mapping_data(uid: str) -> tuple:
    subject, level, question_type, user_type = render_sidebar(uid)
    mappings = Mappings().get_mappings()
    return (
        mappings["subject_map"][subject],
        mappings["level_map"][level],
        mappings["question_type_map"][question_type],
        mappings["user_type_map"][user_type]
    )

def rander_question_form(uid: str) -> None:
    subject, level, question_type, user_type = mapping_data(uid)
    docs_id = generate_id(subject, level, question_type, user_type, uid)
    st.markdown(docs_id)
                
    question = st.text_area("Question")
    question_point = st.text_area("Question Point")
    instruction = st.text_area("Instruction")
    min_words = st.text_input("Min Words", value="40")
    max_words = st.text_input("Max Words", value="50")

    st.markdown("""---""")
    st.markdown("""### Preview""")
    st.markdown(f"""#### Question ID: 
                {docs_id}""")
    st.markdown(f"""
                {question}
    """)
    st.markdown(f"""- {question_point}""")
    st.markdown(f"""- {instruction}""")
    st.markdown(f"""- {min_words}""")
    st.markdown(f"""- {max_words}""")
    st.markdown("""---""")
    st.markdown("""### Submit""")
    if st.button("Submit"):
        data = {
            "id": docs_id,
            "question": question,
            "question_point": question_point,
            "instruction": instruction,
            "min_words": min_words,
            "max_words": max_words,
            "subject": subject,
            "level": level,
            "question_type": question_type,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": uid,
            "user_type": user_type
        }
        st.markdown(data)
        # response = requests.post(f"{api_endpoint}/add_question", json=data)
        # if response.status_code == 200:
        #     st.markdown("Question added successfully")
        # else:
        #     st.markdown("Error adding question") 
