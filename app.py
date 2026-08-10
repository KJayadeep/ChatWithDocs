from dotenv import load_dotenv

load_dotenv()  

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import InMemoryVectorStore
import streamlit as st
from time import sleep


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def document_processing(path):
    loader = PyPDFLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    vector_store = InMemoryVectorStore.from_documents(documents=docs, embedding=embeddings)
    st.session_state.vector_store = vector_store

    st.session_state.document_uploded = True


st.subheader("Document Chatbot")

if "document_uploded" not in st.session_state:
    st.session_state.document_uploded = False

if not st.session_state.document_uploded:
    file = st.file_uploader(
        "Upload a PDF file",
        type=["pdf"],
        key="file_uploader"
    )

    if file:
        with open("uploaded_document.pdf", "wb") as f:
            f.write(file.getvalue())
        with st.spinner("Processing the document..."):
            document_processing("./uploaded_document.pdf")
        st.markdown("### Document processed successfully. You can now ask questions about the document.")
        
        st.success("File uploaded successfully.")
        sleep(2)
        st.rerun()

if st.session_state.document_uploded and st.session_state.vector_store:
    for oneMessage in st.session_state.messages:
        if oneMessage["role"] == "user":
            st.chat_message("user").markdown(oneMessage["content"])
        else:
            st.chat_message("assistant").markdown(oneMessage["content"])
            
    query = st.chat_input("Ask a question about the document:")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").markdown(query)
        documents = st.session_state.vector_store.similarity_search(query,k=2)
        context = ""

        for doc in documents:
            context += doc.page_content + "\n\n"

        prompt = f"""You are a helpful assistant and you provide accurate answers based on the given context. context: {context} question: {query}"""

        response = llm.invoke(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        st.chat_message("assistant").markdown(response.content)