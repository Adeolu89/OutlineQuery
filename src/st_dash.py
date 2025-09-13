import streamlit as st
from chunking import parse_course_outline_simple, create_chunks_improved
from qa import create_vectorstore, answer_question

st.set_page_config(page_title="OutlineQuery", layout="wide")
st.title("OutlineQuery: A Waterloo Course Outline Chatbot")

file = st.file_uploader("Upload your course outline", type="html")

if file is not None:
    # Build the vectorstore once and keep it in session state
    if "vectorstore" not in st.session_state:
        sections = parse_course_outline_simple(file)
        chunks = create_chunks_improved(sections)
        st.session_state.vectorstore = create_vectorstore(chunks)

    st.subheader("Ask a question")
    with st.form("qa_form"):
        query = st.text_input("Your question")
        submitted = st.form_submit_button("Get answer")

    if submitted and query:
        answer = answer_question(st.session_state.vectorstore, query)
        st.write(answer)
