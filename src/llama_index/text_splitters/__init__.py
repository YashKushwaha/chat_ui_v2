"""
from llama_index.core.node_parser import SentenceSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.node_parser import TextSplitterNodeParser
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.node_parser import LangchainNodeParser

def get_recursive_splitter_old(chunk_size=500, chunk_overlap=100):
    return SentenceSplitter(
            chunk_size=500,
            chunk_overlap=100)


def get_recursive_splitter_old(chunk_size=500, chunk_overlap=100):
    return SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        include_metadata=True,
        include_prev_next_rel=True,
        # Optional: force stricter splitting behavior
        secondary_chunking_regex=r"[^,.;。？！]+[,.;。？！]?|[,.;。？！]"
    )

def get_recursive_splitter(chunk_size=500, chunk_overlap=100):
    # Create a Langchain-style splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],  # Fallbacks for recursive splitting
    )

    # Wrap it in LlamaIndex's compatible node parser
    node_parser = LangchainNodeParser(text_splitter)

    return node_parser