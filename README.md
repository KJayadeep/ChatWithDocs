# 📄 RAG — Document Chatbot

A simple Retrieval-Augmented Generation (RAG) chatbot that lets you **upload a PDF and ask questions about it**. Built with [LangChain](https://www.langchain.com/), [Google Gemini](https://ai.google.dev/), and [Streamlit](https://streamlit.io/).

## How It Works

1. Upload a PDF document through the Streamlit interface.
2. The document is split into chunks and converted into embeddings using Google's Gemini embedding model.
3. The chunks are stored in an in-memory vector store.
4. When you ask a question, the most relevant chunks are retrieved and passed to Gemini 2.5 Flash to generate a context-aware answer.

## Tech Stack

- **LangChain** — document loading, text splitting, and orchestration
- **Google Generative AI (Gemini)** — embeddings and chat responses
- **Streamlit** — interactive web UI
- **In-memory vector store** — for similarity search

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/KJayadeep/RAG.git
cd RAG
```

### 2. Install dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the project root and add your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

You can get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 4. Run the app

```bash
streamlit run app.py
```

The app will open in your browser. Upload a PDF, wait for it to process, and start asking questions.

## Project Structure

```
RAG/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example         # Example environment file
└── .gitignore
```

## Notes

- Currently supports one PDF document per session.
- The vector store is in-memory, so uploaded documents are not saved between sessions.

## License

This project is open source and available under the [MIT License](LICENSE).