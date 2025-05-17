import shutil
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from config_settings import UPLOAD_DIR
import os
router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": f"File '{file.filename}' uploaded successfully"}

@router.route("/documents", methods=["GET"])
def list_documents(request):
    files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
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