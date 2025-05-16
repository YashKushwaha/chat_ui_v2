from llama_index.core.node_parser import SentenceSplitter

def get_recursive_splitter(chunk_size=500, chunk_overlap=100):
    return SentenceSplitter(
            chunk_size=500,
            chunk_overlap=100)