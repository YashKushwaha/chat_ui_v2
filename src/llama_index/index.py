import os
import pickle
from pathlib import Path
#from llama_index.llms import OllamaModel
from loaders.epub_loader import EPUBLoader
from text_splitters import get_recursive_splitter
from embedder import get_embedding_model

import faiss
import numpy as np
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core.query_engine import RetrieverQueryEngine

def create_embeddings(file_path, embedding_model):
    
    loader = EPUBLoader(file_path)
    docs = loader.load()

    splitter = get_recursive_splitter()
    nodes = splitter.get_nodes_from_documents(docs)
    print('Len docs -> ', len(docs))
    print('Len nodes -> ', len(nodes))  
    texts = [node.get_content() for node in nodes]
    embeddings = embedding_model.get_text_embedding_batch(texts)

    # Step 5: Attach embeddings back to nodes
    for node, embedding in zip(nodes, embeddings):
        node.embedding = embedding

    # Done: `nodes` are now ready for vector DB insertion or further RAG pipeline steps
    print(f"Embedded {len(nodes)} nodes using GPU.")
    return nodes

def create_empty_vec_db(embedding_dim, save_path = "empty_faiss.idx"):
    # Create empty FAISS index
    faiss_index = faiss.IndexFlatL2(embedding_dim)

    # Initialize vector store
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # Create empty index (no nodes yet)
    index = VectorStoreIndex(nodes=[], vector_store=vector_store)
    faiss.write_index(faiss_index, save_path)
    return index

def load_existing_index(faiss_index_path, nodes_path):
    print("🔁 Loading existing FAISS index and nodes...")
    faiss_index = faiss.read_index(faiss_index_path)

    with open(nodes_path, "rb") as f:
        nodes = pickle.load(f)

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    index = VectorStoreIndex(nodes=nodes, vector_store=vector_store)

    return vector_store, index


embedding_model = get_embedding_model()
embedding_dim = len(embedding_model.get_text_embedding("dummy"))

if __name__ == '__main__':
    file_path = '/mnt/f/chat_ui_v2/uploads/precious-little-sleep.epub'
    faiss_index_path = file_path.replace('.epub', '.idx')
    nodes_path = file_path.replace('.epub', '_nodes.pkl')
    Settings.llm = None  # Important: prevents fallback to OpenAI
    Settings.embed_model = embedding_model

    if Path(faiss_index_path).exists() and Path(nodes_path).exists():
        print('faiss_index_path & nodes_path exist')
        vector_store, index = load_existing_index(faiss_index_path, nodes_path)
    else:
        print('Creating faiss_index_path & nodes_path')
        faiss_index = faiss.IndexFlatL2(embedding_dim)
        vector_store = FaissVectorStore(faiss_index=faiss_index)

        nodes = create_embeddings(file_path, embedding_model)
        index = VectorStoreIndex(nodes=nodes, vector_store=vector_store)
        faiss.write_index(faiss_index, faiss_index_path)

        # Save nodes
        with open(nodes_path, "wb") as f:
            pickle.dump(nodes, f)
    

    retriever = index.as_retriever(similarity_top_k=5)
    query_engine = RetrieverQueryEngine(retriever=retriever) 

    query = "What's this document about?"
    results = query_engine.query(query)
    print('====Results======')
    print(results)
    print('====<Results>======')
    nodes = retriever.retrieve(query)
    print('===Nodes')
    for node in nodes:
        content = node.get_content() 
        print(len(content))
        print(10*'=')