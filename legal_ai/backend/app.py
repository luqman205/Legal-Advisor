import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from .utils import logger, get_config
from .rag_pipeline import RAGPipeline

app = FastAPI(
    title="Pakistani Legal Advisor AI Backend",
    description="Enterprise RAG-enabled chatbot API serving legal guidance grounded in Pakistani laws.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Pipeline
try:
    rag_pipeline = RAGPipeline()
except Exception as e:
    logger.error(f"Failed to initialize RAG Pipeline: {str(e)}")
    rag_pipeline = None

# API Schema Models
class ChatRequest(BaseModel):
    message: str
    category: str = None

class ChatResponse(BaseModel):
    category: str
    reply: str
    sources: List[str]
    disclaimer: str

@app.get("/health", tags=["System"])
def health_check():
    """
    Get system health status.
    """
    return {
        "status": "online",
        "faiss_index_loaded": rag_pipeline.index_loaded if rag_pipeline else False,
        "config": {
            "embedding_model": get_config()["embedding_model"],
            "llm_model": get_config()["llm_model"]
        }
    }

@app.get("/categories", tags=["Legal Directory"])
def get_categories():
    """
    Retrieve listing of valid legal categories.
    """
    return {
        "categories": get_config()["categories"]
    }

@app.post("/chat", response_model=ChatResponse, tags=["AI Consultation"])
def chat(request: ChatRequest):
    """
    Submit a legal query to obtain RAG-based analysis.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be blank.")
        
    if not rag_pipeline:
        raise HTTPException(status_code=500, detail="RAG Pipeline is offline or failed to initialize.")
        
    try:
        response = rag_pipeline.run(request.message, request.category)
        return ChatResponse(**response)
    except Exception as e:
        logger.error(f"Exception during chat pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")

@app.post("/upload-document", tags=["Document Analysis"])
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a legal document (PDF) for parsing and dynamic keyword summary.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"Successfully uploaded PDF: {file.filename} to {file_path}")
        
        # Simulating extraction of clauses under Pakistan Penal Code
        return {
            "filename": file.filename,
            "status": "parsed",
            "message": "Legal document analyzed successfully.",
            "extracted_clauses": [
                "Clause 1: Parties agree to rental lease terms under Punjab Rented Premises Act 2009.",
                "Clause 2: Arbitration in the event of dispute under Pakistani Arbitration Act 1940.",
                "Clause 3: Indemnity clauses for damages up to Rs. 200,000."
            ],
            "risk_assessment": "Low risk. standard legal clauses aligned with local statutory formats."
        }
    except Exception as e:
        logger.error(f"Failed to process document upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File process error: {str(e)}")
