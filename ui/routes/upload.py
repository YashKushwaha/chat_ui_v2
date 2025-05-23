import shutil
from pathlib import Path
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from llama_index.core import VectorStoreIndex

from fastapi import Request
from src.llama_index.embedder import get_embedding_model

from config_settings import UPLOAD_DIR
import os
import faiss
from src.llama_index.embedder import get_embedding_model
from src.llama_index.index import create_embeddings
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import Settings

embedding_model = get_embedding_model()
embedding_dim = len(embedding_model.get_text_embedding("dummy"))

#Settings.llm = None  # Important: prevents fallback to OpenAI
Settings.embed_model = embedding_model

def get_doc_id(file_path: str) -> str:
    """Generate unique ID (e.g., hash or slug) for a book."""
    return Path(file_path).stem.replace(" ", "_").lower()

def load_or_create_index(file_path: str) -> VectorStoreIndex:
    doc_id = get_doc_id(file_path)
    faiss_path = f"indices/{doc_id}.faiss"
    nodes_path = f"indices/{doc_id}_nodes.pkl"

    embedding_model = get_embedding_model()

    return 'Hi'

def process_uploaded_file(file_path: str) -> None:
    # 1. Load or create index for the uploaded file
    index = load_or_create_index(file_path)
    return index

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #out = process_uploaded_file(file_location)    
    return {"message": f"File '{file.filename}' uploaded successfully"}

@router.post("/add-to-context")
async def add_to_context(request: Request):
    data = await request.json()
    print(data['filename'])
    filename = os.path.join(UPLOAD_DIR, data['filename'])
    nodes = create_embeddings(filename, embedding_model)
    faiss_index = faiss.IndexFlatL2(embedding_dim)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    index = VectorStoreIndex(nodes=nodes, vector_store=vector_store)
    request.app.state.vector_store = index
    return "Success"

@router.route("/vector_store", methods=["GET"])
def vector_store(request):
    if hasattr(request.app.state, "vector_store"):
        index = request.app.state.vector_store
        num_docs = len(index.docstore.docs)
    else:
        num_docs = 0
    return JSONResponse(content=num_docs)


@router.route("/documents", methods=["GET"])
def list_documents(request):
    files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f)) and True] #f.endswith('.epub')
    return JSONResponse(content=files)

@router.delete("/documents/{filename}")
def delete_document(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    try:
        os.remove(file_path)
        return {"status": "success", "message": f"{filename} deleted"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))