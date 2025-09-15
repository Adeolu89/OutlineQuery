import streamlit as st
from chunking import parse_course_outline_simple, create_chunks_improved
from qa import create_vectorstore, answer_question

st.set_page_config(page_title="OutlineQuery", layout="wide")
st.title("OutlineQuery: A Waterloo Course Outline Chatbot")

# Initialize session state for the filename
if "processed_filename" not in st.session_state:
    st.session_state.processed_filename = None

file = st.file_uploader("Upload your course outline as a HTML file", type="html")

if file is not None:
    # Re-create the vectorstore if a new file is uploaded
    if "vectorstore" not in st.session_state or st.session_state.processed_filename != file.name:
        with st.spinner("Processing document..."):
            sections = parse_course_outline_simple(file)
            chunks = create_chunks_improved(sections)
            st.session_state.vectorstore = create_vectorstore(chunks)
            st.session_state.processed_filename = file.name # Store the name of the processed file

    st.subheader("Ask a question")
    with st.form("qa_form"):
        query = st.text_input("Your question")
        submitted = st.form_submit_button("Get answer")

    if submitted and query:
        with st.spinner("Finding answer..."):
            answer = answer_question(st.session_state.vectorstore, query)
            st.write(answer)
