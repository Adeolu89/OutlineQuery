# OutlineQuery PDF QA Prototype

Prototype steps:
1. Load course outline PDF (`data/waterloo_courses/STAT331_Outline.pdf`) with `PDFMinerLoader`.
2. Split into overlapping chunks (size=1000, overlap=300).
3. Embed chunks using OpenAI `text-embedding-3-large`.
4. Store vectors in in‑memory FAISS.
5. User enters a question (k=3 retrieval).
6. Build a context‑only prompt.
7. Get deterministic answer from `gpt-4o-mini` (temperature=0).
8. Print answer plus raw context.

Main script: `main.py`

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install langchain langchain-community langchain-openai faiss-cpu python-dotenv
python main.py
```

Sample question:  
What are the grading components?

## Environment Variables

Create a clean `.env` (no quotes, no spaces around =):

```
OPENAI_API_KEY=your_openai_key
```

Rotate the currently committed key immediately (it is exposed and should be treated as compromised). Remove any quotes/spaces in the real file.

## How It Works

1. Loader -> `PDFMinerLoader`
2. Split -> `CharacterTextSplitter`
3. Embed -> `OpenAIEmbeddings(model='text-embedding-3-large')`
4. Index -> `FAISS.from_documents`
5. Retrieve -> `similarity_search(query, k=3)`
6. Prompt -> context + question
7. LLM -> `ChatOpenAI(model='gpt-4o-mini')`
8. Output -> answer + context dump

## Customization

- Change PDF: edit `PDF_PATH` in `main.py`
- Tune chunking: adjust `CHUNK_SIZE`, `CHUNK_OVERLAP`
- More/less context: change `k`
- Different models: swap embedding or chat model names
- Persist index: save/load FAISS instead of rebuilding

## Virtual Environment Note

The current `venv` includes many experimental packages not required for this prototype (installed during trial-and-error). To clean up:

```bash
pip freeze > full-freeze.txt   # archive bloated state (optional)
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install langchain langchain-community langchain-openai faiss-cpu python-dotenv
pip freeze > requirements.txt
```

Commit `requirements.txt`, never the `venv` directory.

## Planned Improvements

- Make chunks more context-aware as they perform poorly when asked about assessment dates
- Turn into a function that can take an course outline file as input
- Deploy so it can be tested by others

## Disclaimer

Prototype / experimental. Verify important answers against the source PDF