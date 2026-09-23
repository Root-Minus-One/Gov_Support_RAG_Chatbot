from sentence_transformers import CrossEncoder

_reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query: str, chunks: list[dict], top_k: int) -> list[dict]:

    if not chunks:
        return []
    pairs = [[query, chunk["chunk_text"]] for chunk in chunks]

    scores = _reranker.predict(pairs)

    scored_chunks = []
    for chunk, score in zip(chunks, scores):
        # Create a shallow copy to avoid mutating the input objects directly
        updated_chunk = chunk.copy()
        updated_chunk["rerank_score"] = float(score)
        scored_chunks.append(updated_chunk)

    sorted_chunks = sorted(
        scored_chunks, key=lambda x: x["rerank_score"], reverse=True
    )

    return sorted_chunks[:top_k]