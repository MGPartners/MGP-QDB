import requests
import streamlit as st
from random import getrandbits
from apps import authenticate, utils
from apps.configs import mappings

api_endpoint = "http://192.168.77.84:8000"

st.title("MG Partners Question Database")

logged_in, uid = authenticate.login()

if logged_in:
    utils.init()

    utils.rander_question_form(uid)

    # subject, level, question_type, user_type = utils.mapping_data(uid)
    # docs_id = utils.generate_id(subject, level, question_type, user_type, uid)
    # st.markdown(docs_id)
                
    # question = st.text_area("Question")
    # question_point = st.text_area("Question Point")
    # instruction = st.text_area("Instruction")
    # min_words = st.text_input("Min Words", value="40")
    # max_words = st.text_input("Max Words", value="50")

    # st.markdown("""---""")
    # st.markdown("""### Preview""")
    # st.markdown(f"""#### Question ID: 
    #             {docs_id}""")
    # st.markdown(f"""
    #             {question}
    # """)
    # st.markdown(f"""- {question_point}""")
    # st.markdown(f"""- {instruction}""")
    # st.markdown(f"""- {min_words}""")
    # st.markdown(f"""- {max_words}""")
    # st.markdown("""---""")
    # st.markdown("""### Submit""")
    # if st.button("Submit"):
    #     data = {
    #         "id": docs_id,
    #         "question": question,
    #         "question_point": question_point,
    #         "instruction": instruction,
    #         "min_words": min_words,
    #         "max_words": max_words,
    #         "subject": subject,
    #         "level": level,
    #         "question_type": question_type,
    #         "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #         "created_by": uid,
    #         "user_type": user_type
    #     }
    #     st.markdown(data)
    #     response = requests.post(f"{api_endpoint}/add_question", json=data)
    #     if response.status_code == 200:
    #         st.markdown("Question added successfully")
    #     else:
    #         st.markdown("Error adding question")
