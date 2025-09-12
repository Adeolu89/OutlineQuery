import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from dotenv import load_dotenv
from langchain_community.document_loaders import PDFMinerLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()

# File Path
PDF_PATH = 'data/waterloo_courses/STAT331_Outline.pdf'
reader = PDFMinerLoader(PDF_PATH)
pdf_content = reader.load()

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 300
text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
docs = text_splitter.split_documents(pdf_content)

# Embeddings
embeddings = OpenAIEmbeddings(model='text-embedding-3-large')

# FAISS Vector Store
vectorstore = FAISS.from_documents(docs, embeddings)

# Query and retrieve relevant documents
query = input("Ask a question about the course outline: ")
found_docs = vectorstore.similarity_search(query, k=3)

# Create Context
context = "\n\n---\n\n".join(d.page_content for d in found_docs)

# Build a prompt for an answer
prompt = f"""You are a helpful assistant. Use ONLY the context to answer.

Context:
{context}

Question: {query}

Answer:"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) 

if context.strip():
    answer = llm.invoke(prompt).content
else:
    answer = "I don't know from the context."

print("ANSWER:\n", answer)
print("CONTEXT: \n", context)