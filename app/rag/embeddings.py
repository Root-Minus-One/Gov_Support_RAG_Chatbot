from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from loguru import logger

from typing import List
import asyncio
import functools

from app.core.config import settings
from app.db.postgres import get_pool
from app.db.mongo import get_db


_embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)



async def embed_texts(texts: list[str]) -> list[list[float]]:
    loop = asyncio.get_running_loop()

    encode_fn = functools.partial(_embedding_model.encode, batch_size=32)

    embeddings = await loop.run_in_executor(None, encode_fn, texts)

    return embeddings.tolist()

    
try:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY.get_secret_value())
    index = pc.Index(settings.PINECONE_INDEX_NAME)
except Exception as e:
    logger.error(f"Failed to initialise Vector Index: {e}")
    raise

async def run_embedding_pipeline():
    try:
        pool = get_pool()
        async with pool.acquire() as conn:

            select_query = "SELECT c.chunk_id, c.chunk_text, c.doc_id, d.category, d.document_title " \
            "FROM chunks c " \
            "JOIN documents d ON c.doc_id = d.doc_id " \
            "WHERE c.is_embedded = FALSE"
            
            update_query = "UPDATE chunks SET is_embedded = TRUE WHERE chunk_id = $1"

            results = await conn.fetch(select_query)
            
            texts = [row["chunk_text"] for row in results]
            embeddings = await embed_texts(texts)

            logger.info(f"Embedding {len(results)} chunks")
            
            BATCH_SIZE = 100
            for i in range(0, len(results), BATCH_SIZE):
                batch_rows = results[i:i+BATCH_SIZE]
                batch_embeddings = embeddings[i:i+BATCH_SIZE]
                vectors = [
                    (str(row["chunk_id"]), emb, {
                        "chunk_text": row["chunk_text"],
                        "doc_id": str(row["doc_id"]),
                        "document_title": row["document_title"],
                        "category": row["category"],
                        "type": "text"})
                    for row, emb in zip(batch_rows, batch_embeddings)
                ]
                index.upsert(vectors=vectors)
                # update is_embedded for this batch

                chunk_ids = [row["chunk_id"] for row in batch_rows]
                await conn.executemany(update_query, [(cid,) for cid in chunk_ids])

            logger.info(f"Embedding pipeline complete - {len(results)} chunks embedded")
                
    except Exception as e:
        logger.error(f"Failed to embed text: {e}")
        raise


    try: 
        db = get_db()
        tables = await db["tables"].find({"is_embedded": False}).to_list(None)

        table_texts = [t["table_markdown"] for t in tables]
        table_embeddings = await embed_texts(table_texts)


        for i in range(0, len(tables), BATCH_SIZE):

            batch_tables = tables[i:i+BATCH_SIZE]
            batch_table_embeddings = table_embeddings[i:i+BATCH_SIZE]


            vectors = [
                        (str(table["_id"]), emb, {
                            "chunk_text": table["table_markdown"],
                            "doc_id": str(table["doc_id"]),
                            "page_number": table["page_number"],
                            "category": table["category"],
                            "file_name": table["file_name"],
                            "type": "table"                
                            }) 
                            for table, emb in zip(batch_tables, batch_table_embeddings)
                            ]
                
            index.upsert(vectors=vectors)

            table_ids = [table["_id"] for table in batch_tables]
            await db["tables"].update_many(
                {"_id": {"$in": table_ids}},
                {"$set": {"is_embedded": True}}
        )

    except Exception as e:
        logger.error(f"Failed to embed table: {e}")
        raise