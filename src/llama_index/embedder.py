import os
import torch

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

os.environ['HF_HOME'] = '/mnt/c/Users/Yash/.cache/huggingface'

device = "cuda" if torch.cuda.is_available() else "cpu"

def get_embedding_model():
    embedding_model = HuggingFaceEmbedding(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        cache_folder = '/mnt/c/Users/Yash/.cache/huggingface/hub',
        embed_batch_size = 64,
        device = 'cuda')
    return embedding_model