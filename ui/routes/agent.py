from pydantic import BaseModel
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from agents.query_router_agent import QueryRouterAgent


router = APIRouter()

@router.post("/agent")
def agent(request: Request, query: QueryRequest):
    llm = request.app.state.llm
    agent = QueryRouterAgent(llm=llm)
    response = agent.run(user_query=query.message)
    return JSONResponse(content={"response": response})
