# pdf_Q&A_cleaned.py
import os
import streamlit as st
from dotenv import load_dotenv
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_community.document_loaders import PyMuPDFLoader
from openai import OpenAI

# ---- Load environment variables ----
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    st.error("DEEPSEEK_API_KEY not found in environment. Please check your .env file.")

# ---- Streamlit UI ----
st.title("PDF Q&A with DeepSeek")
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

            # ---- Query DeepSeek using OpenAI client ----
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                messages = [
                    {"role": "system", "content": "You are an expert assistant."},
                    {"role": "user", "content": f"Answer the following based on this context:\n{context}\n\nQuestion: {user_query}"}
                ]
                response = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=messages
                )
                answer = response.choices[0].message.content
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"API call failed: {str(e)}")
