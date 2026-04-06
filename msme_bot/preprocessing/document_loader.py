#import fitz PyMuPDF
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_core.documents import Document
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



#def load_images

#docling



### Cleaning and Preprocessing

def remove_redundant_text():
    """removes unneccesary text"""
    try:
        pass
    except:
        pass