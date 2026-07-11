#import fitz PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from docling.chunking import HybridChunker

from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc.document import PictureItem
from docling_core.types.doc.base import ImageRefMode


from typing import List, Dict, Any
import numpy as np
import pandas as pd
from PIL import Image
import os
from pathlib import Path



def get_docling_converter():
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True
    pipeline_options.generate_picture_images = True
    pipeline_options.do_ocr = True
    return DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

def extract_assets(pdf_path, converter):
    # Returns the 'Smart Object' (doc) and the 'Physical' Assets for S3
    result = converter.convert(pdf_path)
    
    doc = result.document.export_to_text()
    markdown = result.document.export_to_markdown()

    picture_counter = 0
    for element, _level in result.document.iterate_items():
        if isinstance(element, PictureItem):
            picture_counter += 1
            with open(f"picture-{picture_counter}.png", "wb") as fp:
                element.get_image(result.document).save(fp, "PNG")


    for table_ix, table in enumerate(result.document.tables):
        # Export to DataFrame
        df = table.export_to_dataframe(doc=result.document)
        df.to_csv(f"table-{table_ix}.csv")

        # Or access cell-level data
        for row in table.data.grid:
            for cell in row:
                print(cell.text)

    # Or save markdown with embedded images
    result.document.save_as_markdown("output.md", image_mode=ImageRefMode.EMBEDDED)
    return doc



### Chunking

def get_hierarchical_chunks(doc, file_id):
    chunker = HierarchicalChunker()
    chunk_iter = chunker.chunk(doc)
    
    db_chunks = []
    for chunk in chunk_iter:
        # serialize(chunk) includes text and Markdown tables together!
        db_chunks.append({
            "content": chunker.contextualize(chunk), 
            "metadata": {
                "category": None
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
    


#def metadata_tagging



if __name__ == "__main__":
    doc, assets = extract_assets(r"C:\Users\Ruthvik\Gov_Support_RAG_Chatbot\dataset\Policies\2024INFRA_MS21.pdf", get_docling_converter())
    print(doc)