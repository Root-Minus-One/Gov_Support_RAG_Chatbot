from langchain_core.documents import Document

from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc.document import PictureItem
from docling_core.types.doc.base import ImageRefMode
from transformers import AutoTokenizer

from io import BytesIO
from PIL import Image
from bson.binary import Binary
from pathlib import Path
from loguru import logger
import asyncio
from typing import List, Dict, Any

from app.utils.helper import get_page_number
from app.db.postgres import get_pool
from app.db.mongo import get_db


def extract_metadata(pdf_file) -> dict:
    metadata = {}
    file_path = Path(pdf_file)
    metadata["file_name"] = file_path.name
    metadata["category"] = file_path.parent.name
    metadata["document_title"] = file_path.stem

    return metadata


async def save_document(metadata, total_pages, pool):
    try:
        async with pool.acquire() as conn:
            insert_query = "INSERT INTO documents (file_name, document_title, category, total_pages) " \
            "VALUES ($1, $2, $3, $4) " \
            "RETURNING doc_id;"
                    
            doc_id = await conn.fetchval(insert_query, metadata["file_name"],
                                                       metadata["document_title"],
                                                       metadata["category"], 
                                                       total_pages
                                                    )

            return doc_id
    
    except Exception as e:
        logger.error(e)
        raise


def get_docling_converter():
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True
    pipeline_options.generate_picture_images = True
    pipeline_options.do_ocr = True
    return DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )


async def extract_save_text(doc_id, result):
    # chunks the document text  
    pool = get_pool()
    try:
        chunks = get_hybrid_chunks(result=result)
        # #inserts many rows into chunks  

        records = [
            (
                doc_id,
                chunks[i]["chunk_index"],
                chunks[i]["chunk_text"],
                chunks[i]["char_count"],
                chunks[i]["page_number"]
            )
            for i in range(len(chunks))
        ]

        async with pool.acquire() as conn:
            insert_query = "INSERT INTO chunks (doc_id, page_number, chunk_index, chunk_text, char_count)" \
            "VALUES ($1, $2, $3, $4, $5);"

            await conn.executemany(insert_query, records)
            
            logger.info(f"Saved {len(records)} chunks for doc_id {doc_id}")

    except Exception as e:
        logger.error(f"Failed to save chunks for doc_id {doc_id}: {e}")
        raise



async def extract_save_images(doc_id, result):
    db = get_db()

    collection = db[IMAGES_COLLECTION_NAME]
    image_counter = 0

    try:
        loop = asyncio._get_running_loop()

        def _convert_to_bytes(image):
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer.read()
        

        for element, _level in result.document.iterate_items():
            if isinstance(element, PictureItem):
                image_counter += 1
                pil_image = element.get_image(result.document)
                image_bytes = await loop.run_in_executor(None, _convert_to_bytes, pil_image)
                bson_image = Binary(image_bytes)

                page_number = get_page_number(element)
                
                await collection.insert_one({
                    "doc_id": str(doc_id),
                    "image_index": image_counter,
                    "image_data": bson_image,
                    "page_number": page_number
                    })
        logger.info(f"Saved {image_counter} images for doc_id {doc_id}")

    except Exception as e:
        logger.error(f"failed to save images {e}")
        raise



async def extract_save_tables(doc_id, result):
    db = get_db()

    collection = db[TABLES_COLLECTION_NAME]

    try:
        loop = asyncio._get_running_loop()

        for table_ix, table in enumerate(result.document.tables):
            df = table.export_to_dataframe(doc=result.document)
            
            page_number = get_page_number(table)
            
            await collection.insert_one({
                "doc_id": str(doc_id),
                "table_index": table_ix,
                "table_data": df.to_dict(orient="records"),
                "page_number": page_number
                })
        logger.info(f"Saved {table_ix + 1} tables for doc_id {doc_id}")

        
    except Exception as e:
        logger.error(f"failed to save tables {e}")
        raise    


        # Or access cell-level data
        for row in table.data.grid:
            for cell in row:
                print(cell.text)






### Chunking
_tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
_chunker = HybridChunker(tokenizer=_tokenizer)

def get_hybrid_chunks(result) -> list[dict]:
        
    chunks_iter = _chunker.chunk(result.document) 
    
    chunks_list = []

    for index, chunk in enumerate(chunks_iter):
        page_number = 1

        if chunk.meta.doc_items:
            first_item = chunk.meta.doc_items[0]

            get_page_number(first_item)
            
            # if hasattr(first_item, "prov") and first_item.prov:
            #     page_number = first_item.prov[0].page_no if first_item.prov else 1
        
        chunks_list.append({
            "chunk_index": index,
            "chunk_text": chunk.text,
            "char_count": len(chunk.text),
            "page_number": page_number
        })
    return chunks_list 



async def ingest_file(file_path):
    try:
        logger.info(f"Starting ingestion for {file_path}")

        converter = get_docling_converter()

        metadata = extract_metadata(file_path)

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, converter.convert, file_path)
        total_pages = len(result.document.pages)

        doc_id = await save_document(metadata=metadata, total_pages=total_pages, pool=get_pool())


        await asyncio.gather(
            extract_save_text(doc_id, result),
            extract_save_images(doc_id, result),
            extract_save_tables(doc_id, result)
        )
        logger.info(f"Completed ingestion for {file_path} - doc_id: {doc_id}")
    
    except Exception as e:
        logger.error(f"Ingestion failed for file: {file_path}: {e}")
        raise


async def ingest_folder(folder_path):

    all_files = list(Path(folder_path).rglob("*.pdf"))
    logger.info(f" Found {len(all_files)} PDFs at {folder_path}")

    
    for file in all_files:
        try:
            await ingest_file(file)
        except Exception as e:
            logger.error(f"Failed to process PDF: {file}")
            continue

  





if __name__ == "__main__":
    pass