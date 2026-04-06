from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from docling.chunking import HierarchicalChunker



def get_hierarchical_chunks(doc, file_id):
    chunker = HierarchicalChunker()
    chunk_iter = chunker.chunk(doc)
    
    db_chunks = []
    for chunk in chunk_iter:
        # serialize(chunk) includes text and Markdown tables together!
        db_chunks.append({
            "content": chunker.serialize(chunk), 
            "metadata": {
                "file_id": file_id,
                "headings": chunk.meta.headings,
                "pages": [p.page_no for p in chunk.meta.doc_items.prov] if chunk.meta.doc_items else []
            }
        })
    return db_chunks



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

