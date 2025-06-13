from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Load vector store (example)
embedding = HuggingFaceEmbeddings()
vectordb = Chroma(persist_directory="db", embedding_function=embedding)

retriever = vectordb.as_retriever(search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=retriever
)

def answer_question(question, image_text=""):
    full_query = question + "\n" + image_text
    result = qa_chain(full_query)
    return result['result'], []
