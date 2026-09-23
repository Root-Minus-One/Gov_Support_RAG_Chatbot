from rank_bm25 import BM25Okapi
from app.db.postgres import get_pool
import numpy as np

from loguru import logger


_bm25_index = None
_corpus_chunk_ids = []  # maps BM25 result index → chunk_id
_corpus_texts = []


async def build_bm25_index() -> None:
    global _bm25_index, _corpus_chunk_ids, _corpus_texts
    # fetch all chunks from Postgres

    try:
        pool = get_pool()
        async with pool.acquire() as conn:
            retrieve_query = "SELECT chunk_id, chunk_text FROM chunks;"

            rows = await conn.fetch(retrieve_query)
            _corpus_chunk_ids = [row["chunk_id"] for row in rows]
            _corpus_texts = [row["chunk_text"] for row in rows]

            tokenized_corpus = [text.split() for text in _corpus_texts]

            # build BM25 index
            _bm25_index = BM25Okapi(tokenized_corpus)

    except Exception as e:
        logger.error(f"Failed to build BM25 index: {e}")
        raise
    
    # store corpus and chunk_ids in memory

def bm25_search(query: str, top_k: int) -> list[dict]:
    global _bm25_index, _corpus_chunk_ids, _corpus_texts

    if _bm25_index is None:
        raise RuntimeError(
            "BM25 index has not been initialized. Call build_bm25_index first."
        )
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

        results.append(
            {
                "chunk_id": _corpus_chunk_ids[idx],
                "chunk_text": _corpus_texts[idx],
                "score": float(scores[idx]),
                "rank": rank,
            }
        )

    return results