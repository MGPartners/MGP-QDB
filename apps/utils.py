import streamlit as st
import datetime
from random import getrandbits
from .configs.mappings import Mappings, SystemMapping, QuestionMapping

def generate_id(subject: str, level: str, question_type: str, user_type: str, uid: str) -> str:
        date = datetime.datetime.now().strftime("%Y%m%d")
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
    st.sidebar.text(f"User ID: {uid}")
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


def create_question_form(question_type: str):
    question = st.text_area("Question", key=f"question_text_area")
    if question_type == "writing":
        question_point = st.text_area("Question Point", key="question_point_text_area").split("\n")
        etc = None
    elif question_type == "summarizing":
        question_point = None
        etc = None
    elif question_type == "emailing":
        question_point = None
        etc = st.text_area("Etc", key="question_etc_text_area")
    else:
        raise ValueError("Invalid question type")
    col1, col2 = st.columns(2)
    min_words = col1.number_input("Min Words", min_value=20, max_value=200, value=40, key="input_min_words")
    max_words = col2.number_input("Max Words", min_value=20, max_value=200, value=60, key="input_max_words")
    return {
        "question": question,
        "question_point": question_point,
        "etc": etc,
        "min_words": min_words,
        "max_words": max_words
    }

def rander_question_preview(question_type, question_dict) -> None:
    if question_type == "writing":
        topic = QuestionMapping.writing
    elif question_type == "summarizing":
        topic = QuestionMapping.summarizing
    elif question_type == "emailing":
        topic = QuestionMapping.emailing


    st.markdown(topic)
    st.markdown("""---""")
    st.markdown("""#### Preview""")
    st.markdown(f"""- {topic}""")
    st.markdown(f"""- {QuestionMapping.number_of_words.format(min_words = question_dict['min_words'],
                                                         max_words = question_dict['max_words'])}""")
    st.markdown(f"""- {QuestionMapping.Warning_summarizing}""")
    st.markdown("""---""")
    st.markdown(f"""
                {question_dict["question"]}
    """)
    st.markdown(f"""- {'\n- '.join(question_dict["question_point"])}""") if question_dict["question_point"] else None
    st.markdown(f"""- {question_dict["etc"]}""") if question_dict["etc"] else None
    st.markdown("""---""")

def rander_question_form(uid: str) -> None:
    subject, level, question_type, user_type = mapping_data(uid)
    docs_id = generate_id(subject, level, question_type, user_type, uid)
    question_dict = create_question_form(question_type)
    rander_question_preview(question_type, question_dict)

    if st.button("Submit"):
        data = {
            "id": docs_id,
            "question": question_dict["question"],
            "question_point": question_dict["question_point"],
            "etc": question_dict["etc"],
            "min_words": int(question_dict["min_words"]),
            "max_words": int(question_dict["max_words"]),
            "subject": subject,
            "level": level,
            "question_type": question_type,
            "created_at": datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            "created_by": uid,
            "user_type": user_type
        }
        st.markdown(data)
        # response = requests.post(f"{SystemMapping.api_endpoints}/add_question", json=data)
        # if response.status_code == 200:
        #     st.markdown("Question added successfully")
        # else:
        #     st.markdown("Error adding question") 
        st.markdown(f"""#### Submitted successfully. Question ID is below: 
                    {docs_id}""")