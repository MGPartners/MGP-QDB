import streamlit as st
import datetime
import httpx
from random import getrandbits
from app_configs import mappings, api_settings
from io_schema import request_models


def generate_id(subject: str, grade: str, question_type: str, user_type: str, uid: str) -> str:
        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_bits = getrandbits(8)
        u_parts = uid.split('@')
        if len(u_parts) == 2:
            combined_uid = ''.join(map(''.join, zip(u_parts[0], u_parts[1])))
        else:
            combined_uid = uid[::-1]
        return f"{subject}-{grade}-{question_type}-{user_type}-{combined_uid}-{date}-{random_bits}"

def init() -> None:
    st.markdown(
        """<style>
        .stAppDeployButton {
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True
    )

def render_sidebar(uid: str) -> tuple:
    st.sidebar.text(f"User ID: {uid}")
    subject = st.sidebar.selectbox("Subject", ["英検"])
    grade = st.sidebar.selectbox("Grade", ["３級", "準２級", "２級", "準１級", "１級"])
    question_type = st.sidebar.selectbox("Question type", ["英作文", "英文要約", "Ｅメール"])
    user_type = st.sidebar.selectbox("User type", ["Teacher", "Student"])
    official = st.sidebar.checkbox("Official", value=False)
    return subject, grade, question_type, user_type, official

def mapping_data(uid: str) -> tuple:
    subject, grade, question_type, user_type, official = render_sidebar(uid)
    data_map = mappings.Mappings().get_mappings()
    return (
        data_map["subject_map"][subject],
        data_map["grade_map"][grade],
        data_map["question_type_map"][question_type],
        data_map["user_type_map"][user_type],
        official,
    )

def create_question_form(question_type: str):
    question = st.text_area("QUESTION", key="question_text_area")
    additional_instructions = []
    underlined = ""
    if question_type == "composition":
        additional_instructions = [pt for pt in st.text_area("POINT", key="additional_text_area").split("\n") if pt.strip()]
    elif question_type == "e_mail":
        additional_instructions = [st.text_input("Email to", key="ask_it")]
        underlined = st.text_area("Underlined", key="question_etc_input")
    # For summary, both fields remain empty
    col1, col2 = st.columns(2)
    min_words = col1.number_input("Min Words", min_value=15, max_value=200, value=40, key="input_min_words")
    max_words = col2.number_input("Max Words", min_value=15, max_value=200, value=60, key="input_max_words")
    return {
        "question": question,
        "additional_instructions": additional_instructions,
        "underlined": underlined,
        "min_words": min_words,
        "max_words": max_words
    }

def POINT_CHECKER(additional_instructions):
    if additional_instructions:
        st.markdown("##### POINTS")
        st.markdown("".join([f"- {pt}\n" for pt in additional_instructions]))

def render_question_preview_base(topic, question_dict) -> None:
    st.markdown("---")
    st.markdown("#### Preview")
    st.markdown(f"- {topic}")
    st.markdown(f"- {mappings.QuestionMapping.number_of_words.format(min_words=question_dict['min_words'], max_words=question_dict['max_words'])}")

def render_question_preview(question_type, question_dict) -> None:
    if question_type == "composition":
        render_question_preview_base(mappings.QuestionMapping.composition, question_dict)
        POINT_CHECKER(question_dict["additional_instructions"])
        if question_dict["underlined"]:
            st.write(f"##### Underlined \n - {question_dict['underlined']}")
    elif question_type == "summary":
        render_question_preview_base(mappings.QuestionMapping.summary, question_dict)
        st.markdown(f"- {mappings.QuestionMapping.Warning_summary}")
    elif question_type == "e_mail":
        topic = mappings.QuestionMapping.e_mail.format(
            additional=question_dict["additional_instructions"][0] if question_dict["additional_instructions"] else ""
        )
        render_question_preview_base(topic, question_dict)
        if question_dict["underlined"]:
            st.markdown(f"- {question_dict['underlined']}")
    st.markdown("---")

def submit_question_form(docs_id, question_dict, subject, grade, question_type, uid, user_type, official) -> None:
    data = request_models.QuestionData(
        additional_instructions=question_dict["additional_instructions"],
        grade=grade,
        min_words=int(question_dict["min_words"]),
        max_words=int(question_dict["max_words"]),
        question=question_dict["question"],
        question_type=question_type,
        subject=subject,
        underlined=question_dict["underlined"],
        question_id=docs_id,
        created_by=uid,
        created_at=int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp()),
        user_type=user_type,
        data_name="eiken_questions",
        official=official,
    ).model_dump()
    client = httpx.Client(timeout=60)
    response = client.post(f"{api_settings.api_endpoints.main_endpoint}/add_question", json=data)
    if response.status_code == 200:
        st.markdown("Question added successfully")
        st.markdown(f"#### Submitted successfully. Question ID is below: \n{docs_id}")
    else:
        st.markdown(f"Error adding question, status code: {response.status_code}")
        st.markdown(f"Response details: {response.text}")
    st.markdown("---")

def render_question_form(uid: str) -> None:
    subject, grade, question_type, user_type, official = mapping_data(uid)
    docs_id = generate_id(subject, grade, question_type, user_type, uid)
    question_dict = create_question_form(question_type)
    if not question_dict:
        st.stop()
    render_question_preview(question_type, question_dict)
    if st.button("Submit"):
        submit_question_form(docs_id, question_dict, subject, grade, question_type, uid, user_type, official)


