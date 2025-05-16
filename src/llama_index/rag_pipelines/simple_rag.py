from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine

def simple_rag_pipeline(index: VectorStoreIndex, query: str, service_context=None) -> str:
    query_engine = RetrieverQueryEngine.from_args(index.as_retriever(), service_context=service_context)
    response = query_engine.query(query)
    return str(response)
