from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

persist_directory = "db"
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")  # or "gpt-4o" if you want to try better results
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
