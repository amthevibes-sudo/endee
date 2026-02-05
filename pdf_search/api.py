
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import uvicorn
import json

from search_engine import SemanticSearchEngine
from config import Config


app = FastAPI(title="PDF Semantic Search API")

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Search Engine
engine = SemanticSearchEngine()

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5
    file_filter: Optional[str] = None

class SearchResult(BaseModel):
    id: str
    score: float
    metadata: Dict[str, Any]

@app.get("/api/health")
def health_check():
    return {"status": "ok", "engine_initialized": True}

@app.get("/api/info")
def get_info():
    info = engine.get_index_info()
    if not info:
        return {"total_chunks": 0, "files": {}, "message": "No index found"}
    return info

@app.post("/api/search", response_model=List[SearchResult])
def search(query: SearchQuery):
    try:
        results = engine.search(
            query=query.query,
            top_k=query.top_k,
            filter_by_file=query.file_filter
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        if not Config.PDF_DIR.exists():
            Config.PDF_DIR.mkdir(parents=True)
            
        print(f"DEBUG: Received {len(files)} files for upload")
        saved_files = []
        for file in files:
            print(f"DEBUG: Processing file: {file.filename}")
            file_path = Config.PDF_DIR / file.filename
            with open(file_path, "wb") as buffer:
                content = await file.read()
                print(f"DEBUG: Read {len(content)} bytes from {file.filename}")
                buffer.write(content)
            saved_files.append(file_path)
            
        # Trigger ingestion only for the newly uploaded files
        print("DEBUG: Initializing engine for ingestion")
        engine.initialize()
        process_success = True
        error_messages = []
        for file_path in saved_files:
            print(f"DEBUG: Ingesting file: {file_path}")
            success, message = engine.ingest_pdfs(file_path)
            if not success:
                print(f"DEBUG: Ingestion failed for {file_path}: {message}")
                process_success = False
                error_messages.append(f"{file_path.name}: {message}")
            else:
                print(f"DEBUG: Ingestion success for {file_path}")
        
        if process_success:
            info = engine.get_index_info()
            return {
                "status": "success", 
                "message": f"Uploaded and indexed {len(files)} files",
                "total_chunks": info.get("total_chunks", 0)
            }
        else:
            return {"status": "error", "message": f"Processing failed: {'; '.join(error_messages)}"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingest")
def ingest(pdf_dir: Optional[str] = None):
    try:
        # Initialize if not already done
        engine.initialize()
        
        pdf_path = Path(pdf_dir) if pdf_dir else Config.PDF_DIR
        success = engine.ingest_pdfs(pdf_path)
        
        if success:
            return {"status": "success", "message": "Ingestion completed"}
        else:
            return {"status": "error", "message": "Ingestion failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
def reset():
    if engine.reset_index():
        return {"status": "success", "message": "Index reset"}
    else:
        return {"status": "error", "message": "Reset failed"}

# Serve React static files (only if building as a monolith)
# In Hybrid mode (Vercel + Render), this part is skipped or optional.
if Path("frontend/dist").exists():
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
else:
    print("INFO: Frontend dist not found. Running in API-only mode (Hybrid deployment).")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
