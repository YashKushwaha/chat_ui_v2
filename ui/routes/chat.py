from pydantic import BaseModel
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from src.llama_index.rag_pipelines.simple_rag import  simple_rag_pipeline, simple_llm_call
#generate_answer, simple_llm_call,
from llama_index.core.query_engine import RetrieverQueryEngine


class QueryRequest(BaseModel):
    message: str

router = APIRouter()

@router.post("/chat")
def chat(request: Request, query: QueryRequest):
    llm = request.app.state.llm
    if hasattr(request.app.state, "vector_store"):
        index = request.app.state.vector_store
        retriever = index.as_retriever(similarity_top_k=3)
        query_engine = RetrieverQueryEngine(retriever=retriever) 
        results = query_engine.query(query.message)
        print(type(results))
        print(dir(results))
        print(results)
        response = results.response
    else:
        response = query.message
        """
        response = simple_llm_call(
            question=query.message,
            llm=llm,
            stream=False)
        """
    return JSONResponse(content={"response": response})

