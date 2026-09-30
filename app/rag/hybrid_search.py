from rank_bm25 import BM25Okapi
from app.db.postgres import get_pool
import numpy as np

from loguru import logger


_bm25_index = None
_corpus_chunk_ids = []  # maps BM25 result index → chunk_id
_corpus_texts = []


async def build_bm25_index() -> None:
    global _bm25_index, _corpus_chunk_ids, _corpus_texts, _corpus_metadata
    # fetch all chunks from Postgres

    try:
        pool = get_pool()
        async with pool.acquire() as conn:
            retrieve_query = "SELECT chunk_id, chunk_text, doc_id, page_number FROM chunks;"

            rows = await conn.fetch(retrieve_query)
            _corpus_chunk_ids = [row["chunk_id"] for row in rows]
            _corpus_texts = [row["chunk_text"] for row in rows]

            # Save metadata mapping for search lookup
            _corpus_metadata = [
                {
                    "doc_id": row.get("doc_id", ""),
                    "page_number": row.get("page_number", None),
                    "category": row.get("category", "unknown")
                }
                for row in rows
            ]

            tokenized_corpus = [text.split() for text in _corpus_texts]

            _bm25_index = BM25Okapi(tokenized_corpus)

    except Exception as e:
        logger.error(f"Failed to build BM25 index: {e}")
        raise
    
    # store corpus and chunk_ids in memory

def bm25_search(query: str, top_k: int) -> list[dict]:
    global _bm25_index, _corpus_chunk_ids, _corpus_texts

    if _bm25_index is None:
        raise RuntimeError("BM25 index has not been initialized. Call build_bm25_index first.")
    
    # tokenize query
    tokenized_query = query.lower().split()

    # search BM25 index
    scores = _bm25_index.get_scores(tokenized_query)

    top_k_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for rank, idx in enumerate(top_k_indices, start=1):
        # Skip results with 0 score if you only want relevant matches
        if scores[idx] <= 0:
            continue

        metadata = _corpus_metadata[idx]

        results.append(
            {
                "chunk_id": _corpus_chunk_ids[idx],
                "chunk_text": _corpus_texts[idx],
                "doc_id": _corpus_metadata[idx]["doc_id"],
                "page_number": _corpus_metadata[idx]["page_number"],
                "category": _corpus_metadata[idx]["category"],
                "score": float(scores[idx]),
                "rank": rank,
            }
        )

    return results