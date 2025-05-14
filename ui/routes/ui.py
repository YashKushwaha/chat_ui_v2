from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config.settings import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {
        "request": request,
        "chat_endpoint": "/chat"
    })

@router.get("/test", response_class=HTMLResponse)
async def testing_ui(request: Request):
    return templates.TemplateResponse("base.html", {
        "request": request,
        "chat_endpoint": "/test"
    })

@router.get("/agent", response_class=HTMLResponse)
async def agent(request: Request):
    return templates.TemplateResponse("base.html", {
        "request": request,
        "chat_endpoint": "/agent"
    })
