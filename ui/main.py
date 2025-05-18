import os
from pathlib import Path
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from ui.config_settings import *
from ui.routes import upload, chat

from src.llama_index.llms import OllamaModel

class QueryRequest(BaseModel):
    message: str

app = FastAPI()
app.include_router(upload.router)
app.include_router(chat.router)

# Static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

@app.post("/echo")
async def echo(request: QueryRequest):
    print('User input received -> ', request.message)
    return {"response": request.message}

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("base.html", {
        "request": request,
        "chat_endpoint": "/chat"
    })

model = 'phi4'
url = 'http://localhost:11434/api/generate'

llm_config = dict(model=model, url=url)

app.state.llm = OllamaModel(llm_config)


if __name__ == "__main__":
    import uvicorn
    app_path = Path(__file__).resolve().with_suffix('').name  # gets filename without .py
    uvicorn.run(f"{app_path}:app", host="0.0.0.0", port=8000, reload=True)
