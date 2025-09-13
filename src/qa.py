import os
import re
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from chunking import parse_course_outline_simple, create_chunks_improved

load_dotenv()


embeddings = OpenAIEmbeddings(model='text-embedding-3-large')

def create_vectorstore(chunks):
    """Create a FAISS vector store from document chunks."""
    return FAISS.from_documents(chunks, embeddings)

def answer_question(vectorstore, query: str, k: int = 3, llm_model: str = "gpt-4o-mini", temperature: float = 0) -> str:
    """Answer a question using the course outline vector store."""
    found_docs = vectorstore.similarity_search(query, k=k)
    context = "\n\n---\n\n".join(d.page_content for d in found_docs)

    if not context.strip():
        return "I don't know from the context."

    prompt = f"""You are a helpful assistant. Use ONLY the context to answer.

Context:
{context}

Question: {query}

Answer:"""

    llm = ChatOpenAI(model=llm_model, temperature=temperature)
    return llm.invoke(prompt).content
