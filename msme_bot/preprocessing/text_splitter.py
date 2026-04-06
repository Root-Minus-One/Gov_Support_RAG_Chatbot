from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


def doc_text_splitter(doc_list: List[Document], chunk_size: int, chunk_overlap: int):
    """splits text by paragraphs and sentences"""
    try:
        text_chunker = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
        chunks = text_chunker.split_documents(doc_list)
        
        return chunks
    
    except:
        pass
    

def other_text_chunking(doc_list: List[Document]):
    """other chunking method"""
    try:
        pass
    except:
        pass



#def metadata_tagging

