from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import os

# Set token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Load & split
loader = TextLoader("all_posts.json", encoding="utf-8")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = splitter.split_documents(docs)

# Embed & save
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(texts, embeddings)
vectorstore.save_local("faiss_index")

print("✅ Vectorstore built and saved to 'faiss_index/'")
