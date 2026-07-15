from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://localhost:5178",
        "http://localhost:5180",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


class Question(BaseModel):
    question: str


@app.post("/chat")
def chat(q: Question):
    try:
        results = db.similarity_search(q.question, k=2)
        context = "\n".join([doc.page_content for doc in results])
        prompt = f"""Answer the question using only the context below.

Context:
{context}

Question:
{q.question}

Answer:"""
        response = llm.invoke(prompt)
        return {"answer": response.content}
    except Exception as e:
        return {"answer": f"Sorry, something went wrong: {str(e)}"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        save_path = f"../documents/{file.filename}"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        loader = PyPDFLoader(save_path)
        pages = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(pages)

        db.add_documents(chunks)

        return {"message": f"{file.filename} uploaded and indexed successfully"}
    except Exception as e:
        return {"message": f"Upload failed: {str(e)}"}


@app.get("/documents")
async def list_documents():
    docs = os.listdir("../documents")
    return {"documents": docs}


if __name__ == "__main__":
    print("RAG Chatbot running on http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)