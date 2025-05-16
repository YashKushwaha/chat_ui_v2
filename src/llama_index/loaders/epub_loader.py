import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from llama_index.core.schema import Document  # ✅ LlamaIndex's Document
from uuid import uuid4

class EPUBLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _extract_epub_with_metadata(self):
        book = epub.read_epub(self.file_path)
        chapters = []

        chapter_index = 0
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')

                title = (soup.find('h1') or soup.find('h2') or soup.title)
                title_text = title.get_text(separator=' ', strip=True) if title else f"Chapter {chapter_index + 1}"

                body = soup.body
                raw_text = (
                    body.get_text(separator=' ', strip=True).replace('\xa0', ' ')
                    if body else soup.get_text(separator=' ', strip=True).replace('\xa0', ' ')
                )

                if raw_text:
                    chapters.append(Document(
                        id_=str(uuid4()), 
                        text=raw_text,
                        metadata={
                            'source': self.file_path,
                            'chapter_title': title_text,
                            'chapter_index': chapter_index
                        }
                    ))
                    chapter_index += 1

        return chapters

    def load(self):
        return self._extract_epub_with_metadata()
