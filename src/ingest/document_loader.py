import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document



def load_all_pdfs(base_folder: str):
    """
    Recursively loads PDFs from subfolders inside base_folder.
    Adds folder name as metadata.
    """
    
    all_docs = []
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                category = os.path.basename(root)
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                # Add metadata like folder name and source
                for doc in docs:
                    doc.metadata["category"] = category
                    doc.metadata["source"] = file_path
                all_docs.extend(docs)
    
    return all_docs
