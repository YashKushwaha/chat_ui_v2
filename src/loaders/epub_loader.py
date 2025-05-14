from langchain.schema import Document
from langchain.document_loaders.base import BaseLoader

from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib

class EPUBLoader(BaseLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _extract_epub_with_metadata(self):
        book = epub.read_epub(self.file_path)
        chapters = []
        current_text = []  # List to store paragraphs across documents
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                
                # Extract title (if present)
                title = (soup.find('h1') or soup.find('h2') or soup.title)
                title_text = title.get_text(separator=' ', strip=True) if title else "Untitled Section"
                
                # Extract paragraphs and clean text
                paragraphs = [
                    p.get_text(separator=' ', strip=True).replace('\xa0', ' ') 
                    for p in soup.find_all('p') if p.get_text(strip=True)
                ]
                
                # Append the extracted paragraphs from this document to the current text
                current_text.extend(paragraphs)

                # Append the chapter information, preserving the text order
                chapters.append({
                    'title': title_text,
                    'content': paragraphs
                })

        # Merge all paragraphs from the documents to maintain continuity
        full_text = ' '.join(current_text)
        
        return chapters, full_text


    def load(self):
        documents = []
        chapters = self._extract_epub_with_metadata()
        for chapter in chapters:
            title = chapter['title']
            content = chapter['content']

            for i in range(0, len(content), 3):  # group paragraphs
                chunk_text = " ".join(content[i:i+3])
                metadata = {
                    "chapter_title": title,
                    "source": self.file_path
                }
                documents.append(Document(page_content=chunk_text, metadata=metadata))
        return documents
