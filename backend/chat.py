from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama 
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the DB we created
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Load Ollama model - make sure Ollama is running with: ollama run llama3
llm = ChatOllama(model="gemma2:2b") 

question = "What is in the document?"

# Search the database
docs = db.similarity_search(question, k=2)

# Combine the retrieved text
context = "\n\n".join(doc.page_content for doc in docs)

# Get answer
response = llm.invoke(f"Context: {context}\n\nQuestion: {question}")
print(response.content)