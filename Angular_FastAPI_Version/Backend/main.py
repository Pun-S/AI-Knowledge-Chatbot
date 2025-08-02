import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from document_loader import load_pdf, load_docx, load_txt, chunk_text
from embeddings_store import create_or_append_vector_store
from chat_logic import ask_bot, reset_memory

app = FastAPI()

origins = ["*"]  # Allow all for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open("temp_file", "wb") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        text = load_pdf("temp_file")
    elif file.filename.endswith(".docx"):
        text = load_docx("temp_file")
    elif file.filename.endswith(".txt"):
        text = load_txt("temp_file")
    else:
        return {"error": "Unsupported file type"}

    chunks = chunk_text(text)
    create_or_append_vector_store(chunks)

    return {"message": f"Document '{file.filename}' processed successfully"}

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    answer = ask_bot(query)
    return {"answer": answer}

@app.post("/reset")
async def reset():
    reset_memory()
    return {"message": "Conversation memory cleared"}