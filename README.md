# OutlineQuery: A Waterloo Course Outline Chatbot

OutlineQuery is a simple web application built with Streamlit that allows users to upload a University of Waterloo course outline in HTML format and ask questions about its content.

**Live Demo:** [https://outlinequery.streamlit.app/](https://outlinequery.streamlit.app/)

## How it Works

The application follows a straightforward process:

1.  **File Upload**: The user uploads a course outline as an HTML file.
2.  **In-Memory Processing**: The file is read directly into memory, avoiding the need for temporary files on disk.
3.  **Parsing & Chunking**: The HTML content is parsed to extract meaningful sections, which are then broken down into smaller, manageable chunks for processing.
4.  **Question Answering**: The user submits a question through a form. This query is used along with the document chunks to find the most relevant answer.
5.  **Display Answer**: The generated answer is displayed to the user.

## Project Structure

```
.
├── src
│   ├── st_dash.py         # Main Streamlit application script
│   ├── chunking.py        # Handles parsing and chunking of the HTML document
│   └── qa.py              # Contains the question-answering logic
└── README.md
```

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd data_docx
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file should be created containing libraries like `streamlit`, etc.)*

3.  **Run the application:**
    ```bash
    streamlit run src/st_dash.py
    ```

4.  **Use the application:**
    -   Open your web browser and navigate to the local URL provided by Streamlit.
    -   Use the file uploader to select your HTML course outline.
    -   Once the file is uploaded, type your question into the text box and click "Get answer".