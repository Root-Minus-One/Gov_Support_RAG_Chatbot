from pinecone import Pinecone
from loguru import logger


from app.core.config import settings
from app.rag.embeddings import embed_texts
from app.rag.embeddings import index
from app.rag.hybrid_search import bm25_search
from app.rag.reranker import rerank

async def retrieve_chunks(question: str, top_k: int = 3, category: str | None = None) -> list[dict]:

    embed_question = await embed_texts([question])
    embedding = embed_question[0]

    filter_dict = {"category": category} if category else None

    response = index.query(
        vector=embedding,
        top_k=top_k,
        filter=filter_dict,
        include_metadata=True
    )

    vector_results = []
    for match in response['matches']:
        if match["score"] < 0.5:
            continue
        vector_results.append({
            "chunk_id": match["id"],
            "chunk_text": match["metadata"].get("chunk_text", ""),
            "doc_id": match["metadata"].get("doc_id", ""),
            "document_title": match["metadata"].get("document_title", ""),
            "page_number": match["metadata"].get("page_number", ""),
            "score": match["score"],
            "category": match["metadata"].get("category", "unknown")
        })

    bm25_results = bm25_search(question,top_k)

    fused_rank = reciprocal_rank_fusion(vector_results, bm25_results)

    all_chunks = {}
    for chunk in vector_results + bm25_results:
        chunk_id = chunk.get("chunk_id")
        all_chunks[chunk_id] = chunk

    # Reconstruct Full Chunk Objects with RRF Scores
    fused_chunks = []
    for chunk_id, rrf_score in fused_rank:
        if chunk_id in all_chunks:
            chunk = all_chunks[chunk_id].copy()
            chunk["rrf_score"] = rrf_score
            fused_chunks.append(chunk)

    final_result = rerank(query=question, chunks=fused_chunks, top_k=top_k)

    return final_result


def reciprocal_rank_fusion(vector_results, bm25_results, k=60):
    scores = {}
    
    for rank, chunk in enumerate(vector_results, start=1):
        chunk_id = chunk["chunk_id"]
        scores[chunk_id] = scores.get(chunk_id, 0) + 1/(rank + k)
    
    for rank, chunk in enumerate(bm25_results, start=1):
        chunk_id = chunk["chunk_id"]
        scores[chunk_id] = scores.get(chunk_id, 0) + 1/(rank + k)
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)