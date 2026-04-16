#import fitz PyMuPDF
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_core.documents import Document

from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

from typing import List, Dict, Any
import numpy as np
from PIL import Image
import os



def load_pdf_file(file_path): 
    """Extracts text from .pdf files"""
    try:
        pdf_contents = PyPDFLoader(file_path)
        
        return pdf_contents
    except:
         pass


def load_documents_from_directory(directory_path) -> List[Document]: 
    """ Iterates through a directory, loads pdf files and returns a list of Document objects"""
    
    try:
        if not os.path.isdir(directory_path):
            print(f"Error: The directory '{directory_path}' does not exist.")
            return []
        
        directory_contents : List[Document] = []
        
        pdf_loader = PyPDFDirectoryLoader(directory_path)
        
        directory_contents = pdf_loader.load()
        
        return directory_contents
    except:
        pass



def get_docling_converter():
    options = PdfPipelineOptions()
    options.do_table_structure = True
    options.generate_picture_images = True
    options.do_ocr = True
    return DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)}
    )

def extract_assets(pdf_path, converter):
    # Returns the 'Smart Object' (doc) and the 'Physical' Assets for S3
    result = converter.convert(pdf_path)
    doc = result.document
    
    physical_assets = {
        "tables": [],
        "images": []
    }

    # Prepare raw table data for S3/CSV storage
    for table in doc.tables:
        physical_assets["tables"].append({
            "df": table.export_to_dataframe(),
            "page": table.prov[0].page_no if table.prov else None
        })

    # Prepare raw image files for S3 storage
    for i, img in enumerate(doc.pictures):
        if img.image:
            physical_assets["images"].append({
                "pil": img.image.pil_image,
                "name": f"image_{i}.png",
                "page": img.prov[0].page_no if img.prov else None
            })
            
    return doc, physical_assets




### Cleaning and Preprocessing

def remove_redundant_text():
    """removes unneccesary text"""
    try:
        pass
    except:
        pass

    

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

