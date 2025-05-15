import os
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return "Hello, World!"

if __name__ == "__main__":
    import uvicorn
    app_path = Path(__file__).resolve().with_suffix('').name  # gets filename without .py
    uvicorn.run(f"{app_path}:app", host="0.0.0.0", port=8000, reload=True)
