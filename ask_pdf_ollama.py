
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader

# ---- Load environment variables ----
load_dotenv()

# ---- Streamlit UI ----
st.title("PDF Q&A with Ollama (Deepseek R1)")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
user_query = st.text_input("Enter your question:")

if uploaded_file and user_query:
    with st.spinner("Processing PDF and answering your question..."):
        # ---- Load and parse PDF ----
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        loader = PyMuPDFLoader(
            file_path="temp.pdf",
            mode="single",
            pages_delimiter=",",
            extract_images=True,
            extract_tables="markdown"
        )
        docs = loader.load()

        # ---- Split text into chunks ----
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = splitter.split_documents(docs)

        # ---- Embed and store in Chroma ----
        embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory="./deepseek_chroma"
        )

        # ---- Search relevant documents ----
        relevant_docs = vectorstore.similarity_search(user_query, k=4)
        if not relevant_docs:
            st.warning("No relevant documents found.")
        else:
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            # ---- Query using Ollama LLM (Deepseek R1) ----
            try:
                llm = OllamaLLM(model="deepseek-r1")
                prompt = f"""You are an expert assistant.\nAnswer the following based on this context:\n{context}\n\nQuestion: {user_query}"""
                answer = llm.invoke(prompt)
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"LLM call failed: {str(e)}")
