from langchain_huggingface import HuggingFaceEmbeddings  # ✅ recommended
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

with open("all_posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = [d["content"] for d in data]
metadatas = [{"source": d.get("url", "")} for d in data]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.create_documents(documents, metadatas=metadatas)

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # now from new package

vectorstore = Chroma.from_documents(docs, embedding=embedding, persist_directory="db")
