# AI Document Analyst

An AI-powered document analysis application that allows users to upload PDF documents and ask questions about their contents.

The project combines semantic retrieval using sentence embeddings, a local Large Language Model (LLM), and deterministic Python analysis to provide grounded answers while reducing the risk of incorrect numerical reasoning.

## Features

- Upload and analyse PDF documents through a Streamlit interface
- Ask natural-language questions about document content
- Extract text while preserving page information
- Split documents into page-aware text chunks
- Generate semantic embeddings using Sentence Transformers
- Retrieve relevant document sections using cosine similarity
- Generate grounded answers using a local Ollama LLM
- Display retrieved evidence, page numbers, and similarity scores
- Extract structured property information from PDF content
- Perform deterministic highest and lowest rent calculations
- Extract dashboard statistics such as students, properties, appointments, and landlords
- Route structured numerical questions through Python instead of relying on the LLM
- Support multiple natural-language variations for dashboard count questions
- Automatically test structured extraction and calculations using pytest

## Why Hybrid Analysis?

Large Language Models can struggle with structured information extracted from PDFs, particularly when tables, dashboard layouts, or visual relationships are flattened into plain text.

This project therefore uses a hybrid approach.

Structured questions, such as:

- "Which property has the highest rent?"
- "Which property has the lowest rent?"
- "How many students are shown in the dashboard?"
- "What is the total number of landlords?"

are handled using deterministic Python analysis.

General document questions, such as:

- "What university is mentioned in the document?"
- "What is this document about?"

are handled using semantic retrieval and a local LLM.

This approach combines the flexibility of Retrieval-Augmented Generation (RAG) with the reliability of deterministic analysis for structured data.

## Architecture

```text
PDF Upload
    |
    v
Text Extraction
    |
    +--------------------------+
    |                          |
    v                          v
Structured Extraction      Page-Aware Chunking
    |                          |
    v                          v
Python Analysis           Sentence Embeddings
    |                          |
    |                          v
    |                    Cosine Similarity
    |                          |
    |                          v
    |                   Relevant Chunks
    |                          |
    |                          v
    |                     Ollama LLM
    |                          |
    +------------+-------------+
                 |
                 v
        Answer + Evidence
```

## Technologies

- Python
- PyMuPDF
- Sentence Transformers
- scikit-learn
- Ollama
- Llama 3.2
- Streamlit
- pytest

## Project Structure

```text
ai-document-analyst/
│
├── app/
│   ├── embeddings.py
│   ├── pdf_reader.py
│   ├── rag.py
│   ├── retriever.py
│   ├── table_reader.py
│   ├── text_chunker.py
│   └── ui.py
│
├── data/
│   └── sample.pdf
│
├── tests/
│   └── test_table_reader.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Testing

The project includes automated tests for structured document analysis.

Run the test suite with:

```bash
pytest -v
```

The tests currently verify:

- Dashboard metric extraction
- Highest-rent property identification
- Lowest-rent property identification

## Running the Application

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama and make sure the required local model is available:

```bash
ollama pull llama3.2:3b
```

Start the application:

```bash
streamlit run app/ui.py
```

Then upload a PDF and ask questions through the web interface.

## Current Limitations

- Structured extraction currently depends on document-specific patterns.
- Semantic embeddings are recalculated when questions are processed rather than being persisted in a vector database.
- The local LLM can still produce incorrect answers when document structure is ambiguous, which is why structured numerical questions are routed through deterministic Python logic.
- The application currently focuses on PDF documents.
- The project has not yet been containerised or deployed to a cloud environment.

## Future Improvements

Planned improvements include:

- Persistent vector storage
- Improved document-independent table extraction
- Additional automated RAG evaluation
- FastAPI backend
- Docker containerisation
- Cloud deployment
- Support for additional document formats

## Purpose

This project was developed as a portfolio project to explore practical AI document analysis, Retrieval-Augmented Generation, structured data extraction, local LLM integration, and reliable AI application design.
