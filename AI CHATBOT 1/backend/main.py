from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
from rag_engine import RAGEngine

app = FastAPI(title="Enterprise AI Chatbot API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

rag = RAGEngine()

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    answer: str

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        rag.add_document(file_path)
        return {"message": f"Successfully uploaded and indexed {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_bot(request: QueryRequest):
    try:
        answer = rag.query(request.prompt)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_db():
    rag.reset_collection()
    # Also clear upload folder
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    return {"message": "Database and uploads reset successfully."}

@app.get("/")
async def serve_index():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "online", "model": rag.model_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
