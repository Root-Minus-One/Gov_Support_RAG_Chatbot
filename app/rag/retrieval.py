from pinecone import Pinecone
from loguru import logger


from app.core.config import settings
from app.rag.embeddings import embed_texts
from app.rag.embeddings import index


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

    results = []
    for match in response['matches']:
        if match["score"] < 0.5:
            continue
        results.append({"chunk_text": match["metadata"].get("chunk_text", ""),
                        "doc_id": match["metadata"].get("doc_id", ""),
                        "score": match["score"],
                        "category": match["metadata"].get("category", "unknown")})

    return results