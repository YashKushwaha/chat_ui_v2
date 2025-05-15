from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

app = FastAPI()
app.state.request_log = []

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    template: str = None

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    app.state.request_log.append({
        "endpoint": "/chat",
        "data": payload.dict()
    })
    return {"response": "Mock chat response"}

@app.post("/generate")
async def generate_endpoint(request: Request):
    body = await request.json()
    app.state.request_log.append({
        "endpoint": "/generate",
        "data": body
    })
    return {"generated_text": "Mock generate output"}

@app.get("/log")
async def get_log():
    return app.state.request_log

@app.delete("/log")
async def clear_log():
    app.state.request_log.clear()
    return {"status": "cleared"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
