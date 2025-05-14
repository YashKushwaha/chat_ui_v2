import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

import os

def epub_to_text(file_path):
    book = epub.read_epub(file_path)
    text = ''
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text += soup.get_text() + '\n'
    return text


if __name__ == '__main__':
    print()
    file = os.path.join(os.getcwd(), 'uploads', 'precious-little-sleep.epub')
    text = epub_to_text(file)

    print(len(text))

    print(text[:1000])